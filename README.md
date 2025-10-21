# 🤖 Agente de Vendas - IA para Análise de Dados

Sistema inteligente de análise de vendas com IA, integração com Google Sheets e deploy otimizado.

## 🚀 Deploy Rápido

### Docker (Recomendado)
```bash
# Deploy completo
./deploy.sh

# Acessar: http://localhost:8081
```

### Vercel (Serverless)
```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy
./deploy-vercel.sh

# Acessar: https://seu-projeto.vercel.app
```

## ✨ Funcionalidades

- 📊 **Análise de Vendas** - IA para insights automáticos
- 📈 **Dashboard Interativo** - Visualizações em tempo real
- 🤖 **Chat com IA** - Perguntas sobre vendas
- 📋 **Integração Google Sheets** - Dados em tempo real
- 🐳 **Deploy Docker** - Container otimizado
- ☁️ **Deploy Vercel** - Serverless global

## 🛠️ Tecnologias

- **Backend**: Python, Flask
- **IA**: OpenRouter API
- **Dados**: Google Sheets API
- **Deploy**: Docker, Vercel
- **Frontend**: HTML, CSS, JavaScript

## 📊 Métricas Atuais

- **2.400 registros** de vendas
- **12 guias** de dados
- **Análise em tempo real**
- **IA integrada**

## 🎯 Opções de Deploy

| Método | Complexidade | Custo | Performance | Recomendação |
|--------|-------------|-------|-------------|---------------|
| **Docker** | Baixa | Gratuito | Excelente | Produção |
| **Vercel** | Muito Baixa | Gratuito* | Muito Boa | Demo/Teste |

*Plano gratuito: 100GB bandwidth/mês

## 🔧 Configuração

### 1. Clonar Repositório
```bash
git clone https://github.com/Wellychon/assistentedevendas.git
cd assistentedevendas
```

### 2. Configurar Variáveis
```bash
# Copiar arquivo de exemplo
cp env.example .env

# Editar com suas chaves
nano .env
```

### 3. Deploy
```bash
# Docker
./deploy.sh

# Vercel
./deploy-vercel.sh
```

## 📁 Estrutura do Projeto

```
├── api/                    # API para Vercel
│   └── index.py
├── templates/              # Templates HTML
│   └── dashboard.html
├── Dockerfile             # Container Docker
├── docker-compose.yml    # Orquestração Docker
├── vercel.json           # Configuração Vercel
├── deploy.sh             # Script Docker
├── deploy-vercel.sh      # Script Vercel
└── requirements.txt      # Dependências Python
```

## 🌐 Endpoints da API

- **`/`** - Página inicial
- **`/api/data`** - Dados da planilha
- **`/api/analysis`** - Análise dos dados
- **`/api/chat`** - Chat com IA
- **`/api/health`** - Health check

## 🧪 Testes

```bash
# Testar API local
python3 test-vercel.py

# Testar deploy
python3 test-vercel.py https://seu-projeto.vercel.app
```

## 📚 Documentação

- **[Docker Deploy](DOCKER_DEPLOY.md)** - Deploy com Docker
- **[Vercel Deploy](VERCEL_DEPLOY.md)** - Deploy no Vercel
- **[Deploy Completo](DEPLOY_COMPLETE.md)** - Guia completo
- **[Quick Start](QUICK_START.md)** - Início rápido

## 🔍 Troubleshooting

### Problemas Comuns

**Docker não inicia:**
```bash
# Verificar Docker
docker --version
./deploy.sh logs
```

**Vercel não faz deploy:**
```bash
# Verificar CLI
vercel --version
vercel login
```

**API não responde:**
```bash
# Testar localmente
python3 api/index.py
```

## 📈 Performance

### Otimizações Implementadas

- ✅ **Docker Alpine** (100MB vs 500MB)
- ✅ **Serverless** (escala automática)
- ✅ **Cache inteligente** (dados em memória)
- ✅ **Health checks** (monitoramento)
- ✅ **Scripts otimizados** (deploy rápido)

### Métricas

- **Tempo de Deploy**: 30-60s
- **Tamanho da Imagem**: ~100MB
- **Uso de Memória**: 512MB
- **Tempo de Resposta**: <200ms

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- **Issues**: [GitHub Issues](https://github.com/Wellychon/assistentedevendas/issues)
- **Documentação**: [Wiki do Projeto](https://github.com/Wellychon/assistentedevendas/wiki)
- **Deploy**: [Guia de Deploy](DEPLOY_COMPLETE.md)

## 🎉 Status do Projeto

![Deploy Status](https://img.shields.io/badge/deploy-ready-green)
![Docker](https://img.shields.io/badge/docker-optimized-blue)
![Vercel](https://img.shields.io/badge/vercel-serverless-purple)
![Python](https://img.shields.io/badge/python-3.11-yellow)

---

**Desenvolvido com ❤️ para análise inteligente de vendas**