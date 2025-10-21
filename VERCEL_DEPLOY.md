# 🚀 Deploy no Vercel - Agente de Vendas

## 📋 Pré-requisitos

1. **Conta no Vercel** (gratuita)
2. **Vercel CLI** instalado
3. **Node.js** (para instalar Vercel CLI)

## ⚡ Deploy Rápido

### 1. Instalar Vercel CLI
```bash
npm install -g vercel
```

### 2. Deploy Automatizado
```bash
# Deploy de produção
./deploy-vercel.sh

# Deploy de desenvolvimento
./deploy-vercel.sh dev
```

### 3. Deploy Manual
```bash
# Login no Vercel
vercel login

# Deploy
vercel --prod
```

## 🔧 Configuração

### Variáveis de Ambiente

Configure no painel do Vercel ou via CLI:

```bash
# Via CLI
vercel env add OPENROUTER_API_KEY
vercel env add APPS_SCRIPT_URL
vercel env add SECRET_KEY

# Ou configure no painel: https://vercel.com/dashboard
```

### Arquivos Necessários

- ✅ `api/index.py` - Aplicação principal
- ✅ `vercel.json` - Configuração do Vercel
- ✅ `requirements.txt` - Dependências Python
- ✅ `env.vercel` - Exemplo de variáveis

## 📊 Estrutura do Projeto

```
/
├── api/
│   └── index.py          # Aplicação principal
├── vercel.json           # Configuração Vercel
├── requirements.txt      # Dependências
├── deploy-vercel.sh     # Script de deploy
└── env.vercel           # Variáveis de exemplo
```

## 🌐 Endpoints Disponíveis

- **`/`** - Página inicial com informações
- **`/api/data`** - Dados da planilha
- **`/api/analysis`** - Análise dos dados
- **`/api/chat`** - Chat com IA
- **`/api/update`** - Atualizar dados
- **`/api/health`** - Health check

## 🔍 Comandos Úteis

```bash
# Deploy
./deploy-vercel.sh

# Ver logs
./deploy-vercel.sh logs

# Status
./deploy-vercel.sh status

# Configurar env
./deploy-vercel.sh env

# Remover deploy
./deploy-vercel.sh remove
```

## 🛠️ Desenvolvimento Local

```bash
# Instalar dependências
pip install -r requirements.txt

# Configurar .env.local
cp env.vercel .env.local
# Editar .env.local com suas chaves

# Testar localmente
python api/index.py
```

## 📝 Configuração Avançada

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/index.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "api/index.py"
    }
  ],
  "functions": {
    "api/index.py": {
      "maxDuration": 30,
      "memory": 1024
    }
  }
}
```

### Variáveis de Ambiente Necessárias

```env
OPENROUTER_API_KEY=sua_chave_aqui
APPS_SCRIPT_URL=sua_url_do_apps_script
SECRET_KEY=sua_chave_secreta
```

## 🔍 Troubleshooting

### Problemas Comuns

**Erro de import:**
```bash
# Verificar se todos os arquivos estão na pasta api/
ls -la api/
```

**Erro de dependências:**
```bash
# Verificar requirements.txt
cat requirements.txt
```

**Erro de variáveis:**
```bash
# Verificar variáveis no Vercel
vercel env ls
```

### Logs

```bash
# Ver logs em tempo real
vercel logs --follow

# Ver logs de uma função específica
vercel logs --function=api/index.py
```

## 📊 Monitoramento

### Métricas no Vercel

- **Function Invocations** - Número de chamadas
- **Function Duration** - Tempo de execução
- **Function Errors** - Erros
- **Bandwidth** - Tráfego

### Health Check

```bash
# Testar endpoint
curl https://seu-projeto.vercel.app/api/health

# Resposta esperada
{
  "status": "healthy",
  "timestamp": "2024-01-15 10:30:00",
  "data_loaded": true
}
```

## 🚀 Otimizações

### Performance
- ✅ **Serverless** - Escala automaticamente
- ✅ **Edge Functions** - Resposta rápida
- ✅ **Caching** - Dados em cache
- ✅ **Compression** - Gzip automático

### Custos
- ✅ **Plano Gratuito** - 100GB bandwidth/mês
- ✅ **Function Calls** - 100GB-hours/mês
- ✅ **Sem custos** para projetos pequenos/médios

## 📱 Testando a API

```bash
# Testar dados
curl https://seu-projeto.vercel.app/api/data

# Testar análise
curl https://seu-projeto.vercel.app/api/analysis

# Testar chat
curl -X POST https://seu-projeto.vercel.app/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Olá!"}'
```

## 🎉 Deploy Concluído!

Sua aplicação estará disponível em:
- **URL**: `https://seu-projeto.vercel.app`
- **API**: `https://seu-projeto.vercel.app/api/data`
- **Health**: `https://seu-projeto.vercel.app/api/health`

---

**Deploy realizado com sucesso!** 🚀
