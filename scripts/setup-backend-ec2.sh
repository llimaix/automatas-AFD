#!/bin/bash
# Setup script for EC2 server - AFD Backend API

set -e

echo "🚀 Setting up EC2 server for AFD Backend API..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo "📦 Installing essential packages..."
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release wget

# Install Docker
echo "🐳 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt update
    sudo apt install -y docker-ce docker-ce-cli containerd.io
    
    # Start and enable Docker
    sudo systemctl start docker
    sudo systemctl enable docker
    
    # Add user to docker group
    sudo usermod -aG docker $USER
    echo "⚠️  Please log out and back in for Docker group changes to take effect"
else
    echo "✅ Docker already installed"
fi

# Install Docker Compose
echo "🐳 Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose
else
    echo "✅ Docker Compose already installed"
fi

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 8000/tcp  # Backend API port
sudo ufw --force enable

# Create app directory
echo "📁 Creating application directory..."
mkdir -p ~/afd-backend/data
cd ~/afd-backend

# Create a simple API status page
echo "📄 Creating temporary API status page..."
cat > api-status.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AFD Backend API - Server Ready</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: system-ui, sans-serif;
            background: linear-gradient(135deg, #1e40af, #3b82f6);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .container { max-width: 600px; padding: 2rem; }
        h1 { font-size: 2.5rem; margin-bottom: 1rem; }
        .emoji { font-size: 4rem; margin-bottom: 1rem; }
        p { font-size: 1.2rem; margin-bottom: 1rem; opacity: 0.9; }
        .status { 
            background: rgba(255,255,255,0.1);
            padding: 1.5rem;
            border-radius: 12px;
            margin-top: 2rem;
        }
        .check { color: #10b981; font-weight: bold; }
        .endpoint { 
            background: rgba(0,0,0,0.2);
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="emoji">🤖</div>
        <h1>AFD Backend API</h1>
        <p>Autómatas Finitos Deterministas - API Server</p>
        <div class="status">
            <p class="check">✅ Server configured and ready</p>
            <p class="check">✅ Docker installed and running</p>
            <p class="check">✅ Port 8000 configured</p>
            <p>⏳ Waiting for first API deployment...</p>
        </div>
        <div class="endpoint">
            <p>🔗 API will be available at port 8000</p>
            <p>📚 Documentation at /docs</p>
        </div>
    </div>
</body>
</html>
EOF

# Start a temporary server on port 8000
echo "🚀 Starting temporary API server..."
docker run -d --name temp-api-server -p 8000:80 -v $(pwd)/api-status.html:/usr/share/nginx/html/index.html:ro nginx:alpine

# Setup cleanup cron job
echo "🧹 Setting up cleanup job..."
(crontab -l 2>/dev/null; echo "0 2 * * 0 docker system prune -f") | crontab -

# Display information
echo ""
echo "✅ Backend setup completed successfully!"
echo ""
echo "🔧 System Information:"
echo "   Docker: $(docker --version)"
echo "   Docker Compose: $(docker-compose --version)"
echo ""
echo "🌐 Your backend server is ready at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || hostname -I | awk '{print $1}'):8000"
echo ""
echo "📋 Next steps:"
echo "1. Configure GitHub Secrets:"
echo "   - EC2_HOST: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 2>/dev/null || hostname -I | awk '{print $1}')"
echo "   - EC2_USER: $USER"
echo "   - EC2_SSH_KEY: (your private SSH key)"
echo ""
echo "2. Push to your repository to trigger backend deployment"
echo ""
echo "⚠️  Remember to log out and back in for Docker group permissions"