#!/bin/bash
# Development commands for AFD Backend API

IMAGE_NAME="afd-api"
CONTAINER_NAME="afd-api"

echo "🐍 AFD Backend API - Development Commands"
echo "========================================"

case "$1" in
  "build")
    echo "🔨 Building Backend Docker image..."
    docker build -t $IMAGE_NAME:latest .
    echo "✅ Build completed!"
    ;;
    
  "run")
    echo "🚀 Running backend container locally..."
    docker stop $CONTAINER_NAME 2>/dev/null || true
    docker rm $CONTAINER_NAME 2>/dev/null || true
    docker run -d -p 8000:8000 -v $(pwd)/data:/app/data:rw --name $CONTAINER_NAME $IMAGE_NAME:latest
    echo "✅ Backend started at: http://localhost:8000"
    echo "📚 API docs at: http://localhost:8000/docs"
    ;;
    
  "dev")
    echo "🔧 Starting development server..."
    if [ -f "requirements.txt" ]; then
      pip install -r requirements.txt
    fi
    uvicorn app.api:app --host 0.0.0.0 --port 8000 --reload
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
    echo "🔍 Health check:"
    curl -f http://localhost:8000/health 2>/dev/null && echo "✅ Healthy" || echo "❌ Not responding"
    echo ""
    echo "📚 API Documentation:"
    echo "http://localhost:8000/docs"
    ;;
    
  "clean")
    echo "🧹 Cleaning Docker resources..."
    docker system prune -f
    docker image prune -f
    echo "✅ Cleanup completed"
    ;;
    
  "test")
    echo "🧪 Testing API endpoints..."
    echo "Root endpoint:"
    curl -s http://localhost:8000/ | head -3
    echo ""
    echo "Health endpoint:"
    curl -s http://localhost:8000/health 2>/dev/null || echo "Health endpoint not available"
    echo ""
    echo "Automata endpoint:"
    curl -s http://localhost:8000/automata | head -3
    ;;
    
  "compose-up")
    echo "🚀 Starting with Docker Compose..."
    docker-compose up -d
    echo "✅ Backend started with compose"
    ;;
    
  "compose-down")
    echo "🛑 Stopping Docker Compose..."
    docker-compose down
    ;;
    
  "compose-logs")
    echo "📋 Showing Docker Compose logs..."
    docker-compose logs -f
    ;;
    
  "test-deploy")
    echo "🧪 Testing complete deployment..."
    echo "1️⃣ Building image..."
    docker build -t $IMAGE_NAME:latest .
    
    echo "2️⃣ Saving image..."
    docker save $IMAGE_NAME:latest > backend-image.tar
    
    echo "3️⃣ Loading image..."
    docker load < backend-image.tar
    
    echo "4️⃣ Starting with production compose..."
    docker-compose -f docker-compose.prod.yml up -d
    
    echo "5️⃣ Testing health..."
    sleep 10
    if curl -f http://localhost:8000/ > /dev/null 2>&1; then
      echo "✅ Deployment test successful!"
      echo "📚 API docs: http://localhost:8000/docs"
    else
      echo "❌ Deployment test failed"
    fi
    
    rm backend-image.tar
    ;;
    
  *)
    echo ""
    echo "Available commands:"
    echo "  build         - Build Docker image"
    echo "  run           - Run container locally"
    echo "  dev           - Start development server (uvicorn)"
    echo "  logs          - Show container logs"
    echo "  stop          - Stop and remove container"
    echo "  status        - Show container status and health"
    echo "  clean         - Clean Docker resources"
    echo "  test          - Test API endpoints"
    echo "  compose-up    - Start with Docker Compose"
    echo "  compose-down  - Stop Docker Compose"
    echo "  compose-logs  - Show Compose logs"
    echo "  test-deploy   - Test complete deployment flow"
    echo ""
    echo "Examples:"
    echo "  ./backend-commands.sh build && ./backend-commands.sh run"
    echo "  ./backend-commands.sh dev"
    echo "  ./backend-commands.sh test-deploy"
    ;;
esac