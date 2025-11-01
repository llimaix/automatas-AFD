# 🚀 Deployment Guide - Automatas AFD Frontend

Simple and robust deployment setup for your React frontend using Docker and GitHub Actions.

## 🎯 Quick Start

### 1. Server Setup (One-time)

Connect to your EC2 server and run:

```bash
ssh -i your-key.pem ubuntu@your-server-ip

# Download and run setup script
wget https://raw.githubusercontent.com/llimaix/automatas-AFD/main/scripts/setup-ec2.sh
chmod +x setup-ec2.sh
./setup-ec2.sh

# Log out and back in for Docker permissions
exit
ssh -i your-key.pem ubuntu@your-server-ip
```

### 2. GitHub Secrets

Add these secrets in your GitHub repository (Settings → Secrets → Actions):

| Secret | Value | Example |
|--------|-------|---------|
| `EC2_HOST` | Your server IP | `54.123.456.789` |
| `EC2_USER` | SSH username | `ubuntu` |
| `EC2_SSH_KEY` | Private SSH key content | `-----BEGIN RSA...` |

### 3. Deploy

Push to `main` or `front` branch → Automatic deployment! 🎉

## 📁 Project Structure

```
├── Dockerfile              # Multi-stage build
├── docker-compose.yml      # Production container config
├── nginx.conf              # Nginx configuration
├── .github/workflows/      
│   └── deploy.yml          # Deployment workflow
├── scripts/
│   └── setup-ec2.sh        # Server setup script
└── dev-commands.sh         # Development utilities
```

## 🛠️ Development Commands

```bash
# Build and test locally
./dev-commands.sh build
./dev-commands.sh run

# Development server
./dev-commands.sh dev

# View logs
./dev-commands.sh logs

# Test complete deployment flow
./dev-commands.sh test-deploy

# Clean up resources
./dev-commands.sh clean
```

## 🔍 Monitoring & Troubleshooting

### Check deployment status:
```bash
# On server
docker ps
docker logs automatas-afd-frontend

# Health check
curl http://localhost/health
```

### Common issues:

**Container not starting:**
```bash
docker logs automatas-afd-frontend
docker-compose up -d
```

**Port 80 busy:**
```bash
sudo netstat -tulpn | grep :80
docker stop $(docker ps -q --filter "publish=80")
```

**Permission denied:**
```bash
sudo usermod -aG docker $USER
# Log out and back in
```

## 🚀 Deployment Flow

1. **Push** → GitHub Actions triggered
2. **Build** → Docker image created
3. **Transfer** → Image sent to server
4. **Deploy** → Old container stopped, new started
5. **Verify** → Health checks performed
6. **Cleanup** → Old images removed

## 🔐 Security Features

- ✅ No source code on server
- ✅ Containerized isolation  
- ✅ Security headers configured
- ✅ Minimal attack surface
- ✅ Automated updates

## 📊 Performance Features

- ✅ Multi-stage Docker build
- ✅ Gzip compression
- ✅ Static asset caching
- ✅ Health monitoring
- ✅ Zero-downtime deployments

## 🎛️ Configuration

### Environment Variables
Configure in `docker-compose.yml`:
```yaml
environment:
  - NODE_ENV=production
  - API_URL=https://api.example.com  # Add as needed
```

### Nginx Tuning
Modify `nginx.conf` for custom:
- Cache policies
- Security headers  
- Rate limiting
- SSL termination

## 🆘 Support

1. **GitHub Actions logs** - Check workflow execution
2. **Container logs** - `docker logs automatas-afd-frontend`
3. **Nginx logs** - `/var/log/nginx/` on server
4. **Health endpoint** - `http://your-server/health`

---

**🎉 That's it! Your app deploys automatically on every push.**