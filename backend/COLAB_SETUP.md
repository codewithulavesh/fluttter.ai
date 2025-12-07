# 🚀 Google Colab Setup Guide - Flutter Code Generation Model Training

This guide provides step-by-step instructions to train your Flutter code generation model on Google Colab with a Tesla T4 GPU (15GB VRAM).

---

## 📋 Prerequisites

- Google Account with Colab access
- GitHub repository: `https://github.com/codewithulavesh/fluttter.ai.git`
- Weights & Biases account (optional, for tracking)
- Hugging Face account (for model access)

---

## 🔧 Step 1: Setup Colab Environment

### 1.1 Create New Colab Notebook
1. Go to [Google Colab](https://colab.research.google.com/)
2. Click **File → New Notebook**
3. Click **Runtime → Change runtime type**
4. Select **T4 GPU** as Hardware accelerator
5. Click **Save**

### 1.2 Verify GPU Access
Run this in a cell to confirm your GPU:

```python
!nvidia-smi
```

Expected output should show:
- GPU: Tesla T4
- Memory: ~15360 MiB
- CUDA Version: 12.4

---

## 📦 Step 2: Clone Repository & Install Dependencies

### 2.1 Clone Your Repository
```python
# Clone the repository
!git clone https://github.com/codewithulavesh/fluttter.ai.git
%cd fluttter.ai
```

### 2.2 Install Required Packages
```python
# Install all dependencies
!pip install -q torch>=2.1.0 transformers>=4.36.0 datasets>=2.16.0 \
    accelerate>=0.25.0 peft>=0.7.0 bitsandbytes>=0.41.0 \
    trl>=0.7.0 evaluate>=0.4.1 wandb>=0.16.0 \
    tensorboard>=2.15.0 scipy>=1.11.0 pandas>=2.1.0 \
    numpy>=1.24.0 scikit-learn>=1.3.0 tqdm>=4.66.0 \
    python-dotenv>=1.0.0

# Verify installation
!pip list | grep -E "torch|transformers|trl|peft"
```

**⏱️ Expected Time:** 3-5 minutes

---

## 🔑 Step 3: Authentication Setup

### 3.1 Hugging Face Login (Required)
```python
# Login to Hugging Face to access models
from huggingface_hub import login

# You'll be prompted to enter your HF token
# Get token from: https://huggingface.co/settings/tokens
login()
```

### 3.2 Weights & Biases Login (Optional but Recommended)
```python
# Login to W&B for experiment tracking
import wandb

# You'll be prompted to enter your W&B API key
# Get key from: https://wandb.ai/authorize
wandb.login()
```

**If you don't want to use W&B**, update config.ini:
```python
# Disable W&B logging
!sed -i 's/report_to = wandb/report_to = none/g' config.ini
```

---

## 📊 Step 4: Verify Data

### 4.1 Check Dataset
```python
# Verify data.json exists and is valid
import json

with open('data.json', 'r') as f:
    data = json.load(f)
    
print(f"✅ Dataset loaded successfully!")
print(f"📊 Total examples: {len(data)}")
print(f"📝 First example keys: {list(data[0].keys())}")
```

### 4.2 Inspect Sample Data
```python
# Show a sample entry
print("\n🔍 Sample Entry:")
print(json.dumps(data[0], indent=2)[:500] + "...")
```

---

## ⚙️ Step 5: Configure Training Parameters

### 5.1 Review Configuration
```python
# Display current config
!cat config.ini
```

### 5.2 Optimize for T4 GPU (15GB VRAM)
```python
# Update config for T4 GPU - prevents OOM errors
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Optimize for T4 GPU
config['training']['train_batch_size'] = '2'  # Reduced for T4
config['training']['eval_batch_size'] = '2'
config['training']['gradient_accumulation_steps'] = '8'  # Maintain effective batch size
config['training']['max_length'] = '1024'  # Reduced sequence length
config['training']['gradient_checkpointing'] = 'true'  # Save memory
config['model']['use_4bit'] = 'true'  # Enable QLoRA
config['lora']['rank'] = '16'  # Balanced LoRA rank

# Save updated config
with open('config.ini', 'w') as f:
    config.write(f)

print("✅ Configuration optimized for T4 GPU!")
```

---

## 🎯 Step 6: Prepare Dataset

### 6.1 Process Raw Data
```python
# Process data.json into training-ready format
!python prepare_dataset.py

# This creates:
# - processed_data/sft_dataset/ (for supervised fine-tuning)
# - processed_data/dpo_dataset/ (for preference optimization)
# - processed_data/chat_dataset/ (for chat format)
```

**⏱️ Expected Time:** 1-2 minutes

### 6.2 Verify Processed Data
```python
# Check processed datasets
from datasets import load_from_disk

sft_data = load_from_disk('processed_data/sft_dataset')
print(f"✅ SFT Dataset: {sft_data}")

dpo_data = load_from_disk('processed_data/dpo_dataset')
print(f"✅ DPO Dataset: {dpo_data}")
```

---

## 🏋️ Step 7: Train the Model

### Option A: Quick Training (Recommended for Testing)
```python
# Quick training with reduced epochs - good for testing
!python train_quick.py
```
**⏱️ Expected Time:** 15-30 minutes

### Option B: Full SFT Training
```python
# Full supervised fine-tuning
!python train_sft.py
```
**⏱️ Expected Time:** 1-3 hours (depending on data size)

### Option C: Full Pipeline (SFT + DPO)
```python
# Complete training pipeline
!chmod +x run_training.sh
!./run_training.sh
```
**⏱️ Expected Time:** 3-6 hours

### Option D: DPO Only (After SFT)
```python
# Run DPO training on already fine-tuned model
!python train_dpo.py
```
**⏱️ Expected Time:** 1-2 hours

---

## 📈 Step 8: Monitor Training

### 8.1 Real-time Monitoring
If using W&B:
```python
# Your training will be visible at:
# https://wandb.ai/YOUR_USERNAME/flutter-code-generation
```

If using TensorBoard:
```python
# Load TensorBoard in Colab
%load_ext tensorboard
%tensorboard --logdir outputs/
```

### 8.2 Check Training Progress
```python
# Monitor GPU usage during training
!watch -n 1 nvidia-smi  # Run in separate cell
```

### 8.3 View Training Logs
```python
# Check latest logs
!tail -f outputs/sft_model/trainer_log.txt
```

---

## 💾 Step 9: Save Your Model

### 9.1 Check Output Directory
```python
# List trained models
!ls -lh outputs/
```

### 9.2 Save to Google Drive
```python
from google.colab import drive

# Mount Google Drive
drive.mount('/content/drive')

# Copy model to Drive
!cp -r outputs/ /content/drive/MyDrive/flutter_ai_models/

print("✅ Model saved to Google Drive!")
```

### 9.3 Upload to Hugging Face Hub (Optional)
```python
from huggingface_hub import HfApi

api = HfApi()

# Upload SFT model
api.upload_folder(
    folder_path="outputs/sft_model",
    repo_id="YOUR_USERNAME/flutter-codegen-sft",
    repo_type="model",
)

# Upload DPO model (if trained)
api.upload_folder(
    folder_path="outputs/dpo_model",
    repo_id="YOUR_USERNAME/flutter-codegen-dpo",
    repo_type="model",
)

print("✅ Models uploaded to Hugging Face!")
```

---

## 🧪 Step 10: Test Your Model

### 10.1 Run Inference
```python
# Test the trained model
!python inference.py
```

### 10.2 Interactive Testing
```python
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# Load model
base_model = "codellama/CodeLlama-7b-hf"
model_path = "outputs/sft_model"  # or outputs/dpo_model

print("Loading model...")
tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    load_in_4bit=True,
    device_map="auto",
)
model = PeftModel.from_pretrained(model, model_path)

# Test generation
def generate_code(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        temperature=0.7,
        top_p=0.95,
        do_sample=True,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Example test
prompt = "Create a Flutter button widget with rounded corners and gradient background"
result = generate_code(prompt)
print(f"\n🎨 Generated Code:\n{result}")
```

---

## 🔍 Step 11: Troubleshooting

### Common Issues & Solutions

#### ❌ Out of Memory (OOM) Error
```python
# Solution: Reduce batch size and sequence length
!sed -i 's/train_batch_size = 2/train_batch_size = 1/g' config.ini
!sed -i 's/max_length = 1024/max_length = 512/g' config.ini
```

#### ❌ CUDA Out of Memory
```python
# Clear GPU memory
import torch
torch.cuda.empty_cache()

# Restart runtime: Runtime → Restart runtime
```

#### ❌ Model Download Fails
```python
# Pre-download model
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "codellama/CodeLlama-7b-hf"
print("Downloading model...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
print("✅ Model downloaded!")
```

#### ❌ Dataset Loading Error
```python
# Regenerate processed data
!rm -rf processed_data/
!python prepare_dataset.py
```

#### ❌ Permission Denied for run_training.sh
```python
# Fix permissions
!chmod +x run_training.sh
```

---

## 📊 Step 12: Performance Optimization

### 12.1 Enable Flash Attention (Optional)
```python
# For faster training (requires compatible GPU)
!pip install flash-attn --no-build-isolation

# Update config to use flash attention
# Add to model loading: attn_implementation="flash_attention_2"
```

### 12.2 Monitor Resource Usage
```python
# Check memory usage
!free -h

# Check disk usage
!df -h

# GPU utilization
!nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv
```

---

## 📝 Complete Colab Notebook Template

Here's a complete notebook you can copy-paste:

```python
# ========================================
# CELL 1: Setup Environment
# ========================================
!nvidia-smi
!git clone https://github.com/codewithulavesh/fluttter.ai.git
%cd fluttter.ai

# ========================================
# CELL 2: Install Dependencies
# ========================================
!pip install -q torch>=2.1.0 transformers>=4.36.0 datasets>=2.16.0 \
    accelerate>=0.25.0 peft>=0.7.0 bitsandbytes>=0.41.0 \
    trl>=0.7.0 evaluate>=0.4.1 wandb>=0.16.0 \
    tensorboard>=2.15.0 scipy>=1.11.0 pandas>=2.1.0 \
    numpy>=1.24.0 scikit-learn>=1.3.0 tqdm>=4.66.0 \
    python-dotenv>=1.0.0

# ========================================
# CELL 3: Authentication
# ========================================
from huggingface_hub import login
login()

# Optional: W&B login
# import wandb
# wandb.login()

# ========================================
# CELL 4: Optimize Config for T4
# ========================================
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

config['training']['train_batch_size'] = '2'
config['training']['eval_batch_size'] = '2'
config['training']['gradient_accumulation_steps'] = '8'
config['training']['max_length'] = '1024'
config['training']['gradient_checkpointing'] = 'true'
config['model']['use_4bit'] = 'true'

with open('config.ini', 'w') as f:
    config.write(f)

print("✅ Config optimized!")

# ========================================
# CELL 5: Prepare Dataset
# ========================================
!python prepare_dataset.py

# ========================================
# CELL 6: Train Model (Choose One)
# ========================================
# Quick training (recommended for first run)
!python train_quick.py

# OR Full SFT training
# !python train_sft.py

# OR Complete pipeline
# !chmod +x run_training.sh
# !./run_training.sh

# ========================================
# CELL 7: Save to Google Drive
# ========================================
from google.colab import drive
drive.mount('/content/drive')
!cp -r outputs/ /content/drive/MyDrive/flutter_ai_models/
print("✅ Saved to Drive!")

# ========================================
# CELL 8: Test Model
# ========================================
!python inference.py
```

---

## ⏱️ Expected Timeline

| Step | Task | Time |
|------|------|------|
| 1-2 | Setup & Clone | 2-3 min |
| 3 | Install Dependencies | 3-5 min |
| 4 | Authentication | 1-2 min |
| 5 | Prepare Dataset | 1-2 min |
| 6 | Quick Training | 15-30 min |
| 6 | Full SFT Training | 1-3 hours |
| 6 | Full Pipeline (SFT+DPO) | 3-6 hours |
| 7 | Save & Test | 5-10 min |

**Total (Quick):** ~30-45 minutes  
**Total (Full):** ~4-7 hours

---

## 💡 Pro Tips

1. **Save Frequently**: Colab sessions timeout after 12 hours. Save to Drive regularly.
2. **Use Checkpoints**: Training saves checkpoints every 100 steps by default.
3. **Monitor GPU**: Keep an eye on GPU memory to prevent OOM errors.
4. **Start Small**: Use `train_quick.py` first to verify everything works.
5. **Backup Models**: Always save to Google Drive or Hugging Face Hub.
6. **Resume Training**: If interrupted, you can resume from the last checkpoint.

---

## 🎓 Next Steps

After successful training:

1. ✅ Test model with various Flutter prompts
2. ✅ Fine-tune hyperparameters based on results
3. ✅ Deploy model to production
4. ✅ Create API endpoint for inference
5. ✅ Build Flutter app integration

---

## 📞 Support

If you encounter issues:
- Check the **Troubleshooting** section above
- Review training logs in `outputs/`
- Verify GPU memory with `nvidia-smi`
- Ensure all dependencies are installed correctly

---

## 🎉 Success Checklist

- [ ] GPU verified (Tesla T4, 15GB)
- [ ] Repository cloned
- [ ] Dependencies installed
- [ ] Authenticated (HuggingFace)
- [ ] Dataset prepared
- [ ] Config optimized for T4
- [ ] Training completed without errors
- [ ] Model saved to Google Drive
- [ ] Inference tested successfully
- [ ] Model uploaded to HF Hub (optional)

---

**Happy Training! 🚀**

Last Updated: December 7, 2025
