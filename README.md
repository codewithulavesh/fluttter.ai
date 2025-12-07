# Flutter Code Generation - Fine-tuning Pipeline

Complete pipeline for fine-tuning language models on Flutter code generation using **Supervised Fine-Tuning (SFT)** and **Reinforcement Learning (DPO)**.

## 📋 Overview

This project provides a complete training pipeline to create a specialized Flutter code generation model:

1. **Data Preparation**: Convert your Flutter dataset into training-ready formats
2. **Supervised Fine-Tuning (SFT)**: Initial training on instruction-response pairs
3. **Direct Preference Optimization (DPO)**: Reinforcement learning through preference learning

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Prepare Dataset

```bash
python prepare_dataset.py
```

This will create three datasets in `./processed_data/`:
- `sft_dataset/` - For supervised fine-tuning
- `chat_dataset/` - For chat-based training
- `dpo_dataset/` - For preference optimization

### 3. Run Supervised Fine-Tuning

```bash
python train_sft.py
```

**Configuration options in `train_sft.py`:**
- `model_name`: Base model to fine-tune (default: CodeLlama-7b)
- `use_lora`: Enable LoRA for efficient training (default: True)
- `use_4bit`: Enable 4-bit quantization/QLoRA (default: True)
- `num_train_epochs`: Number of training epochs (default: 3)
- `learning_rate`: Learning rate (default: 2e-4)

### 4. Run DPO Training (Reinforcement Learning)

```bash
python train_dpo.py
```

**Configuration options in `train_dpo.py`:**
- `model_name`: SFT model path (default: ./outputs/sft_model)
- `beta`: DPO temperature parameter (default: 0.1)
- `loss_type`: DPO loss function (default: sigmoid)
- `num_train_epochs`: Number of epochs (default: 1)

## 📊 Dataset Format

Your `data.json` contains 6 Flutter project datasets with instruction-following format:

```json
{
  "dataset_name": "flutter_todo_app_professional",
  "metadata": {
    "framework": "Flutter 3.0+",
    "architecture": "Clean Architecture"
  },
  "instructions": [
    {
      "instruction": "Create a Flutter ToDo application...",
      "input": "",
      "output": {
        "project_structure": {...}
      }
    }
  ]
}
```

## 🎯 Training Pipeline

### Stage 1: Supervised Fine-Tuning (SFT)
- **Purpose**: Teach the model to follow instructions and generate Flutter code
- **Method**: Standard supervised learning on instruction-response pairs
- **Duration**: ~3 epochs
- **Output**: Base fine-tuned model

### Stage 2: Direct Preference Optimization (DPO)
- **Purpose**: Improve code quality through preference learning
- **Method**: Learn from chosen vs. rejected response pairs
- **Duration**: ~1 epoch
- **Output**: Reinforcement-learned model

## 💡 Model Recommendations

### For Code Generation:
1. **CodeLlama-7B/13B** (Recommended)
   - Specialized for code
   - Best for Flutter/Dart generation
   
2. **Mistral-7B**
   - General purpose, good performance
   - Fast inference

3. **Llama-2-7B/13B**
   - Solid baseline
   - Good instruction following

### Hardware Requirements:

| Model Size | Method | VRAM Required |
|------------|--------|---------------|
| 7B | QLoRA (4-bit) | 8-12 GB |
| 7B | LoRA (16-bit) | 16-24 GB |
| 13B | QLoRA (4-bit) | 16-20 GB |
| 13B | LoRA (16-bit) | 32-40 GB |

## 🔧 Advanced Configuration

### LoRA Parameters

```python
lora_r=16,          # Rank (higher = more parameters)
lora_alpha=32,      # Scaling factor
lora_dropout=0.05   # Dropout rate
```

### Training Parameters

```python
per_device_train_batch_size=4,
gradient_accumulation_steps=4,  # Effective batch size = 4 * 4 = 16
learning_rate=2e-4,
warmup_ratio=0.03,
max_length=2048
```

### DPO Parameters

```python
beta=0.1,           # Temperature (0.1-0.5, higher = more conservative)
loss_type="sigmoid" # Options: sigmoid, hinge, ipo
```

## 📈 Monitoring Training

### Using Weights & Biases (WandB)

1. Login to WandB:
```bash
wandb login
```

2. Training metrics will be automatically logged:
   - Loss curves
   - Learning rate schedule
   - Gradient norms
   - Evaluation metrics

### Using TensorBoard

```bash
tensorboard --logdir ./outputs/sft_model/runs
```

## 🎓 Inference / Testing

After training, test your model:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./outputs/dpo_model")
tokenizer = AutoTokenizer.from_pretrained("./outputs/dpo_model")

prompt = """### Task: Flutter Application Development

**Framework**: Flutter 3.0+
**Architecture**: Clean Architecture

**Instruction**: Create a simple counter app with state management

**Output**:"""

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_length=2048, temperature=0.7)
print(tokenizer.decode(outputs[0]))
```

## 📁 Project Structure

```
datasets/
├── data.json                    # Your Flutter dataset
├── requirements.txt             # Python dependencies
├── prepare_dataset.py           # Dataset preparation script
├── train_sft.py                 # Supervised fine-tuning
├── train_dpo.py                 # DPO/reinforcement learning
├── processed_data/              # Prepared datasets
│   ├── sft_dataset/
│   ├── chat_dataset/
│   └── dpo_dataset/
└── outputs/                     # Trained models
    ├── sft_model/
    └── dpo_model/
```

## 🐛 Troubleshooting

### Out of Memory (OOM)
- Reduce `per_device_train_batch_size`
- Increase `gradient_accumulation_steps`
- Enable `gradient_checkpointing=True`
- Use 4-bit quantization (`use_4bit=True`)

### Slow Training
- Use `bf16=True` instead of `fp16`
- Enable `gradient_checkpointing=False` if you have enough VRAM
- Reduce `max_length`

### Poor Results
- Increase training epochs
- Try different learning rates (1e-5 to 5e-4)
- Adjust LoRA rank (8, 16, 32, 64)
- For DPO: adjust `beta` parameter

## 📚 References

- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [QLoRA Paper](https://arxiv.org/abs/2305.14314)
- [DPO Paper](https://arxiv.org/abs/2305.18290)
- [TRL Library](https://github.com/huggingface/trl)

## 📝 License

MIT License

## 🤝 Contributing

Feel free to open issues or submit pull requests!

---

**Happy Training! 🚀**
# fluttter.ai
