# ⚡ Quick Start - Google Colab (1-Page Reference)

## 🎯 5-Minute Setup

### 1️⃣ Create Colab Notebook
- Go to [colab.research.google.com](https://colab.research.google.com)
- **Runtime → Change runtime type → T4 GPU**

### 2️⃣ Clone & Install (Copy-paste this cell)
```python
!nvidia-smi
!git clone https://github.com/codewithulavesh/fluttter.ai.git
%cd fluttter.ai
!pip install -q torch transformers datasets accelerate peft bitsandbytes trl evaluate wandb tensorboard scipy pandas numpy scikit-learn tqdm python-dotenv
```

### 3️⃣ Authenticate
```python
from huggingface_hub import login
login()  # Enter token from: https://huggingface.co/settings/tokens
```

### 4️⃣ Optimize for T4
```python
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
config['training']['train_batch_size'] = '2'
config['training']['gradient_accumulation_steps'] = '8'
config['training']['max_length'] = '1024'
config['model']['use_4bit'] = 'true'
config['logging']['report_to'] = 'none'  # Disable W&B
with open('config.ini', 'w') as f:
    config.write(f)
```

### 5️⃣ Prepare & Train
```python
!python prepare_dataset.py
!python train_quick.py  # 15-30 min
```

### 6️⃣ Save to Drive
```python
from google.colab import drive
drive.mount('/content/drive')
!cp -r outputs/ /content/drive/MyDrive/flutter_ai_model/
```

---

## 🚨 If You Get OOM Error

```python
# Emergency fix - run this and restart training
import configparser
config = configparser.ConfigParser()
config.read('config.ini')
config['training']['train_batch_size'] = '1'
config['training']['max_length'] = '512'
with open('config.ini', 'w') as f:
    config.write(f)
```

---

## 🧪 Test Your Model

```python
!python inference.py
```

---

## ⏱️ Training Times (Tesla T4)

| Mode | Time | Command |
|------|------|---------|
| Quick Test | 15-30 min | `!python train_quick.py` |
| Full SFT | 1-3 hours | `!python train_sft.py` |
| SFT + DPO | 3-6 hours | `!./run_training.sh` |

---

## 📚 Full Documentation

- **Complete Guide:** `COLAB_SETUP.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`
- **Full Notebook:** `colab_notebook.py`

---

## ✅ Success Checklist

- [ ] GPU shows Tesla T4 (15GB)
- [ ] Repository cloned
- [ ] Dependencies installed (no errors)
- [ ] Hugging Face authenticated
- [ ] Config optimized
- [ ] Dataset prepared
- [ ] Training started
- [ ] Model saved to Drive

---

**Need Help?** Check `TROUBLESHOOTING.md`

**Last Updated:** Dec 7, 2025
