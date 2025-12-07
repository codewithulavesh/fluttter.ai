"""
Dataset Preparation for Fine-tuning
Converts the Flutter code dataset into formats suitable for:
1. Supervised Fine-Tuning (SFT)
2. Reinforcement Learning (RLHF/DPO)
"""

import json
import pandas as pd
from datasets import Dataset, DatasetDict
from typing import List, Dict, Any
import random


class DatasetPreparator:
    def __init__(self, data_path: str):
        """Initialize with path to data.json"""
        with open(data_path, 'r') as f:
            self.raw_data = json.load(f)
        
        print(f"✓ Loaded {len(self.raw_data)} datasets")
    
    def prepare_sft_dataset(self) -> Dataset:
        """
        Prepare dataset for Supervised Fine-Tuning
        Format: instruction -> response pairs
        """
        examples = []
        
        for dataset in self.raw_data:
            dataset_name = dataset.get('dataset_name', 'unknown')
            metadata = dataset.get('metadata', {})
            instructions = dataset.get('instructions', [])
            
            for inst in instructions:
                instruction = inst.get('instruction', '')
                input_text = inst.get('input', '')
                output = inst.get('output', {})
                
                # Convert output to formatted string
                output_str = json.dumps(output, indent=2)
                
                # Create prompt in chat format
                prompt = self._format_prompt(instruction, input_text, metadata)
                
                examples.append({
                    'prompt': prompt,
                    'completion': output_str,
                    'dataset_name': dataset_name,
                    'metadata': json.dumps(metadata)
                })
        
        print(f"✓ Created {len(examples)} training examples")
        return Dataset.from_list(examples)
    
    def prepare_chat_format(self) -> Dataset:
        """
        Prepare dataset in chat/conversation format
        Suitable for models like Llama, Mistral, etc.
        """
        examples = []
        
        for dataset in self.raw_data:
            dataset_name = dataset.get('dataset_name', '')
            metadata = dataset.get('metadata', {})
            instructions = dataset.get('instructions', [])
            
            for inst in instructions:
                instruction = inst.get('instruction', '')
                input_text = inst.get('input', '')
                output = inst.get('output', {})
                
                # Create conversation format
                messages = [
                    {
                        "role": "system",
                        "content": f"You are an expert Flutter developer. You create professional, production-ready Flutter applications following clean architecture principles. Framework: {metadata.get('framework', 'Flutter')}, Architecture: {metadata.get('architecture', 'Clean Architecture')}"
                    },
                    {
                        "role": "user",
                        "content": instruction + (f"\n\nInput: {input_text}" if input_text else "")
                    },
                    {
                        "role": "assistant",
                        "content": json.dumps(output, indent=2)
                    }
                ]
                
                examples.append({
                    'messages': messages,
                    'dataset_name': dataset_name
                })
        
        print(f"✓ Created {len(examples)} chat examples")
        return Dataset.from_list(examples)
    
    def prepare_dpo_dataset(self, num_negatives: int = 1) -> Dataset:
        """
        Prepare dataset for Direct Preference Optimization (DPO)
        Creates chosen/rejected pairs for preference learning
        """
        examples = []
        
        for dataset in self.raw_data:
            dataset_name = dataset.get('dataset_name', '')
            metadata = dataset.get('metadata', {})
            instructions = dataset.get('instructions', [])
            
            for inst in instructions:
                instruction = inst.get('instruction', '')
                input_text = inst.get('input', '')
                output = inst.get('output', {})
                
                prompt = self._format_prompt(instruction, input_text, metadata)
                chosen = json.dumps(output, indent=2)
                
                # Generate negative examples (simplified versions or incomplete)
                for _ in range(num_negatives):
                    rejected = self._generate_negative_example(output)
                    
                    examples.append({
                        'prompt': prompt,
                        'chosen': chosen,
                        'rejected': rejected,
                        'dataset_name': dataset_name
                    })
        
        print(f"✓ Created {len(examples)} DPO preference pairs")
        return Dataset.from_list(examples)
    
    def _format_prompt(self, instruction: str, input_text: str, metadata: Dict) -> str:
        """Format instruction into a prompt"""
        framework = metadata.get('framework', 'Flutter')
        architecture = metadata.get('architecture', 'Clean Architecture')
        
        prompt = f"""### Task: Flutter Application Development

**Framework**: {framework}
**Architecture**: {architecture}

**Instruction**: {instruction}
"""
        
        if input_text:
            prompt += f"\n**Input**: {input_text}\n"
        
        prompt += "\n**Output**:"
        
        return prompt
    
    def _generate_negative_example(self, correct_output: Dict) -> str:
        """
        Generate a negative example for DPO training
        This creates intentionally worse outputs for preference learning
        """
        # Strategy: Remove some keys or simplify the structure
        if isinstance(correct_output, dict):
            # Create a simplified version
            negative = {}
            keys = list(correct_output.keys())
            
            # Randomly remove 30-50% of keys
            num_to_keep = max(1, int(len(keys) * random.uniform(0.5, 0.7)))
            keys_to_keep = random.sample(keys, num_to_keep)
            
            for key in keys_to_keep:
                value = correct_output[key]
                if isinstance(value, dict):
                    # Simplify nested dicts
                    negative[key] = {k: "..." for k in list(value.keys())[:2]}
                elif isinstance(value, list) and len(value) > 0:
                    # Truncate lists
                    negative[key] = value[:1]
                else:
                    negative[key] = value
            
            return json.dumps(negative, indent=2)
        
        return "{}"
    
    def split_dataset(self, dataset: Dataset, train_size: float = 0.9) -> DatasetDict:
        """Split dataset into train/validation sets"""
        split = dataset.train_test_split(test_size=1-train_size, seed=42)
        
        dataset_dict = DatasetDict({
            'train': split['train'],
            'validation': split['test']
        })
        
        print(f"✓ Split: {len(dataset_dict['train'])} train, {len(dataset_dict['validation'])} validation")
        return dataset_dict
    
    def save_datasets(self, output_dir: str = './processed_data'):
        """Save all prepared datasets"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # 1. SFT Dataset
        print("\n📦 Preparing SFT dataset...")
        sft_dataset = self.prepare_sft_dataset()
        sft_split = self.split_dataset(sft_dataset)
        sft_split.save_to_disk(f"{output_dir}/sft_dataset")
        print(f"✓ Saved to {output_dir}/sft_dataset")
        
        # 2. Chat Format Dataset
        print("\n📦 Preparing Chat format dataset...")
        chat_dataset = self.prepare_chat_format()
        chat_split = self.split_dataset(chat_dataset)
        chat_split.save_to_disk(f"{output_dir}/chat_dataset")
        print(f"✓ Saved to {output_dir}/chat_dataset")
        
        # 3. DPO Dataset
        print("\n📦 Preparing DPO dataset...")
        dpo_dataset = self.prepare_dpo_dataset(num_negatives=2)
        dpo_split = self.split_dataset(dpo_dataset)
        dpo_split.save_to_disk(f"{output_dir}/dpo_dataset")
        print(f"✓ Saved to {output_dir}/dpo_dataset")
        
        print(f"\n✅ All datasets saved to {output_dir}/")
        
        return {
            'sft': sft_split,
            'chat': chat_split,
            'dpo': dpo_split
        }


def main():
    """Main execution"""
    print("=" * 70)
    print("DATASET PREPARATION FOR FINE-TUNING")
    print("=" * 70)
    
    # Initialize preparator
    preparator = DatasetPreparator('data.json')
    
    # Prepare and save all datasets
    datasets = preparator.save_datasets()
    
    # Print statistics
    print("\n" + "=" * 70)
    print("DATASET STATISTICS")
    print("=" * 70)
    
    for name, dataset_dict in datasets.items():
        print(f"\n{name.upper()} Dataset:")
        print(f"  Train: {len(dataset_dict['train'])} examples")
        print(f"  Validation: {len(dataset_dict['validation'])} examples")
        print(f"  Columns: {dataset_dict['train'].column_names}")
    
    print("\n✅ Dataset preparation complete!")
    print("Next steps:")
    print("  1. Run: python train_sft.py (for supervised fine-tuning)")
    print("  2. Run: python train_dpo.py (for reinforcement learning)")


if __name__ == "__main__":
    main()
