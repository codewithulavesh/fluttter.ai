"""
Direct Preference Optimization (DPO) Training Script
Implements reinforcement learning through preference-based training
This is more stable and efficient than traditional RLHF with PPO
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
    BitsAndBytesConfig
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import DPOTrainer, DPOConfig
import wandb


@dataclass
class ModelArguments:
    """Arguments for model configuration"""
    model_name: str = field(
        default="./outputs/sft_model",  # Use SFT model as base
        metadata={"help": "Base model (preferably SFT-trained model)"}
    )
    reference_model: Optional[str] = field(
        default=None,
        metadata={"help": "Reference model for DPO (if None, uses frozen copy of model)"}
    )
    use_lora: bool = field(
        default=True,
        metadata={"help": "Use LoRA for parameter-efficient fine-tuning"}
    )
    use_4bit: bool = field(
        default=True,
        metadata={"help": "Use 4-bit quantization"}
    )
    lora_r: int = field(default=16)
    lora_alpha: int = field(default=32)
    lora_dropout: float = field(default=0.05)


@dataclass
class DataArguments:
    """Arguments for data configuration"""
    data_path: str = field(
        default="./processed_data/dpo_dataset",
        metadata={"help": "Path to DPO dataset"}
    )
    max_length: int = field(default=2048)
    max_prompt_length: int = field(default=512)


@dataclass
class DPOTrainingArguments(DPOConfig):
    """DPO-specific training arguments"""
    output_dir: str = field(default="./outputs/dpo_model")
    num_train_epochs: int = field(default=1)
    per_device_train_batch_size: int = field(default=2)
    per_device_eval_batch_size: int = field(default=2)
    gradient_accumulation_steps: int = field(default=8)
    learning_rate: float = field(default=5e-5)
    weight_decay: float = field(default=0.01)
    warmup_ratio: float = field(default=0.1)
    lr_scheduler_type: str = field(default="cosine")
    logging_steps: int = field(default=10)
    save_steps: int = field(default=100)
    eval_steps: int = field(default=100)
    evaluation_strategy: str = field(default="steps")
    save_total_limit: int = field(default=3)
    bf16: bool = field(default=True)
    gradient_checkpointing: bool = field(default=True)
    report_to: str = field(default="wandb")
    
    # DPO-specific parameters
    beta: float = field(
        default=0.1,
        metadata={"help": "DPO temperature parameter (higher = more conservative)"}
    )
    loss_type: str = field(
        default="sigmoid",
        metadata={"help": "DPO loss type: sigmoid, hinge, or ipo"}
    )


class DPOTrainerWrapper:
    def __init__(
        self,
        model_args: ModelArguments,
        data_args: DataArguments,
        training_args: DPOTrainingArguments
    ):
        self.model_args = model_args
        self.data_args = data_args
        self.training_args = training_args
        
        # Initialize wandb
        wandb.init(
            project="flutter-code-generation",
            name=f"dpo-{model_args.model_name.split('/')[-1]}",
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
        self.tokenizer.padding_side = "left"  # Important for DPO
        
        # Model configuration
        if self.model_args.use_4bit:
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
        
        # Reference model (frozen copy for DPO)
        if self.model_args.reference_model:
            print(f"✓ Loading reference model: {self.model_args.reference_model}")
            self.ref_model = AutoModelForCausalLM.from_pretrained(
                self.model_args.reference_model,
                device_map="auto",
                torch_dtype=torch.bfloat16,
                trust_remote_code=True
            )
        else:
            print("✓ Using frozen copy of model as reference")
            self.ref_model = None  # DPOTrainer will create frozen copy
        
        # Apply LoRA to trainable model
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
        """Load and prepare DPO dataset"""
        print(f"\n📦 Loading DPO dataset from: {self.data_args.data_path}")
        
        self.dataset = load_from_disk(self.data_args.data_path)
        
        print(f"✓ Train examples: {len(self.dataset['train'])}")
        print(f"✓ Validation examples: {len(self.dataset['validation'])}")
        
        # Show sample
        sample = self.dataset['train'][0]
        print("\n📝 Sample DPO pair:")
        print(f"Prompt: {sample['prompt'][:100]}...")
        print(f"Chosen: {sample['chosen'][:100]}...")
        print(f"Rejected: {sample['rejected'][:100]}...")
    
    def train(self):
        """Start DPO training"""
        print("\n🚀 Starting DPO training...")
        
        # DPO Trainer
        trainer = DPOTrainer(
            model=self.model,
            ref_model=self.ref_model,
            args=self.training_args,
            train_dataset=self.dataset['train'],
            eval_dataset=self.dataset['validation'],
            tokenizer=self.tokenizer,
            max_length=self.data_args.max_length,
            max_prompt_length=self.data_args.max_prompt_length,
        )
        
        # Train
        trainer.train()
        
        # Save final model
        print("\n💾 Saving final model...")
        trainer.save_model(self.training_args.output_dir)
        self.tokenizer.save_pretrained(self.training_args.output_dir)
        
        print(f"✅ DPO training complete! Model saved to {self.training_args.output_dir}")
        
        wandb.finish()


def main():
    """Main execution"""
    print("=" * 70)
    print("DIRECT PREFERENCE OPTIMIZATION (DPO) TRAINING")
    print("=" * 70)
    print("\n⚠️  Make sure you've run SFT training first!")
    print("DPO works best when starting from an SFT-trained model.\n")
    
    # Configuration
    model_args = ModelArguments(
        model_name="./outputs/sft_model",  # Use your SFT model
        reference_model=None,  # Will use frozen copy
        use_lora=True,
        use_4bit=True,
        lora_r=16,
        lora_alpha=32
    )
    
    data_args = DataArguments(
        data_path="./processed_data/dpo_dataset",
        max_length=2048,
        max_prompt_length=512
    )
    
    training_args = DPOTrainingArguments(
        output_dir="./outputs/dpo_model",
        num_train_epochs=1,  # DPO typically needs fewer epochs
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,
        learning_rate=5e-5,  # Lower LR for DPO
        bf16=True,
        logging_steps=10,
        save_steps=100,
        eval_steps=100,
        evaluation_strategy="steps",
        save_total_limit=3,
        gradient_checkpointing=True,
        report_to="wandb",
        beta=0.1,  # DPO temperature
        loss_type="sigmoid"  # DPO loss type
    )
    
    # Initialize trainer
    trainer = DPOTrainerWrapper(model_args, data_args, training_args)
    
    # Train
    trainer.train()


if __name__ == "__main__":
    main()
