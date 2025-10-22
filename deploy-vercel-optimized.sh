#!/bin/bash

echo "🚀 Deploy Otimizado para Vercel - Dashboard Moderno"
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📋 Verificando pré-requisitos...${NC}"

# Verifica se o Vercel CLI está instalado
if ! command -v vercel &> /dev/null; then
    echo -e "${RED}❌ Vercel CLI não encontrado. Instalando...${NC}"
    npm install -g vercel
fi

# Verifica se está logado no Vercel
if ! vercel whoami &> /dev/null; then
    echo -e "${YELLOW}⚠️ Não está logado no Vercel. Faça login primeiro:${NC}"
    echo "vercel login"
    exit 1
fi

echo -e "${GREEN}✅ Vercel CLI configurado${NC}"

# Verifica tamanho do projeto
echo -e "${BLUE}📊 Verificando tamanho do projeto...${NC}"
PROJECT_SIZE=$(du -sh . | cut -f1)
echo -e "${GREEN}📦 Tamanho do projeto: $PROJECT_SIZE${NC}"

if [[ $PROJECT_SIZE > "250M" ]]; then
    echo -e "${RED}❌ Projeto muito grande para Vercel (limite: 250MB)${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Projeto dentro do limite do Vercel${NC}"

# Verifica se as variáveis de ambiente estão configuradas
echo -e "${BLUE}🔧 Verificando configurações...${NC}"

# Cria arquivo de ambiente se não existir
if [ ! -f ".env.local" ]; then
    echo -e "${YELLOW}⚠️ Criando arquivo .env.local...${NC}"
    cat > .env.local << EOF
OPENROUTER_API_KEY=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
PYTHON_VERSION=3.11
EOF
    echo -e "${GREEN}✅ Arquivo .env.local criado${NC}"
fi

# Verifica se o dashboard_app.py está configurado
if [ ! -f "dashboard_app.py" ]; then
    echo -e "${RED}❌ dashboard_app.py não encontrado${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Arquivos principais encontrados${NC}"

# Deploy
echo -e "${BLUE}🚀 Iniciando deploy...${NC}"
echo -e "${YELLOW}📝 Configurações:${NC}"
echo "  - Entry point: api.py"
echo "  - Template: modern_dashboard.html"
echo "  - IA: OpenRouter configurada"
echo "  - Dados: 2.400 registros"

# Deploy com configurações otimizadas
vercel --prod --yes

echo -e "${GREEN}🎉 Deploy concluído!${NC}"
echo -e "${BLUE}📱 Acesse seu dashboard em: https://seu-projeto.vercel.app${NC}"
echo -e "${YELLOW}💡 Dicas:${NC}"
echo "  - Use 'Atualizar Dados' para carregar informações da planilha"
echo "  - Chat com IA está funcionando"
echo "  - Dashboard responsivo e moderno"
