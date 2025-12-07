# 🔧 Troubleshooting Guide - Google Colab Training

Common issues and solutions for training on Tesla T4 GPU.

---

## 🚨 Critical Issues

### 1. CUDA Out of Memory (OOM)

**Error Message:**
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Solutions (try in order):**

#### Solution A: Reduce Batch Size
```python
import configparser
config = configparser.ConfigParser()
config.read('config.ini')

config['training']['train_batch_size'] = '1'  # Minimum
config['training']['eval_batch_size'] = '1'
config['training']['gradient_accumulation_steps'] = '16'  # Compensate

with open('config.ini', 'w') as f:
    config.write(f)
```

#### Solution B: Reduce Sequence Length
```python
config['training']['max_length'] = '512'  # From 1024
```

#### Solution C: Clear GPU Memory
```python
import torch
import gc

torch.cuda.empty_cache()
gc.collect()

# Then restart runtime: Runtime → Restart runtime
```

#### Solution D: Enable More Aggressive Memory Optimization
```python
config['training']['gradient_checkpointing'] = 'true'
config['model']['use_4bit'] = 'true'
config['lora']['rank'] = '8'  # Reduce from 16
```

---

### 2. Model Download Fails

**Error Message:**
```
OSError: Can't load tokenizer for 'codellama/CodeLlama-7b-hf'
```

**Solution:**
```python
# Pre-download the model
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "codellama/CodeLlama-7b-hf"

print("Downloading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(model_name)

print("Downloading model...")
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    load_in_4bit=True,
    device_map="auto",
)

print("✅ Model downloaded and cached!")
```

---

### 3. Hugging Face Authentication Error

**Error Message:**
```
OSError: You are trying to access a gated repo.
```

**Solution:**
```python
from huggingface_hub import login

# Get token from: https://huggingface.co/settings/tokens
# Make sure token has READ access
login(token="your_token_here")

# Or use interactive login
login()
```

**Additional Steps:**
1. Go to https://huggingface.co/codellama/CodeLlama-7b-hf
2. Click "Agree and access repository"
3. Wait for approval (usually instant)
4. Try again

---

### 4. Dataset Loading Error

**Error Message:**
```
JSONDecodeError: Expecting value: line X column Y
```

**Solution:**
```python
# Validate JSON
import json

try:
    with open('data.json', 'r') as f:
        data = json.load(f)
    print(f"✅ JSON valid! {len(data)} entries")
except json.JSONDecodeError as e:
    print(f"❌ JSON Error at line {e.lineno}: {e.msg}")
    
# If invalid, re-download from GitHub
!wget https://raw.githubusercontent.com/codewithulavesh/fluttter.ai/main/data.json -O data.json
```

---

### 5. Colab Session Timeout

**Error Message:**
```
Your session crashed after using all available RAM.
```

**Prevention:**
```python
# Save checkpoints frequently
config['logging']['save_steps'] = '50'  # Save every 50 steps

# Monitor memory
!watch -n 30 free -h
```

**Recovery:**
```python
# Resume from checkpoint
# Training automatically resumes from last checkpoint if output dir exists
!python train_sft.py  # Will resume automatically
```

---

## ⚠️ Warning Issues

### 6. W&B Login Failed

**Error Message:**
```
wandb: ERROR Unable to authenticate
```

**Solution:**
```python
# Disable W&B
!sed -i 's/report_to = wandb/report_to = none/g' config.ini

# Verify
!grep "report_to" config.ini
```

---

### 7. Slow Training Speed

**Symptoms:**
- Training slower than expected
- GPU utilization < 80%

**Solutions:**

#### Check GPU Utilization
```python
!nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv -l 1
```

#### Optimize Batch Size
```python
# Increase if GPU memory allows
config['training']['train_batch_size'] = '4'
config['training']['gradient_accumulation_steps'] = '4'
```

#### Enable Mixed Precision
```python
config['training']['use_bf16'] = 'true'  # For T4 GPU
```

---

### 8. Import Errors

**Error Message:**
```
ModuleNotFoundError: No module named 'transformers'
```

**Solution:**
```python
# Reinstall all dependencies
!pip install --upgrade torch transformers datasets accelerate peft \
    bitsandbytes trl evaluate wandb tensorboard scipy pandas \
    numpy scikit-learn tqdm python-dotenv

# Verify
!pip list | grep transformers
```

---

### 9. BitsAndBytes Error

**Error Message:**
```
ImportError: libcudart.so.11.0: cannot open shared object file
```

