"""
Inference Script for Testing Fine-tuned Models
Test your SFT or DPO models on Flutter code generation tasks
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from typing import Optional
import json


class FlutterCodeGenerator:
    def __init__(self, model_path: str, device: str = "auto"):
        """
        Initialize the code generator
        
        Args:
            model_path: Path to fine-tuned model (e.g., ./outputs/dpo_model)
            device: Device to run on (auto, cuda, cpu)
        """
        print(f"🔧 Loading model from: {model_path}")
        
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            trust_remote_code=True
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map=device,
            torch_dtype=torch.bfloat16,
            trust_remote_code=True
        )
        
        self.model.eval()
        print("✓ Model loaded successfully")
    
    def generate_code(
        self,
        instruction: str,
        input_text: str = "",
        framework: str = "Flutter 3.0+",
        architecture: str = "Clean Architecture",
        max_length: int = 2048,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        num_return_sequences: int = 1
    ) -> str:
        """
        Generate Flutter code based on instruction
        
        Args:
            instruction: What to build
            input_text: Additional context (optional)
            framework: Flutter framework version
            architecture: Architecture pattern
            max_length: Maximum tokens to generate
            temperature: Sampling temperature (higher = more creative)
            top_p: Nucleus sampling parameter
            top_k: Top-k sampling parameter
            num_return_sequences: Number of outputs to generate
            
        Returns:
            Generated code/project structure
        """
        # Format prompt
        prompt = f"""### Task: Flutter Application Development

**Framework**: {framework}
**Architecture**: {architecture}

**Instruction**: {instruction}
"""
        
        if input_text:
            prompt += f"\n**Input**: {input_text}\n"
        
        prompt += "\n**Output**:"
        
        print(f"\n📝 Prompt:\n{prompt}\n")
        print("⏳ Generating...")
        
        # Tokenize
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            truncation=True,
            max_length=512
        ).to(self.model.device)
        
        # Generation config
        gen_config = GenerationConfig(
            max_length=max_length,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            num_return_sequences=num_return_sequences,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                generation_config=gen_config
            )
        
        # Decode
        generated_text = self.tokenizer.decode(
            outputs[0],
            skip_special_tokens=True
        )
        
        # Extract only the generated part (after prompt)
        response = generated_text[len(prompt):].strip()
        
        return response
    
    def interactive_mode(self):
        """Interactive mode for testing"""
        print("\n" + "=" * 70)
        print("INTERACTIVE FLUTTER CODE GENERATION")
        print("=" * 70)
        print("\nType 'quit' to exit\n")
        
        while True:
            try:
                instruction = input("\n💡 Enter your instruction: ").strip()
                
                if instruction.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not instruction:
                    continue
                
                # Generate
                response = self.generate_code(
                    instruction=instruction,
                    temperature=0.7,
                    max_length=2048
                )
                
                print("\n" + "=" * 70)
                print("GENERATED OUTPUT:")
                print("=" * 70)
                print(response)
                print("=" * 70)
                
                # Ask if user wants to save
                save = input("\n💾 Save output? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Enter filename (e.g., output.json): ").strip()
                    with open(filename, 'w') as f:
                        # Try to parse as JSON, otherwise save as text
                        try:
                            parsed = json.loads(response)
                            json.dump(parsed, f, indent=2)
                        except:
                            f.write(response)
                    print(f"✓ Saved to {filename}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Flutter Code Generator")
    parser.add_argument(
        "--model_path",
        type=str,
        default="./outputs/dpo_model",
        help="Path to fine-tuned model"
    )
    parser.add_argument(
        "--instruction",
        type=str,
        default=None,
        help="Instruction for code generation"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Sampling temperature"
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=2048,
        help="Maximum generation length"
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = FlutterCodeGenerator(args.model_path)
    
    if args.interactive or args.instruction is None:
        # Interactive mode
        generator.interactive_mode()
    else:
        # Single generation
        response = generator.generate_code(
            instruction=args.instruction,
            temperature=args.temperature,
            max_length=args.max_length
        )
        
        print("\n" + "=" * 70)
        print("GENERATED OUTPUT:")
        print("=" * 70)
        print(response)
        print("=" * 70)


if __name__ == "__main__":
    # Example usage
    print("=" * 70)
    print("FLUTTER CODE GENERATOR - INFERENCE")
    print("=" * 70)
    
    # Example 1: Direct generation
    print("\n📝 Example 1: Direct Generation\n")
    
    generator = FlutterCodeGenerator("./outputs/dpo_model")
    
    response = generator.generate_code(
        instruction="Create a simple Flutter counter app with Provider state management",
        framework="Flutter 3.0+",
        architecture="Clean Architecture",
        temperature=0.7
    )
    
    print("\n" + "=" * 70)
    print("GENERATED OUTPUT:")
    print("=" * 70)
    print(response[:500] + "..." if len(response) > 500 else response)
    print("=" * 70)
    
    # Example 2: Interactive mode
    print("\n\n📝 Starting Interactive Mode...\n")
    generator.interactive_mode()
