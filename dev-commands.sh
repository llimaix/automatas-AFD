#!/bin/bash
# Script de comandos útiles para desarrollo local

echo "🐳 Comandos útiles para Automatas AFD Frontend"
echo "=============================================="

case "$1" in
  "build")
    echo "🔨 Construyendo imagen Docker..."
    docker build -t automatas-afd-frontend:latest .
    ;;
  "run")
    echo "🚀 Ejecutando contenedor localmente..."
    docker run -d -p 80:80 --name automatas-afd-frontend automatas-afd-frontend:latest
    echo "✅ Aplicación disponible en: http://localhost"
    ;;
  "dev")
    echo "🔧 Iniciando servidor de desarrollo..."
    npm run dev
    ;;
  "logs")
    echo "📋 Mostrando logs del contenedor..."
    docker logs -f automatas-afd-frontend
    ;;
  "stop")
    echo "🛑 Deteniendo contenedor..."
    docker stop automatas-afd-frontend
    docker rm automatas-afd-frontend
    ;;
  "clean")
    echo "🧹 Limpiando recursos Docker..."
    docker system prune -f
    docker image prune -f
    ;;
  "compose-up")
    echo "🚀 Iniciando con Docker Compose..."
    docker-compose up -d
    echo "✅ Aplicación disponible en: http://localhost"
    ;;
  "compose-down")
    echo "🛑 Deteniendo Docker Compose..."
    docker-compose down
    ;;
  "compose-logs")
    echo "📋 Mostrando logs de Docker Compose..."
    docker-compose logs -f
    ;;
  "test-build")
    echo "🧪 Probando build completo..."
    npm ci
    npm run build
    echo "✅ Build completado exitosamente"
    ;;
  *)
    echo ""
    echo "Comandos disponibles:"
    echo "  ./dev-commands.sh build         - Construir imagen Docker"
    echo "  ./dev-commands.sh run           - Ejecutar contenedor"
    echo "  ./dev-commands.sh dev           - Servidor de desarrollo"
    echo "  ./dev-commands.sh logs          - Ver logs del contenedor"
    echo "  ./dev-commands.sh stop          - Detener contenedor"
    echo "  ./dev-commands.sh clean         - Limpiar recursos Docker"
    echo "  ./dev-commands.sh compose-up    - Iniciar con Docker Compose"
    echo "  ./dev-commands.sh compose-down  - Detener Docker Compose"
    echo "  ./dev-commands.sh compose-logs  - Ver logs de Compose"
    echo "  ./dev-commands.sh test-build    - Probar build local"
    echo ""
    echo "Ejemplos:"
    echo "  ./dev-commands.sh build && ./dev-commands.sh run"
    echo "  ./dev-commands.sh compose-up"
    ;;
esac