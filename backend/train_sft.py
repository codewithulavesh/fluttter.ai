"""
Supervised Fine-Tuning (SFT) Script
Fine-tunes a language model on the Flutter code generation dataset
Supports: LoRA, QLoRA, and full fine-tuning
"""

import os
import torch
from dataclasses import dataclass, field
from typing import Optional
from datasets import load_from_disk
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import wandb


@dataclass
class ModelArguments:
    """Arguments for model configuration"""
    model_name: str = field(
        default="codellama/CodeLlama-7b-hf",
        metadata={"help": "Model to fine-tune (e.g., codellama/CodeLlama-7b-hf, mistralai/Mistral-7B-v0.1)"}
    )
    use_lora: bool = field(
        default=True,
        metadata={"help": "Use LoRA for parameter-efficient fine-tuning"}
    )
    use_4bit: bool = field(
        default=True,
        metadata={"help": "Use 4-bit quantization (QLoRA)"}
    )
    lora_r: int = field(
        default=16,
        metadata={"help": "LoRA rank"}
    )
    lora_alpha: int = field(
        default=32,
        metadata={"help": "LoRA alpha"}
    )
    lora_dropout: float = field(
        default=0.05,
        metadata={"help": "LoRA dropout"}
    )


@dataclass
class DataArguments:
    """Arguments for data configuration"""
    data_path: str = field(
        default="./processed_data/sft_dataset",
        metadata={"help": "Path to processed dataset"}
    )
    max_length: int = field(
        default=2048,
        metadata={"help": "Maximum sequence length"}
    )


@dataclass
class CustomTrainingArguments(TrainingArguments):
    """Custom training arguments"""
    output_dir: str = field(default="./outputs/sft_model")
    num_train_epochs: int = field(default=3)
    per_device_train_batch_size: int = field(default=4)
    per_device_eval_batch_size: int = field(default=4)
    gradient_accumulation_steps: int = field(default=4)
    learning_rate: float = field(default=2e-4)
    weight_decay: float = field(default=0.01)
    warmup_ratio: float = field(default=0.03)
    lr_scheduler_type: str = field(default="cosine")
    logging_steps: int = field(default=10)
    save_steps: int = field(default=100)
    eval_steps: int = field(default=100)
    evaluation_strategy: str = field(default="steps")
    save_total_limit: int = field(default=3)
    fp16: bool = field(default=True)
    gradient_checkpointing: bool = field(default=True)
    report_to: str = field(default="wandb")


class SFTTrainer:
    def __init__(
        self,
        model_args: ModelArguments,
        data_args: DataArguments,
        training_args: CustomTrainingArguments
    ):
        self.model_args = model_args
        self.data_args = data_args
        self.training_args = training_args
        
        # Initialize wandb
        wandb.init(
            project="flutter-code-generation",
            name=f"sft-{model_args.model_name.split('/')[-1]}",
            config={
                **vars(model_args),
                **vars(data_args),
                **vars(training_args)
            }
        )
        
        self.setup_model()
        self.setup_data()
    
    def setup_model(self):
        """Initialize model and tokenizer"""
        print(f"\n🔧 Loading model: {self.model_args.model_name}")
        
        # Tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_args.model_name,
            trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"
        
        # Model configuration
        if self.model_args.use_4bit:
            # QLoRA configuration
            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_args.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
            
            self.model = prepare_model_for_kbit_training(self.model)
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_args.model_name,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True
            )
        
        # Apply LoRA
        if self.model_args.use_lora:
            print("✓ Applying LoRA...")
            lora_config = LoraConfig(
                r=self.model_args.lora_r,
                lora_alpha=self.model_args.lora_alpha,
                target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
                lora_dropout=self.model_args.lora_dropout,
                bias="none",
                task_type="CAUSAL_LM"
            )
            
            self.model = get_peft_model(self.model, lora_config)
            self.model.print_trainable_parameters()
        
        print("✓ Model loaded successfully")
    
    def setup_data(self):
        """Load and prepare dataset"""
        print(f"\n📦 Loading dataset from: {self.data_args.data_path}")
        
        self.dataset = load_from_disk(self.data_args.data_path)
        
        # Tokenize dataset
        def tokenize_function(examples):
            # Combine prompt and completion
            texts = [
                f"{prompt}\n{completion}"
                for prompt, completion in zip(examples['prompt'], examples['completion'])
            ]
            
            tokenized = self.tokenizer(
                texts,
                truncation=True,
                max_length=self.data_args.max_length,
                padding="max_length",
                return_tensors="pt"
            )
            
            # Set labels (same as input_ids for causal LM)
            tokenized["labels"] = tokenized["input_ids"].clone()
            
            return tokenized
        
        print("✓ Tokenizing dataset...")
        self.tokenized_dataset = self.dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=self.dataset['train'].column_names,
            desc="Tokenizing"
        )
        
        print(f"✓ Train examples: {len(self.tokenized_dataset['train'])}")
        print(f"✓ Validation examples: {len(self.tokenized_dataset['validation'])}")
    
    def train(self):
        """Start training"""
        print("\n🚀 Starting training...")
        
        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )
        
        # Trainer
        trainer = Trainer(
            model=self.model,
            args=self.training_args,
            train_dataset=self.tokenized_dataset['train'],
            eval_dataset=self.tokenized_dataset['validation'],
            data_collator=data_collator,
        )
        
        # Train
        trainer.train()
        
        # Save final model
        print("\n💾 Saving final model...")
        trainer.save_model(self.training_args.output_dir)
        self.tokenizer.save_pretrained(self.training_args.output_dir)
        
        print(f"✅ Training complete! Model saved to {self.training_args.output_dir}")
        
        wandb.finish()


def main():
    """Main execution"""
    print("=" * 70)
    print("SUPERVISED FINE-TUNING (SFT)")
    print("=" * 70)
    
    # Configuration
    model_args = ModelArguments(
        model_name="codellama/CodeLlama-7b-hf",  # Change to your preferred model
        use_lora=True,
        use_4bit=True,
        lora_r=16,
        lora_alpha=32
    )
    
    data_args = DataArguments(
        data_path="./processed_data/sft_dataset",
        max_length=2048
    )
    
    training_args = CustomTrainingArguments(
        output_dir="./outputs/sft_model",
        num_train_epochs=3,
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=2e-4,
        fp16=False,  # Use bf16 instead
        bf16=True,
        logging_steps=10,
        save_steps=100,
        eval_steps=100,
        evaluation_strategy="steps",
        save_total_limit=3,
        gradient_checkpointing=True,
        report_to="wandb"
    )
    
    # Initialize trainer
    trainer = SFTTrainer(model_args, data_args, training_args)
    
    # Train
    trainer.train()


if __name__ == "__main__":
    main()
