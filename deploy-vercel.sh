#!/bin/bash

# 🚀 Deploy Script - Vercel (Otimizado)
set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print() { echo -e "${2}${1}${NC}"; }

# Verificar Vercel CLI
check_vercel() {
    if ! command -v vercel >/dev/null 2>&1; then
        print "❌ Vercel CLI não instalado!" "$RED"
        print "Instale com: npm i -g vercel" "$YELLOW"
        exit 1
    fi
}

# Setup inicial
setup() {
    print "⚙️ Configurando para Vercel..." "$BLUE"
    
    # Criar .env.local se não existir
    if [ ! -f ".env.local" ] && [ -f "env.vercel" ]; then
        cp env.vercel .env.local
        print "✅ .env.local criado" "$GREEN"
    fi
    
    # Verificar arquivos necessários
    if [ ! -f "api/index.py" ]; then
        print "❌ api/index.py não encontrado!" "$RED"
        exit 1
    fi
    
    if [ ! -f "vercel.json" ]; then
        print "❌ vercel.json não encontrado!" "$RED"
        exit 1
    fi
}

# Deploy
deploy() {
    print "🚀 Fazendo deploy no Vercel..." "$BLUE"
    check_vercel
    setup
    
    # Deploy
    vercel --prod
    
    print "✅ Deploy concluído!" "$GREEN"
}

# Deploy de desenvolvimento
deploy_dev() {
    print "🚀 Deploy de desenvolvimento..." "$BLUE"
    check_vercel
    setup
    
    # Deploy dev
    vercel
    
    print "✅ Deploy de desenvolvimento concluído!" "$GREEN"
}

# Ver logs
logs() {
    print "📋 Logs do Vercel..." "$BLUE"
    vercel logs
}

# Status
status() {
    print "📊 Status do projeto..." "$BLUE"
    vercel ls
}

# Remover deploy
remove() {
    print "🗑️ Removendo deploy..." "$BLUE"
    vercel remove --yes
    print "✅ Deploy removido!" "$GREEN"
}

# Configurar variáveis
env() {
    print "⚙️ Configurando variáveis de ambiente..." "$BLUE"
    print "Configure as variáveis no painel do Vercel:" "$YELLOW"
    print "- OPENROUTER_API_KEY" "$YELLOW"
    print "- APPS_SCRIPT_URL" "$YELLOW"
    print "- SECRET_KEY" "$YELLOW"
    print "" "$NC"
    print "Ou use: vercel env add" "$BLUE"
}

# Comandos
case "${1:-deploy}" in
    "deploy") deploy ;;
    "dev") deploy_dev ;;
    "logs") logs ;;
    "status") status ;;
    "remove") remove ;;
    "env") env ;;
    "help") 
        print "Comandos: deploy, dev, logs, status, remove, env" "$BLUE"
        ;;
    *) print "Comando desconhecido: $1" "$RED" && exit 1 ;;
esac
