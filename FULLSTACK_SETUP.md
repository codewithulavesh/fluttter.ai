# 🚀 Full Stack Setup Guide - Lovable-like Flutter AI Platform

Complete guide to run your AI-powered Flutter code generation platform (Frontend + Backend + AI Model).

---

## 📋 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR APPLICATION                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐         ┌──────────────┐                 │
│  │   FRONTEND   │  HTTP   │   BACKEND    │                 │
│  │              │ ◄─────► │              │                 │
│  │ React + Vite │         │ FastAPI      │                 │
│  │ Port: 5173   │         │ Port: 8000   │                 │
│  └──────────────┘         └──────┬───────┘                 │
│                                   │                          │
│                                   │ Inference                │
│                                   ▼                          │
│                          ┌─────────────────┐                │
│                          │   AI MODEL      │                │
│                          │                 │                │
│                          │ CodeLlama-7B    │                │
│                          │ + Fine-tuning   │                │
│                          └─────────────────┘                │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Quick Start (3 Steps)

### 1️⃣ Start Backend API Server
```bash
cd backend
python api_server.py
```

### 2️⃣ Start Frontend Dev Server
```bash
cd frontend
npm run dev
```

### 3️⃣ Open Browser
```
http://localhost:5173
```

---

## 📦 Detailed Setup

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **CUDA-capable GPU** (recommended, 8GB+ VRAM)
- **16GB+ RAM**

---

## 🔧 Backend Setup

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
# Install ML dependencies
pip install -r requirements.txt

# Install API server dependencies
pip install fastapi uvicorn[standard] python-multipart pydantic pydantic-settings
```

### Step 4: (Optional) Train Your Model
```bash
# Quick training (15-30 min)
python train_quick.py

# OR Full SFT training (1-3 hours)
python train_sft.py

# OR Complete pipeline (3-6 hours)
chmod +x run_training.sh
./run_training.sh
```

**Note:** You can skip training and use the base model, but results will be better with fine-tuning.

### Step 5: Start API Server
```bash
python api_server.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Loading tokenizer from codellama/CodeLlama-7b-hf...
INFO:     Loading base model from codellama/CodeLlama-7b-hf...
INFO:     ✅ Model loaded successfully!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 6: Test API
```bash
# In a new terminal
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "device": "cuda",
  "timestamp": "2025-12-07T20:00:00"
}
```

---

## 🎨 Frontend Setup

### Step 1: Navigate to Frontend
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Configure Environment
```bash
# .env file is already created with:
VITE_API_URL=http://localhost:8000
```

### Step 4: Start Dev Server
```bash
npm run dev
```

You should see:
```
VITE v5.4.19  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### Step 5: Open in Browser
```
http://localhost:5173
```

---

## 🧪 Testing the Integration

### Test 1: Health Check
1. Open browser to `http://localhost:5173`
2. Open browser console (F12)
3. The app should load without errors

### Test 2: Generate Code
1. Click "New Project" or open existing project
2. Go to Editor
3. Enter a prompt: `"Create a Flutter button with rounded corners"`
4. Click "Generate UI"
5. Wait for AI to generate variants
6. You should see 3 code variants appear

### Test 3: Check Console
Look for console message:
```
✅ Generated 3 variants using AI model
```

If you see:
```
⚠️ Using mock data (API unavailable)
```
Then the backend is not connected properly.

---

## 🔍 Troubleshooting

### Backend Issues

#### ❌ Port 8000 Already in Use
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9

# Or use different port
uvicorn api_server:app --port 8001
```

#### ❌ CUDA Out of Memory
```bash
# Edit api_server.py, change line 72:
load_in_4bit=True,  # Already enabled

# Or reduce max_tokens in API calls
# Edit frontend/src/stores/projectStore.ts line 88:
max_tokens: 256,  # Reduced from 512
```

#### ❌ Model Not Found
```bash
# Check if model exists
ls -la outputs/

# If no model, train one:
python train_quick.py

# Or use base model (edit api_server.py line 62):
model_path = None  # Force base model
```

### Frontend Issues

#### ❌ Port 5173 Already in Use
```bash
# Kill process
lsof -ti:5173 | xargs kill -9

# Or edit vite.config.ts to use different port
```

#### ❌ API Connection Failed
```bash
# Check backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/api_server.py
# Make sure your frontend port is in allow_origins
```

#### ❌ TypeScript Errors
```bash
# Rebuild
npm run build

