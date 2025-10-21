#!/bin/bash

# 🔄 Backup Script - Agente de Vendas (Otimizado)
set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print() { echo -e "${2}${1}${NC}"; }

# Configurações
BACKUP_DIR="./backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/backup_${DATE}.tar.gz"

# Criar backup
create_backup() {
    print "🔄 Criando backup..." "$BLUE"
    mkdir -p "$BACKUP_DIR"
    
    # Arquivos essenciais
    tar -czf "$BACKUP_FILE" \
        credentials.json \
        token.json \
        apps_script_url.txt \
        .env \
        logs/ \
        templates/ \
        2>/dev/null || true
    
    print "✅ Backup criado: $BACKUP_FILE" "$GREEN"
    print "📊 Tamanho: $(du -h "$BACKUP_FILE" | cut -f1)" "$GREEN"
    
    # Limpar backups antigos (manter últimos 5)
    cd "$BACKUP_DIR"
    ls -t backup_*.tar.gz | tail -n +6 | xargs -r rm -f
}

# Listar backups
list_backups() {
    print "📋 Backups disponíveis:" "$BLUE"
    if [ -d "$BACKUP_DIR" ]; then
        ls -lh "$BACKUP_DIR"/backup_*.tar.gz 2>/dev/null || print "Nenhum backup encontrado" "$YELLOW"
    else
        print "Diretório de backup não existe" "$YELLOW"
    fi
}

# Restaurar backup
restore_backup() {
    local file="$1"
    if [ -z "$file" ]; then
        print "❌ Especifique o arquivo de backup" "$RED"
        exit 1
    fi
    
    if [ ! -f "$BACKUP_DIR/$file" ]; then
        print "❌ Arquivo não encontrado: $file" "$RED"
        exit 1
    fi
    
    print "🔄 Restaurando $file..." "$BLUE"
    docker-compose down 2>/dev/null || true
    tar -xzf "$BACKUP_DIR/$file"
    print "✅ Backup restaurado!" "$GREEN"
}

# Comandos
case "${1:-backup}" in
    "backup") create_backup ;;
    "list") list_backups ;;
    "restore") restore_backup "$2" ;;
    "help") print "Comandos: backup, list, restore <arquivo>" "$BLUE" ;;
    *) print "Comando desconhecido: $1" "$RED" && exit 1 ;;
esac
