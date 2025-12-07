#!/bin/bash

# Flutter Code Generation - Training Pipeline
# Quick start script for the complete training workflow

set -e  # Exit on error

echo "=========================================================================="
echo "FLUTTER CODE GENERATION - TRAINING PIPELINE"
echo "=========================================================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if data.json exists
if [ ! -f "data.json" ]; then
    print_error "data.json not found!"
    exit 1
fi

print_success "Found data.json"

# Step 1: Install dependencies
print_step "Installing dependencies..."
if command -v pip3 &> /dev/null; then
    pip3 install -r requirements.txt
else
    pip install -r requirements.txt
fi
print_success "Dependencies installed"

# Step 2: Prepare datasets
print_step "Preparing datasets..."
python3 prepare_dataset.py
print_success "Datasets prepared"

# Step 3: Ask user what to do
echo ""
echo "=========================================================================="
echo "TRAINING OPTIONS"
echo "=========================================================================="
echo "1) Run Supervised Fine-Tuning (SFT) only"
echo "2) Run SFT + DPO (Full pipeline)"
echo "3) Run DPO only (requires existing SFT model)"
echo "4) Skip training, just prepare data"
echo ""
read -p "Select option (1-4): " option

case $option in
    1)
        print_step "Starting Supervised Fine-Tuning..."
        python3 train_sft.py
        print_success "SFT training complete!"
        ;;
    2)
        print_step "Starting Supervised Fine-Tuning..."
        python3 train_sft.py
        print_success "SFT training complete!"
        
        echo ""
        print_step "Starting DPO training..."
        python3 train_dpo.py
        print_success "DPO training complete!"
        ;;
    3)
        if [ ! -d "./outputs/sft_model" ]; then
            print_error "SFT model not found! Please run SFT first."
            exit 1
        fi
        
        print_step "Starting DPO training..."
        python3 train_dpo.py
        print_success "DPO training complete!"
        ;;
    4)
        print_success "Data preparation complete! You can now run training manually."
        ;;
    *)
        print_error "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "=========================================================================="
echo "TRAINING COMPLETE!"
echo "=========================================================================="
echo ""
echo "Next steps:"
echo "  1. Test your model: python3 inference.py --interactive"
echo "  2. View training logs in WandB or TensorBoard"
echo "  3. Check model outputs in ./outputs/"
echo ""
print_success "All done! 🎉"
