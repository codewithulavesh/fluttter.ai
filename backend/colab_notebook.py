"""
Flutter AI Code Generation - Google Colab Training Notebook
============================================================
Copy each cell below into separate cells in Google Colab

GPU: Tesla T4 (15GB VRAM)
CUDA: 12.4
"""

# ========================================
# CELL 1: Verify GPU
# ========================================
print("🔍 Checking GPU availability...")
!nvidia-smi
print("\n✅ If you see Tesla T4 above, you're good to go!")

# ========================================
# CELL 2: Clone Repository
# ========================================
print("📦 Cloning repository...")
!git clone https://github.com/codewithulavesh/fluttter.ai.git
%cd fluttter.ai
!ls -la
print("\n✅ Repository cloned!")

# ========================================
# CELL 3: Install Dependencies
# ========================================
print("📚 Installing dependencies (this may take 3-5 minutes)...")
!pip install -q torch>=2.1.0 transformers>=4.36.0 datasets>=2.16.0 \
    accelerate>=0.25.0 peft>=0.7.0 bitsandbytes>=0.41.0 \
    trl>=0.7.0 evaluate>=0.4.1 wandb>=0.16.0 \
    tensorboard>=2.15.0 scipy>=1.11.0 pandas>=2.1.0 \
    numpy>=1.24.0 scikit-learn>=1.3.0 tqdm>=4.66.0 \
    python-dotenv>=1.0.0

print("\n✅ Verifying installations...")
!pip list | grep -E "torch|transformers|trl|peft|bitsandbytes"
print("\n✅ All dependencies installed!")

# ========================================
# CELL 4: Hugging Face Authentication
# ========================================
print("🔑 Logging into Hugging Face...")
print("Get your token from: https://huggingface.co/settings/tokens")
from huggingface_hub import login
login()
print("\n✅ Authenticated with Hugging Face!")

# ========================================
# CELL 5: Weights & Biases (Optional)
# ========================================
# Uncomment if you want to use W&B for tracking
# print("📊 Logging into Weights & Biases...")
# print("Get your API key from: https://wandb.ai/authorize")
# import wandb
# wandb.login()

# If NOT using W&B, disable it in config:
print("⚙️ Disabling W&B logging...")
!sed -i 's/report_to = wandb/report_to = none/g' config.ini
print("✅ W&B disabled (using local logging)")

# ========================================
# CELL 6: Verify Dataset
# ========================================
print("📊 Checking dataset...")
import json

with open('data.json', 'r') as f:
    data = json.load(f)
    
print(f"✅ Dataset loaded successfully!")
print(f"📊 Total examples: {len(data)}")
print(f"📝 Example keys: {list(data[0].keys())}")
print(f"\n🔍 Sample entry (first 300 chars):")
print(json.dumps(data[0], indent=2)[:300] + "...")

# ========================================
# CELL 7: Optimize Config for T4 GPU
# ========================================
print("⚙️ Optimizing configuration for Tesla T4 GPU...")
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# T4-optimized settings (prevents OOM errors)
config['training']['train_batch_size'] = '2'
config['training']['eval_batch_size'] = '2'
config['training']['gradient_accumulation_steps'] = '8'
config['training']['max_length'] = '1024'
config['training']['gradient_checkpointing'] = 'true'
config['model']['use_4bit'] = 'true'
config['lora']['rank'] = '16'

with open('config.ini', 'w') as f:
    config.write(f)

print("✅ Configuration optimized!")
print("\n📋 Key settings:")
print(f"  • Batch size: 2")
print(f"  • Gradient accumulation: 8 (effective batch: 16)")
print(f"  • Max sequence length: 1024")
print(f"  • 4-bit quantization: Enabled")
print(f"  • LoRA rank: 16")

# ========================================
# CELL 8: Prepare Dataset
# ========================================
print("🔄 Processing dataset...")
print("This will create SFT and DPO datasets...")
!python prepare_dataset.py

print("\n✅ Dataset preparation complete!")
print("\n📁 Checking processed data:")
!ls -lh processed_data/