# Or ignore and run anyway
npm run dev
```

---

## 🚀 Production Deployment

### Backend Deployment

#### Option 1: Docker
```dockerfile
# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 2: Cloud GPU (RunPod, Vast.ai, etc.)
```bash
# Upload backend folder
# SSH into instance
pip install -r requirements.txt
python api_server.py
```

### Frontend Deployment

#### Build for Production
```bash
cd frontend
npm run build
```

#### Deploy to Vercel/Netlify
```bash
# Update .env for production
VITE_API_URL=https://your-api-domain.com

npm run build
# Upload dist/ folder to hosting
```

---

## 📊 Performance Optimization

### Backend Optimization

#### 1. Use Quantization
Already enabled in `api_server.py`:
```python
load_in_4bit=True  # Reduces VRAM by 75%
```

#### 2. Batch Requests
```python
# For multiple requests, batch them
# Edit api_server.py to add batch endpoint
```

#### 3. Caching
```python
# Add Redis caching for common prompts
from functools import lru_cache

@lru_cache(maxsize=100)
def generate_cached(prompt: str):
    # ...
```

### Frontend Optimization

#### 1. Code Splitting
Already enabled with Vite

#### 2. Lazy Loading
```typescript
// Lazy load editor page
const Editor = lazy(() => import('./pages/Editor'));
```

#### 3. Debounce API Calls
```typescript
// Add debounce to prompt input
const debouncedGenerate = debounce(generateVariants, 500);
```

---

## 📈 Monitoring

### Backend Monitoring
```bash
# Add logging
tail -f api_server.log

# Monitor GPU
watch -n 1 nvidia-smi
```

### Frontend Monitoring
```typescript
// Add analytics
import { analytics } from './lib/analytics';

analytics.track('code_generated', {
  prompt_length: prompt.length,
  variants_count: variants.length,
});
```

---

## 🎓 Next Steps

### Immediate
- [x] Setup backend API server
- [x] Setup frontend dev server
- [x] Connect frontend to backend
- [ ] Test code generation
- [ ] Train model for better results

### Short Term
- [ ] Add user authentication
- [ ] Implement project persistence (database)
- [ ] Add code export functionality
- [ ] Improve error handling
- [ ] Add loading states

### Long Term
- [ ] Deploy to production
- [ ] Add team collaboration features
- [ ] Implement version control
- [ ] Add Flutter preview (actual rendering)
- [ ] Monetization (billing system)

---

## 📝 Development Workflow

### Daily Development
```bash
# Terminal 1: Backend
cd backend
source venv/bin/activate
python api_server.py

# Terminal 2: Frontend
cd frontend
npm run dev

# Terminal 3: Monitoring
watch -n 1 nvidia-smi
```

### Making Changes

#### Backend Changes
1. Edit `api_server.py` or other Python files
2. Server auto-reloads (uvicorn --reload)
3. Test with `curl` or frontend

#### Frontend Changes
1. Edit React components
2. Vite hot-reloads automatically
3. Check browser console for errors

---

## 🔐 Security Considerations

### Backend
- [ ] Add API authentication (JWT tokens)
- [ ] Rate limiting
- [ ] Input validation
- [ ] HTTPS in production

### Frontend
- [ ] Sanitize user input
- [ ] Secure API keys
- [ ] CORS configuration
- [ ] Content Security Policy

---

## 💡 Tips & Tricks

1. **Use Mock Data During Development**: If model is slow, temporarily use mock data
2. **Monitor GPU Memory**: Keep an eye on VRAM usage
3. **Save Checkpoints**: Train model in stages, save checkpoints
4. **Version Control**: Commit often, use branches
5. **Documentation**: Document your prompts and results

---

## 📞 Support

### Common Commands

```bash
# Check backend status
curl http://localhost:8000/health

# Check model info
curl http://localhost:8000/api/model/info

# Test generation
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Create a button", "num_variants": 1}'

# Frontend build
cd frontend && npm run build

# Backend logs
cd backend && tail -f api_server.log
```

---

## ✅ Success Checklist

- [ ] Backend API running on port 8000
- [ ] Frontend dev server running on port 5173
- [ ] Health check returns "healthy"
- [ ] Model loaded successfully
- [ ] Frontend connects to backend
- [ ] Code generation works
- [ ] Variants display correctly
- [ ] No console errors

---

**You're all set! 🎉**

Your Lovable-like Flutter AI platform is ready to use!

**Last Updated:** December 7, 2025
