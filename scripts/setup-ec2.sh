#!/bin/bash
# Script para configurar servidor EC2 con Docker para el despliegue del frontend
# Ejecuta este script una vez en tu servidor EC2

echo "🚀 Configurando servidor EC2 con Docker para Automatas AFD Frontend..."

# Actualizar sistema
echo "📦 Actualizando paquetes del sistema..."
sudo apt update && sudo apt upgrade -y

# Instalar dependencias básicas
echo "📦 Instalando dependencias básicas..."
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release wget

# Instalar Docker
echo "� Instalando Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Iniciar y habilitar Docker
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario al grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
echo "� Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear enlace simbólico
sudo ln -sf /usr/local/bin/docker-compose /usr/bin/docker-compose

# Verificar instalación
echo "✅ Verificando instalación..."
docker --version
docker-compose --version

# Configurar firewall
echo "🔥 Configurando firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw --force enable

# Crear directorio para la aplicación
echo "📁 Creando directorios..."
mkdir -p ~/automatas-afd
cd ~/automatas-afd

# Crear página de mantenimiento temporal con Docker
echo "📄 Creando contenedor temporal..."
cat > docker-compose.temp.yml << 'EOF'
version: '3.8'
services:
  temp-page:
    image: nginx:alpine
    container_name: temp-automatas-page
    ports:
      - "80:80"
    volumes:
      - ./temp-html:/usr/share/nginx/html:ro
    restart: unless-stopped
EOF

# Crear página HTML temporal
mkdir -p temp-html
cat > temp-html/index.html << 'EOF'
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Automatas AFD - Servidor Listo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
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
        .docker-info {
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
        <div class="emoji">🐳</div>
        <h1>Automatas AFD</h1>
        <p>Reconocedor de Palabras con Autómatas Finitos Deterministas</p>
        <div class="status">
            <p class="check">✅ Servidor EC2 configurado correctamente</p>
            <p class="check">✅ Docker instalado y funcionando</p>
            <p class="check">✅ Docker Compose configurado</p>
            <p>⏳ Esperando primer despliegue desde GitHub Actions...</p>
        </div>
        <div class="docker-info">
            <p>🐳 Contenedor temporal ejecutándose</p>
            <p>🚀 Listo para recibir despliegues automáticos</p>
        </div>
    </div>
</body>
</html>
EOF

# Iniciar contenedor temporal
echo "🚀 Iniciando contenedor temporal..."
docker-compose -f docker-compose.temp.yml up -d

# Configurar limpieza automática de Docker
echo "🧹 Configurando limpieza automática de Docker..."
(crontab -l 2>/dev/null; echo "0 2 * * 0 docker system prune -f") | crontab -

# Mostrar información del servidor
echo ""
echo "✅ ¡Configuración completada!"
echo "🌐 Tu servidor está listo en: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo ""
echo "📋 Información del servidor:"
echo "🐳 Docker version: $(docker --version)"
echo "🐳 Docker Compose version: $(docker-compose --version)"
echo ""
echo "🔧 Estado de los servicios:"
sudo systemctl status docker --no-pager -l
echo ""
echo "📦 Contenedores en ejecución:"
docker ps
echo ""
echo "📋 Próximos pasos:"
echo "1. Configura los secrets en GitHub:"
echo "   - EC2_HOST: $(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)"
echo "   - EC2_USER: ubuntu (o tu usuario)"
echo "   - EC2_SSH_KEY: tu clave privada SSH"
echo "   - EC2_PORT: 22 (opcional)"
echo ""
echo "2. Haz push a tu repositorio para activar el deployment"
echo ""
echo "⚠️ IMPORTANTE: Cierra esta sesión SSH y vuelve a conectarte para que los cambios de grupo (docker) tomen efecto"