# ========================================
# CELL 9: Verify Processed Datasets
# ========================================
print("🔍 Verifying processed datasets...")
from datasets import load_from_disk

sft_data = load_from_disk('processed_data/sft_dataset')
print(f"\n✅ SFT Dataset:")
print(f"  • Train: {len(sft_data['train'])} examples")
print(f"  • Validation: {len(sft_data['validation'])} examples")
print(f"  • Features: {sft_data['train'].features}")

dpo_data = load_from_disk('processed_data/dpo_dataset')
print(f"\n✅ DPO Dataset:")
print(f"  • Train: {len(dpo_data['train'])} examples")
print(f"  • Validation: {len(dpo_data['validation'])} examples")
print(f"  • Features: {dpo_data['train'].features}")

# ========================================
# CELL 10: Start Training (OPTION 1 - Quick)
# ========================================
print("🚀 Starting QUICK training (recommended for testing)...")
print("⏱️ Estimated time: 15-30 minutes")
print("\n" + "="*50)
!python train_quick.py
print("="*50)
print("\n✅ Quick training complete!")

# ========================================
# CELL 11: Start Training (OPTION 2 - Full SFT)
# ========================================
# Uncomment to run full SFT training instead
# print("🚀 Starting FULL SFT training...")
# print("⏱️ Estimated time: 1-3 hours")
# print("\n" + "="*50)
# !python train_sft.py
# print("="*50)
# print("\n✅ SFT training complete!")

# ========================================
# CELL 12: Start Training (OPTION 3 - Full Pipeline)
# ========================================
# Uncomment to run complete SFT + DPO pipeline
# print("🚀 Starting COMPLETE training pipeline (SFT + DPO)...")
# print("⏱️ Estimated time: 3-6 hours")
# print("\n" + "="*50)
# !chmod +x run_training.sh
# !./run_training.sh
# print("="*50)
# print("\n✅ Complete training pipeline finished!")

# ========================================
# CELL 13: Monitor GPU During Training
# ========================================
# Run this in a separate cell while training
# !watch -n 2 nvidia-smi

