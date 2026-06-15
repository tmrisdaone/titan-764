#!/data/data/com.termux/files/usr/bin/bash
# TITAN-7 ARM64 Termux Setup Script
# Run this once to provision your phone's environment.

set -e

echo "🚀 Provisioning TITAN-7 ARM64 Environment..."

# 1. Update and install core dependencies
pkg update -y
pkg install -y python termux-api openssl

# 2. Grant Termux API permissions (opens Android settings)
echo "⚠️ Please grant 'termux-api' permissions in the Android pop-up."
termux-setup-storage

# 3. Install Python dependencies for the brain
pip install --upgrade pip
pip install pyserial requests

# 4. Check Ollama installation
if ! command -v ollama &> /dev/null; then
    echo "⚠️ Ollama not found. Install it via:"
    echo "   curl -fsSL https://ollama.com/install.sh | sh"
    echo "   (Note: On Android/Termux, you may need to use a proot-distro Ubuntu environment for Ollama)"
else
    echo "✅ Ollama detected."
fi

# 5. Pull the lightweight model
echo "📥 Downloading Qwen 0.5B model (this may take a few minutes)..."
ollama pull qwen2:0.5b

echo "✅ Setup complete! Connect your ESP32 via USB OTG and run:"
echo "   python3 brain/main.py"
