#!/bin/bash
# Development commands for Automatas AFD Frontend

IMAGE_NAME="automatas-afd-frontend"
CONTAINER_NAME="automatas-afd-frontend"

echo "🐳 Automatas AFD Frontend - Development Commands"
echo "================================================"

case "$1" in
  "build")
    echo "🔨 Building Docker image..."
    docker build -t $IMAGE_NAME:latest .
    echo "✅ Build completed!"
    ;;
    
  "run")
    echo "🚀 Running container locally..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    docker run -d -p 80:80 --name $CONTAINER_NAME $IMAGE_NAME:latest
    echo "✅ Container started at: http://localhost"
    ;;
    
  "dev")
    echo "🔧 Starting development server..."
    npm run dev
    ;;
    
  "logs")
    echo "📋 Showing container logs..."
    docker logs -f $CONTAINER_NAME
    ;;
    
  "stop")
    echo "🛑 Stopping container..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    echo "✅ Container stopped"
    ;;
    
  "status")
    echo "📊 Container status:"
    docker ps --filter name=$CONTAINER_NAME
    echo ""
    echo "� Health check:"
    curl -f http://localhost/health 2>/dev/null && echo "✅ Healthy" || echo "❌ Not responding"
    ;;
    
  "clean")
    echo "🧹 Cleaning Docker resources..."
    docker system prune -f
    docker image prune -f
    echo "✅ Cleanup completed"
    ;;
    
  "test-build")
    echo "🧪 Testing build process..."
    npm ci
    npm run build
    echo "✅ Build test completed"
    ;;
    
  "test-deploy")
    echo "🧪 Testing complete deployment..."
    echo "1️⃣ Building image..."
    docker build -t $IMAGE_NAME:latest .
    
    echo "2️⃣ Saving image..."
    docker save $IMAGE_NAME:latest > frontend-image.tar
    
    echo "3️⃣ Loading image..."
    docker load < frontend-image.tar
    
    echo "4️⃣ Starting with compose..."
    docker-compose up -d
    
    echo "5️⃣ Testing health..."
    sleep 5
    if curl -f http://localhost/ > /dev/null 2>&1; then
      echo "✅ Deployment test successful!"
    else
      echo "❌ Deployment test failed"
    fi
    
    rm frontend-image.tar
    ;;
    
  *)
    echo ""
    echo "Available commands:"
    echo "  build       - Build Docker image"
    echo "  run         - Run container locally"
    echo "  dev         - Start development server"
    echo "  logs        - Show container logs"
    echo "  stop        - Stop and remove container"
    echo "  status      - Show container status and health"
    echo "  clean       - Clean Docker resources"
    echo "  test-build  - Test npm build process"
    echo "  test-deploy - Test complete deployment flow"
    echo ""
    echo "Examples:"
    echo "  ./dev-commands.sh build && ./dev-commands.sh run"
    echo "  ./dev-commands.sh test-deploy"
    ;;
esac