# ========================================
# CELL 14: Check Training Outputs
# ========================================
print("📁 Checking training outputs...")
!ls -lh outputs/
print("\n📊 Model directories:")
!du -sh outputs/*

# ========================================
# CELL 15: Mount Google Drive
# ========================================
print("💾 Mounting Google Drive...")
from google.colab import drive
drive.mount('/content/drive')
print("✅ Google Drive mounted!")

# ========================================
# CELL 16: Save Model to Google Drive
# ========================================
print("💾 Saving model to Google Drive...")
import os
from datetime import datetime

# Create timestamped backup
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
drive_path = f"/content/drive/MyDrive/flutter_ai_models_{timestamp}"

!mkdir -p "{drive_path}"
!cp -r outputs/ "{drive_path}/"
!cp config.ini "{drive_path}/"
!cp data.json "{drive_path}/"

print(f"\n✅ Model saved to: {drive_path}")
print("\n📦 Saved files:")
!ls -lh "{drive_path}"

# ========================================
# CELL 17: Test Model - Basic Inference
# ========================================
print("🧪 Testing model with inference script...")
!python inference.py

# ========================================
# CELL 18: Test Model - Interactive
# ========================================
print("🧪 Loading model for interactive testing...")
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Configuration
base_model = "codellama/CodeLlama-7b-hf"
model_path = "outputs/sft_model"  # Change to outputs/dpo_model if you ran DPO

print(f"📦 Loading base model: {base_model}")
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    load_in_4bit=True,
    device_map="auto",
    torch_dtype=torch.float16,
)

print(f"🔧 Loading LoRA adapter from: {model_path}")
model = PeftModel.from_pretrained(model, model_path)

print("✅ Model loaded successfully!")

# Generation function
def generate_flutter_code(prompt, max_tokens=512, temperature=0.7):
    """Generate Flutter code from a prompt"""
    full_prompt = f"### Instruction:\n{prompt}\n\n### Response:\n"
    
    inputs = tokenizer(full_prompt, return_tensors="pt").to("cuda")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=0.95,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )
    
    generated = tokenizer.decode(outputs[0], skip_special_tokens=True)
    # Extract only the response part
    if "### Response:" in generated:
        generated = generated.split("### Response:")[1].strip()
    
    return generated

print("\n" + "="*60)
print("🎨 Model ready for testing!")
print("="*60)

# ========================================
# CELL 19: Test with Sample Prompts
# ========================================
print("🧪 Testing with sample prompts...\n")

test_prompts = [
    "Create a Flutter button widget with rounded corners and a gradient background",
    "Build a Flutter card widget with shadow and padding",
    "Create a Flutter text field with validation",
    "Design a Flutter app bar with custom colors",
]

for i, prompt in enumerate(test_prompts, 1):
    print(f"\n{'='*60}")
    print(f"Test {i}/{len(test_prompts)}")
    print(f"{'='*60}")
    print(f"📝 Prompt: {prompt}")
    print(f"\n🎨 Generated Code:")
    print("-" * 60)
    
    result = generate_flutter_code(prompt, max_tokens=300)
    print(result)
    print("-" * 60)

# ========================================
# CELL 20: Custom Prompt Testing
# ========================================
# Test with your own prompts
custom_prompt = "Create a Flutter ListView with custom items"  # Change this!

print(f"📝 Custom Prompt: {custom_prompt}\n")
print("🎨 Generated Code:")
print("="*60)
result = generate_flutter_code(custom_prompt, max_tokens=512, temperature=0.7)
print(result)
print("="*60)

# ========================================
# CELL 21: Upload to Hugging Face Hub (Optional)
# ========================================
# Uncomment to upload your model to Hugging Face
# from huggingface_hub import HfApi
# 
# api = HfApi()
# 
# # Replace with your username
# username = "YOUR_HF_USERNAME"
# 
# print(f"📤 Uploading model to Hugging Face Hub...")
# api.upload_folder(
#     folder_path="outputs/sft_model",
#     repo_id=f"{username}/flutter-codegen-sft",
#     repo_type="model",
# )
# print(f"✅ Model uploaded to: https://huggingface.co/{username}/flutter-codegen-sft")

# ========================================
# CELL 22: Cleanup & Summary
# ========================================
print("\n" + "="*60)
print("🎉 TRAINING COMPLETE - SUMMARY")
print("="*60)

import os
import json

# Check outputs
if os.path.exists("outputs/sft_model"):
    print("\n✅ SFT Model: outputs/sft_model")
    sft_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                   for dirpath, _, filenames in os.walk("outputs/sft_model")
                   for filename in filenames) / (1024**2)
    print(f"   Size: {sft_size:.2f} MB")

if os.path.exists("outputs/dpo_model"):
    print("\n✅ DPO Model: outputs/dpo_model")
    dpo_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                   for dirpath, _, filenames in os.walk("outputs/dpo_model")
                   for filename in filenames) / (1024**2)
    print(f"   Size: {dpo_size:.2f} MB")

print("\n📊 Dataset Info:")
with open('data.json', 'r') as f:
    data = json.load(f)
print(f"   Total examples: {len(data)}")

print("\n💾 Backup Location:")
print(f"   Google Drive: {drive_path}")

print("\n🎯 Next Steps:")
print("   1. Test model with various prompts (Cell 20)")
print("   2. Upload to Hugging Face Hub (Cell 21)")
print("   3. Download from Google Drive for deployment")
print("   4. Integrate into your Flutter development workflow")

print("\n" + "="*60)
print("Happy Coding! 🚀")
print("="*60)

# ========================================
# CELL 23: Clear GPU Memory (if needed)
# ========================================
# Run this if you need to free up GPU memory
# import torch
# import gc
# 
# del model
# del tokenizer
# gc.collect()
# torch.cuda.empty_cache()
# print("✅ GPU memory cleared!")
