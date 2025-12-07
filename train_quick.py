"""
Quick Training Script for Small Datasets
Optimized for your 6-example Flutter dataset
"""

import os
os.environ['WANDB_DISABLED'] = 'true'  # Disable wandb for quick testing

import torch
from datasets import load_from_disk
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
)
from peft import LoraConfig, get_peft_model


def main():
    print("=" * 70)
    print("QUICK TRAINING - SMALL DATASET")
    print("=" * 70)
    
    # Use a smaller model for testing
    model_name = "gpt2"  # Small model for quick testing
    
    print(f"\n🔧 Loading model: {model_name}")
    
    # Load tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # Use float32 for CPU/MPS
    )
    
    # Apply LoRA
    print("✓ Applying LoRA...")
    lora_config = LoraConfig(
        r=8,  # Smaller rank for quick training
        lora_alpha=16,
        target_modules=["c_attn"],  # GPT-2 attention modules
        lora_dropout=0.05,
        bias="none",
        task_type="CAUSAL_LM"
    )
    
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()
    
    # Load dataset
    print(f"\n📦 Loading dataset...")
    dataset = load_from_disk("./processed_data/sft_dataset")
    
    # Tokenize
    def tokenize_function(examples):
        texts = [
            f"{prompt}\n{completion}"
            for prompt, completion in zip(examples['prompt'], examples['completion'])
        ]
        
        tokenized = tokenizer(
            texts,
            truncation=True,
            max_length=512,  # Shorter for quick training
            padding="max_length",
            return_tensors="pt"
        )
        
        tokenized["labels"] = tokenized["input_ids"].clone()
        return tokenized
    
    print("✓ Tokenizing...")
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        remove_columns=dataset['train'].column_names,
    )
    
    # Training arguments
    training_args = TrainingArguments(
        output_dir="./outputs/quick_test",
        num_train_epochs=5,  # More epochs for small dataset
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        learning_rate=5e-4,
        logging_steps=1,
        save_steps=10,
        eval_steps=2,
        evaluation_strategy="steps",
        save_total_limit=2,
        report_to="none",  # Disable reporting
        remove_unused_columns=False,
    )
    
    # Data collator
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer,
        mlm=False
    )
    
    # Trainer
    print("\n🚀 Starting training...")
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_dataset['train'],
        eval_dataset=tokenized_dataset['validation'],
        data_collator=data_collator,
    )
    
    # Train
    trainer.train()
    
    # Save
    print("\n💾 Saving model...")
    trainer.save_model("./outputs/quick_test")
    tokenizer.save_pretrained("./outputs/quick_test")
    
    print("\n✅ Training complete!")
    print(f"Model saved to: ./outputs/quick_test")
    
    # Test generation
    print("\n🧪 Testing generation...")
    model.eval()
    
    test_prompt = """### Task: Flutter Application Development

**Framework**: Flutter 3.0+
**Architecture**: Clean Architecture

**Instruction**: Create a simple Flutter app

**Output**:"""
    
    inputs = tokenizer(test_prompt, return_tensors="pt")
    outputs = model.generate(
        **inputs,
        max_length=200,
        temperature=0.7,
        do_sample=True,
        pad_token_id=tokenizer.eos_token_id
    )
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print("\n" + "=" * 70)
    print("SAMPLE GENERATION:")
    print("=" * 70)
    print(generated[:500] + "..." if len(generated) > 500 else generated)
    print("=" * 70)


if __name__ == "__main__":
    main()
