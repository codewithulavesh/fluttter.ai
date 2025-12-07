# 🚀 Inherit.AI - AI-Powered Flutter Code Generation Platform

> A Lovable-like platform for generating Flutter code using AI. Built with React, FastAPI, and fine-tuned CodeLlama.

![Platform](https://img.shields.io/badge/Platform-Full%20Stack-blue)
![AI Model](https://img.shields.io/badge/AI-CodeLlama--7B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

- 🤖 **AI-Powered Code Generation** - Generate Flutter widgets from natural language
- 🎨 **Beautiful UI** - Modern, responsive interface built with React + shadcn/ui
- 🔄 **Multiple Variants** - Get 3 different code variations for each prompt
- 📝 **Code Editor** - Built-in editor with syntax highlighting
- 📱 **Device Preview** - See your Flutter UI in real-time
- 🎯 **Style Presets** - Choose from different UI styles (Lovable, Material, Cupertino)
- 💾 **Project Management** - Create, save, and manage multiple projects
- 🚀 **Fast Generation** - Optimized inference with 4-bit quantization

---

## 🏗️ Architecture

```
inherit.ai/
├── frontend/          # React + TypeScript + Vite
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # App pages
│   │   ├── stores/      # State management (Zustand)
│   │   └── lib/         # API client & utilities
│   └── package.json
│
├── backend/           # Python + FastAPI
│   ├── api_server.py     # API server
│   ├── train_sft.py      # Supervised fine-tuning
│   ├── train_dpo.py      # DPO training
│   ├── inference.py      # Model inference
│   ├── data.json         # Training dataset
│   └── requirements.txt
│
└── start.sh          # Startup script
```

---

## 🚀 Quick Start

### One-Command Start
```bash
./start.sh
```

This will:
1. Start the backend API server (port 8000)
2. Start the frontend dev server (port 5173)
3. Open your browser automatically

### Manual Start

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install fastapi uvicorn
python api_server.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📖 Documentation

- **[Full Stack Setup Guide](FULLSTACK_SETUP.md)** - Complete setup instructions
- **[Training Guide](backend/COLAB_SETUP.md)** - How to train the model on Google Colab
- **[Troubleshooting](backend/TROUBLESHOOTING.md)** - Common issues and solutions
- **[API Documentation](http://localhost:8000/docs)** - Interactive API docs (when server is running)

---

## 🎯 Usage

### 1. Create a New Project
- Click "New Project" on the dashboard
- Choose a template (Blank, E-commerce, Social, etc.)
- Enter project name and description

### 2. Generate Code
- Open your project in the editor
- Enter a prompt: `"Create a Flutter button with rounded corners and gradient background"`
- Click "Generate UI" or press `Cmd+Enter`
- Wait for AI to generate 3 variants

### 3. Review & Apply
- Review the generated code variants
- Click on a variant to preview it
- Click "Accept" to apply it to your project

### 4. Export
- Click "Export" to download your Flutter project as a ZIP file
- Extract and run with `flutter run`

---

## 🧠 AI Model

### Base Model
- **CodeLlama-7B** - Meta's code generation model

### Fine-Tuning
The model is fine-tuned using:
1. **Supervised Fine-Tuning (SFT)** - Learn from Flutter code examples
2. **Direct Preference Optimization (DPO)** - Learn from preferred code styles

### Training Your Own Model

#### Quick Training (15-30 min)
```bash
cd backend
python train_quick.py
```

#### Full Training (3-6 hours)
```bash
cd backend
./run_training.sh
```

#### Google Colab Training
See [COLAB_SETUP.md](backend/COLAB_SETUP.md) for step-by-step instructions.

---

## 🛠️ Tech Stack

### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **shadcn/ui** - UI components
- **Tailwind CSS** - Styling
- **Zustand** - State management
- **React Router** - Routing
- **TanStack Query** - Data fetching

### Backend
- **FastAPI** - API framework
- **PyTorch** - ML framework
- **Transformers** - Hugging Face library
- **PEFT** - Parameter-efficient fine-tuning
- **bitsandbytes** - Quantization

### AI/ML
- **CodeLlama-7B** - Base model
- **LoRA** - Efficient fine-tuning
- **QLoRA** - 4-bit quantization
- **DPO** - Preference optimization

---

## 📊 Performance

### Model Performance
- **Inference Speed**: ~2-5 seconds per variant (on T4 GPU)
- **VRAM Usage**: ~6GB (with 4-bit quantization)
- **Quality**: Improves significantly with fine-tuning

### System Requirements

#### Minimum
- **CPU**: 4 cores
- **RAM**: 8GB
- **GPU**: Optional (CPU inference supported)
- **Storage**: 10GB

#### Recommended
- **CPU**: 8+ cores
- **RAM**: 16GB+
- **GPU**: NVIDIA GPU with 8GB+ VRAM (T4, RTX 3060, etc.)
- **Storage**: 20GB+

---

## 🔧 Configuration

### Backend Configuration
Edit `backend/config.ini`:

```ini
[model]
base_model = codellama/CodeLlama-7b-hf
use_4bit = true

[training]
train_batch_size = 2
max_length = 1024

[lora]
rank = 16
alpha = 32
```

### Frontend Configuration
Edit `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
```

---

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://localhost:8000/health

# Generate code
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a button", "num_variants": 1}'
```

### Test Frontend
```bash
cd frontend
npm run build  # Build for production
npm run preview  # Preview production build
```

---

## 🚢 Deployment

### Backend Deployment

#### Docker
```bash
cd backend
docker build -t inherit-ai-backend .
docker run -p 8000:8000 inherit-ai-backend
```

#### Cloud GPU
- **RunPod**: Upload backend folder, run `python api_server.py`
- **Vast.ai**: Same as RunPod
- **Google Cloud**: Use GPU instances with CUDA

### Frontend Deployment

#### Vercel/Netlify
```bash
cd frontend
npm run build
# Upload dist/ folder
```

Update `.env` with production API URL.

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Meta AI** - CodeLlama model
- **Hugging Face** - Transformers library
- **Lovable** - Inspiration for the UI/UX
- **shadcn/ui** - Beautiful UI components

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/codewithulavesh/fluttter.ai/issues)
- **Documentation**: See docs in this repository
- **Email**: [your-email@example.com]

---

## 🗺️ Roadmap

### Current Version (v1.0)
- [x] AI code generation
- [x] Multiple variants
- [x] Code editor
- [x] Project management
- [x] Fine-tuning pipeline

### Upcoming (v1.1)
- [ ] User authentication
- [ ] Database persistence
- [ ] Real Flutter preview
- [ ] Code export improvements
- [ ] Team collaboration

### Future (v2.0)
- [ ] Multi-language support (React, Vue, etc.)
- [ ] Version control integration
- [ ] Advanced code refactoring
- [ ] Marketplace for templates
- [ ] Enterprise features

---

## 📈 Stats

- **Lines of Code**: ~15,000+
- **Components**: 50+
- **API Endpoints**: 5
- **Training Dataset**: 100+ Flutter examples
- **Model Parameters**: 7B (base) + LoRA adapters

---

## 🎓 Learn More

- [Flutter Documentation](https://flutter.dev/docs)
- [CodeLlama Paper](https://arxiv.org/abs/2308.12950)
- [DPO Paper](https://arxiv.org/abs/2305.18290)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)

---

**Made with ❤️ by [Ulavesh](https://github.com/codewithulavesh)**

**Star ⭐ this repo if you find it useful!**

---

Last Updated: December 7, 2025
