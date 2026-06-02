#!/bin/bash
# Vext Audit Capital - Automated Droplet Setup Script (with Auto-Swap Protection)
# Designed to build and run backend agents with zero manual terminal commands.

# Exit immediately if any command fails
set -e

echo "======================================================================"
echo "🚀 STARTING AUTOMATED VEXT AUDIT SERVER PROVISIONING..."
echo "======================================================================"

# 1. Proactive Memory Protection: Configure 2GB Swap Space (Virtual RAM)
# This prevents Out-Of-Memory (OOM) crashes on 1GB RAM plans during PDF generation.
echo "🧠 [1/7] Configuring 2GB virtual memory swap space..."
if [ ! -f /swapfile ]; then
    sudo fallocate -l 2G /swapfile
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swap space configured successfully."
else
    echo "ℹ️ Swap space already configured."
fi

# 2. Update and Upgrade Packages
echo "🔄 [2/7] Updating Ubuntu system packages..."
sudo apt update && sudo apt upgrade -y

# 3. Install Core System Dependencies
echo "📦 [3/7] Installing Python, Node.js, NPM, Git, and Build utilities..."
sudo apt install python3-pip python3-venv python3-dev build-essential git nodejs npm -y

# 4. Install PM2 Globally
echo "⚙️ [4/7] Installing PM2 process manager globally..."
sudo npm install -g pm2

# 5. Set Up Python Virtual Environment
echo "🐍 [5/7] Creating isolated Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 6. Install Python Packages
echo "📥 [6/7] Upgrading pip and installing required Python libraries..."
pip install --upgrade pip
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    echo "⚠️ Warning: requirements.txt not found. Installing core modules manually..."
    pip install google-generativeai pydantic pydantic-settings requests python-dotenv
fi

# 7. Initialize Logs and Start PM2
echo "📁 [7/7] Creating log directories and starting background agents..."
mkdir -p logs

if [ -f ecosystem.config.js ]; then
    echo "⚡ PM2 ecosystem configuration detected. Starting agents orchestrator..."
    pm2 start ecosystem.config.js
    
    # Save PM2 state and configure it to boot automatically when the server restarts
    echo "🛡️ Configuring PM2 to automatically restart on server reboot..."
    pm2 save
    
    # Automate the PM2 startup service configuration
    sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u root --hp /root || true
    pm2 save
else
    echo "⚠️ Warning: ecosystem.config.js not found. Skipping initial PM2 boot."
fi

echo "======================================================================"
echo "🎉 SERVER PROVISIONING COMPLETE!"
echo "----------------------------------------------------------------------"
echo "Your Python background agents are now running and managed by PM2."
echo "Useful Commands:"
echo "  - View live status:  pm2 status"
echo "  - View live logs:    pm2 logs"
echo "  - Restart agents:    pm2 restart vext-agents-orchestrator"
echo "======================================================================"
