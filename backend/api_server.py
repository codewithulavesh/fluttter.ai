"""
FastAPI Server for Flutter Code Generation
Serves the trained AI model and provides REST API endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import uvicorn
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Flutter AI Code Generator",
    description="AI-powered Flutter code generation API",
    version="1.0.0"
)

# CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Vite default ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model variables
model = None
tokenizer = None
device = "cuda" if torch.cuda.is_available() else "cpu"

# Request/Response Models
class GenerateRequest(BaseModel):
    prompt: str
    temperature: float = 0.7
    max_tokens: int = 512
    num_variants: int = 3
    style: Optional[str] = "lovable"

class CodeVariant(BaseModel):
    id: str
    code: str
    description: str
    score: float

class GenerateResponse(BaseModel):
    variants: List[CodeVariant]
    prompt: str
    generated_at: str

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    device: str
    timestamp: str

# Model Loading
def load_model():
    """Load the trained model and tokenizer"""
    global model, tokenizer
    
    try:
        base_model_name = "codellama/CodeLlama-7b-hf"
        
        # Check for trained model
        model_path = "outputs/dpo_model" if os.path.exists("outputs/dpo_model") else "outputs/sft_model"
        
        if not os.path.exists(model_path):
            logger.warning(f"No trained model found at {model_path}. Using base model only.")
            model_path = None
        
        logger.info(f"Loading tokenizer from {base_model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        
        logger.info(f"Loading base model from {base_model_name}...")
        model = AutoModelForCausalLM.from_pretrained(
            base_model_name,
            load_in_4bit=True,
            device_map="auto",
            torch_dtype=torch.float16,
        )
        
        # Load fine-tuned adapter if available
        if model_path:
            logger.info(f"Loading fine-tuned adapter from {model_path}...")
            model = PeftModel.from_pretrained(model, model_path)
            logger.info("✅ Fine-tuned model loaded successfully!")
        else:
            logger.info("✅ Base model loaded (no fine-tuning applied)")
        
        model.eval()
        logger.info(f"Model loaded on device: {device}")
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        raise

@app.on_event("startup")
async def startup_event():
    """Load model on server startup"""
    logger.info("Starting Flutter AI Code Generator API...")
    load_model()
    logger.info("Server ready to accept requests!")

# API Endpoints
@app.get("/", response_model=dict)
async def root():
    """Root endpoint"""
    return {
        "message": "Flutter AI Code Generator API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "generate": "/api/generate",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy" if model is not None else "model_not_loaded",
        model_loaded=model is not None,
        device=device,
        timestamp=datetime.now().isoformat()
    )

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """
    Generate Flutter code variants from a prompt
    
    Args:
        request: GenerateRequest with prompt and generation parameters
    
    Returns:
        GenerateResponse with code variants
    """
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        logger.info(f"Generating code for prompt: {request.prompt[:50]}...")
        
        variants = []
        
        # Generate multiple variants
        for i in range(request.num_variants):
            # Format prompt for the model
            formatted_prompt = f"""### Instruction:
Create a Flutter widget based on this description: {request.prompt}

Style: {request.style}

### Response:
"""
            
            # Tokenize input
            inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)
            
            # Generate code
            with torch.no_grad():
                outputs = model.generate(
                    **inputs,
                    max_new_tokens=request.max_tokens,
                    temperature=request.temperature + (i * 0.1),  # Vary temperature for diversity
                    top_p=0.95,
                    do_sample=True,
                    pad_token_id=tokenizer.eos_token_id,
                    num_return_sequences=1,
                )
            
            # Decode output
            generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the response part
            if "### Response:" in generated_text:
                code = generated_text.split("### Response:")[1].strip()
            else:
                code = generated_text.strip()
            
            # Create variant
            variant = CodeVariant(
                id=f"variant_{i+1}_{datetime.now().timestamp()}",
                code=code,
                description=f"Variant {i+1} - Temperature {request.temperature + (i * 0.1):.1f}",
                score=0.9 - (i * 0.1)  # Mock score, higher for first variants
            )
            variants.append(variant)
            
            logger.info(f"Generated variant {i+1}/{request.num_variants}")
        
        response = GenerateResponse(
            variants=variants,
            prompt=request.prompt,
            generated_at=datetime.now().isoformat()
        )
        
        logger.info(f"Successfully generated {len(variants)} variants")
        return response
        
    except Exception as e:
        logger.error(f"Error generating code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/refine")
async def refine_code(code: str, instructions: str):
    """Refine existing code based on instructions"""
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        formatted_prompt = f"""### Instruction:
Refine this Flutter code based on these instructions: {instructions}

Current code:
{code}

### Response:
"""
        
        inputs = tokenizer(formatted_prompt, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.95,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id,
            )
        
        refined_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        if "### Response:" in refined_code:
            refined_code = refined_code.split("### Response:")[1].strip()
        
        return {"refined_code": refined_code}
        
    except Exception as e:
        logger.error(f"Error refining code: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/model/info")
async def model_info():
    """Get information about the loaded model"""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    model_path = "outputs/dpo_model" if os.path.exists("outputs/dpo_model") else "outputs/sft_model"
    
    return {
        "base_model": "codellama/CodeLlama-7b-hf",
        "fine_tuned": os.path.exists(model_path),
        "model_path": model_path if os.path.exists(model_path) else None,
        "device": device,
        "model_type": "DPO" if "dpo" in model_path else "SFT" if os.path.exists(model_path) else "Base",
    }

# Run server
if __name__ == "__main__":
    uvicorn.run(
        "api_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
