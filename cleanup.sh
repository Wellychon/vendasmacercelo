#!/bin/bash

# 🧹 Script de Limpeza - Agente de Vendas
set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print() { echo -e "${2}${1}${NC}"; }

# Limpeza completa
full_cleanup() {
    print "🧹 Limpeza completa..." "$BLUE"
    
    # Parar containers
    docker-compose down 2>/dev/null || true
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Remover containers
    docker container prune -f
    
    # Remover imagens
    docker image prune -a -f
    
    # Remover volumes
    docker volume prune -f
    
    # Remover redes
    docker network prune -f
    
    # Limpeza do sistema
    docker system prune -a -f
    
    print "✅ Limpeza concluída!" "$GREEN"
}

# Limpeza leve
light_cleanup() {
    print "🧹 Limpeza leve..." "$BLUE"
    
    # Parar containers
    docker-compose down 2>/dev/null || true
    
    # Remover apenas containers parados
    docker container prune -f
    
    # Remover imagens não utilizadas
    docker image prune -f
    
    print "✅ Limpeza leve concluída!" "$GREEN"
}

# Mostrar uso de espaço
show_space() {
    print "📊 Uso de espaço Docker:" "$BLUE"
    docker system df
}

# Comandos
case "${1:-light}" in
    "full") full_cleanup ;;
    "light") light_cleanup ;;
    "space") show_space ;;
    "help") print "Comandos: full, light, space" "$BLUE" ;;
    *) print "Comando desconhecido: $1" "$RED" && exit 1 ;;
esac
