# 🗂️ Project Structure - Clean & Organized

## 📁 Essential Files

```
datasets/
│
├── 📊 DATA
│   ├── data.json                    # Your Flutter dataset (6 examples)
│   └── processed_data/              # Prepared training datasets
│       ├── sft_dataset/            # For supervised fine-tuning
│       ├── chat_dataset/           # For chat-based training
│       └── dpo_dataset/            # For reinforcement learning
│
├── 🚀 TRAINING SCRIPTS
│   ├── prepare_dataset.py          # Convert data.json to training format
│   ├── train_quick.py              # Quick training (GPT-2, for testing)
│   ├── train_sft.py                # Full supervised fine-tuning
│   ├── train_dpo.py                # Reinforcement learning (DPO)
│   └── run_training.sh             # Automated training pipeline
│
├── 🧪 TESTING
│   └── inference.py                # Test your trained models
│
├── ⚙️ CONFIGURATION
│   ├── config.ini                  # Training parameters
│   └── requirements.txt            # Python dependencies
│
└── 📚 DOCUMENTATION
    ├── README.md                   # Complete guide
    └── TRAINING_STATUS.md          # Current status & next steps
```

## 🎯 Quick Reference

### Start Training
```bash
./run_training.sh              # Interactive menu
# OR
python3 train_quick.py         # Quick test (recommended for 6 examples)
# OR
python3 train_sft.py          # Full training (takes longer)
```

### Test Model
```bash
python3 inference.py --interactive
```

### Add More Data
1. Edit `data.json` (add more Flutter examples)
2. Run `python3 prepare_dataset.py`
3. Train again

---

**All unnecessary files removed! ✨**
**Total: 11 essential files + 1 data directory**