**Solution:**
```python
# Install compatible bitsandbytes
!pip uninstall -y bitsandbytes
!pip install bitsandbytes==0.41.0

# Verify CUDA
!nvcc --version
```

---

### 10. Training Not Starting

**Symptoms:**
- Script runs but no progress
- Stuck at "Loading model..."

**Solutions:**

#### Check GPU Availability
```python
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"CUDA device: {torch.cuda.get_device_name(0)}")
print(f"CUDA version: {torch.version.cuda}")
```

#### Verify Dataset
```python
from datasets import load_from_disk

try:
    dataset = load_from_disk('processed_data/sft_dataset')
    print(f"✅ Dataset loaded: {len(dataset['train'])} examples")
except Exception as e:
    print(f"❌ Dataset error: {e}")
    print("Regenerating dataset...")
    !python prepare_dataset.py
```

---

## 🐛 Common Warnings (Safe to Ignore)

### 11. Token Warnings
```
Token indices sequence length is longer than the specified maximum sequence length
```
**Action:** None needed - sequences are automatically truncated

### 12. Gradient Checkpointing Warning
```
You are using gradient checkpointing with `use_reentrant=True`
```
**Action:** None needed - this is expected behavior

### 13. Padding Warning
```
Setting `pad_token_id` to `eos_token_id`
```
**Action:** None needed - automatic padding configuration

---

## 📊 Performance Diagnostics

### Check Training Progress
```python
# View latest logs
!tail -100 outputs/sft_model/trainer_log.txt

# Check tensorboard
%load_ext tensorboard
%tensorboard --logdir outputs/
```

### Monitor Resource Usage
```python
# GPU
!nvidia-smi

# RAM
!free -h

# Disk
!df -h

# Process
!ps aux | grep python
```

### Validate Model Output
```python
# Quick inference test
!python -c "
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

tokenizer = AutoTokenizer.from_pretrained('codellama/CodeLlama-7b-hf')
model = AutoModelForCausalLM.from_pretrained(
    'codellama/CodeLlama-7b-hf',
    load_in_4bit=True,
    device_map='auto'
)
model = PeftModel.from_pretrained(model, 'outputs/sft_model')

inputs = tokenizer('Create a button', return_tensors='pt').to('cuda')
outputs = model.generate(**inputs, max_new_tokens=50)
print(tokenizer.decode(outputs[0]))
"
```

---

## 🔄 Reset Everything

If all else fails:

```python
# 1. Clear outputs
!rm -rf outputs/
!rm -rf processed_data/

# 2. Clear cache
import torch
import gc
torch.cuda.empty_cache()
gc.collect()

# 3. Restart runtime
# Runtime → Restart runtime

# 4. Start fresh
!git pull origin main
!python prepare_dataset.py
!python train_quick.py
```

---

## 📞 Getting Help

### Collect Debug Information
```python
print("="*60)
print("DEBUG INFORMATION")
print("="*60)

# System info
!nvidia-smi
!free -h
!df -h

# Python packages
!pip list | grep -E "torch|transformers|trl|peft|bitsandbytes"

# Config
!cat config.ini

# Dataset
import json
with open('data.json', 'r') as f:
    data = json.load(f)
print(f"\nDataset: {len(data)} examples")

# Processed data
!ls -lh processed_data/

# Outputs
!ls -lh outputs/

print("="*60)
```

### Check Logs
```python
# Training logs
!find outputs/ -name "*.log" -o -name "*.txt" | head -5

# Last 50 lines of training
!tail -50 outputs/sft_model/trainer_log.txt
```

---

## ✅ Verification Checklist

Before asking for help, verify:

- [ ] GPU is Tesla T4 (`nvidia-smi`)
- [ ] CUDA 12.4 is available
- [ ] All packages installed (`pip list`)
- [ ] Authenticated with Hugging Face
- [ ] `data.json` is valid JSON
- [ ] Dataset processed successfully
- [ ] Config optimized for T4
- [ ] Enough disk space (>10GB free)
- [ ] Runtime hasn't timed out

---

## 🎯 Quick Fixes Summary

| Issue | Quick Fix |
|-------|-----------|
| OOM Error | Reduce batch size to 1 |
| Slow Download | Pre-download model |
| Auth Error | Re-run `login()` |
| JSON Error | Re-download `data.json` |
| Import Error | Reinstall dependencies |
| Timeout | Save to Drive frequently |
| No Progress | Check GPU with `nvidia-smi` |
| Bad Output | Increase training epochs |

---

**Last Updated:** December 7, 2025
