#!/bin/bash

# 🐳 Deploy Script - Agente de Vendas (Otimizado)
set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print() { echo -e "${2}${1}${NC}"; }

# Verificações básicas
check_docker() {
    if ! command -v docker >/dev/null 2>&1; then
        print "❌ Docker não instalado!" "$RED"
        exit 1
    fi
    if ! command -v docker-compose >/dev/null 2>&1; then
        print "❌ Docker Compose não instalado!" "$RED"
        exit 1
    fi
}

# Setup mínimo
setup() {
    print "⚙️ Configurando..." "$BLUE"
    mkdir -p logs
    [ ! -f ".env" ] && [ -f "env.example" ] && cp env.example .env
    [ ! -f "token.json" ] && echo '{}' > token.json
}

# Deploy
deploy() {
    print "🚀 Fazendo deploy..." "$BLUE"
    check_docker
    setup
    
    # Parar containers existentes
    docker-compose down 2>/dev/null || true
    
    # Build e start
    docker-compose build --no-cache
    docker-compose up -d
    
    # Aguardar aplicação
    print "⏳ Aguardando aplicação..." "$YELLOW"
    for i in {1..15}; do
        if curl -s http://localhost:8081/api/data >/dev/null 2>&1; then
            print "✅ Aplicação funcionando!" "$GREEN"
            print "🌐 http://localhost:8081" "$GREEN"
            return 0
        fi
        sleep 2
    done
    
    print "❌ Aplicação não respondeu" "$RED"
    docker-compose logs app
    exit 1
}

# Comandos
case "${1:-deploy}" in
    "deploy") deploy ;;
    "stop") docker-compose down ;;
    "restart") docker-compose restart ;;
    "logs") docker-compose logs -f app ;;
    "status") docker-compose ps ;;
    "clean") docker-compose down -v && docker system prune -f ;;
    "help") 
        print "Comandos: deploy, stop, restart, logs, status, clean" "$BLUE"
        ;;
    *) print "Comando desconhecido: $1" "$RED" && exit 1 ;;
esac
