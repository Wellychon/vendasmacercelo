# 🚀 Deploy Completo - Agente de Vendas

## 📋 Opções de Deploy

### 1. 🐳 Docker (Local/Produção)
```bash
# Deploy com Docker
./deploy.sh

# Acessar: http://localhost:8081
```

### 2. ☁️ Vercel (Serverless)
```bash
# Instalar Vercel CLI
npm install -g vercel

# Deploy no Vercel
./deploy-vercel.sh

# Acessar: https://seu-projeto.vercel.app
```

## 🎯 Recomendação por Cenário

| Cenário | Recomendação | Motivo |
|---------|---------------|--------|
| **Desenvolvimento** | Docker | Hot reload, fácil debug |
| **Produção Local** | Docker | Controle total, performance |
| **Produção Cloud** | Vercel | Serverless, escalável |
| **Demo/Teste** | Vercel | Rápido, gratuito |

## ⚡ Deploy Rápido

### Docker (Recomendado para Produção)
```bash
# 1. Configurar
cp env.example .env
# Editar .env com suas chaves

# 2. Deploy
./deploy.sh

# 3. Acessar
# http://localhost:8081
```

### Vercel (Recomendado para Demo)
```bash
# 1. Instalar Vercel CLI
npm install -g vercel

# 2. Deploy
./deploy-vercel.sh

# 3. Configurar variáveis no painel do Vercel
# https://vercel.com/dashboard
```

## 🔧 Configuração

### Variáveis Necessárias

```env
# APIs
OPENROUTER_API_KEY=sua_chave_aqui
APPS_SCRIPT_URL=sua_url_do_apps_script

# Segurança
SECRET_KEY=sua_chave_secreta_aqui
```

### Arquivos de Credenciais (Docker)

- `credentials.json` - Google Sheets API
- `token.json` - Token de autenticação
- `apps_script_url.txt` - URL do Apps Script

## 📊 Comparação de Deploy

| Aspecto | Docker | Vercel |
|---------|--------|--------|
| **Setup** | 2 min | 5 min |
| **Custo** | Gratuito | Gratuito* |
| **Performance** | Excelente | Muito boa |
| **Escalabilidade** | Manual | Automática |
| **Controle** | Total | Limitado |
| **Debug** | Fácil | Médio |
| **Manutenção** | Manual | Automática |

*Plano gratuito do Vercel: 100GB bandwidth/mês

## 🛠️ Comandos Úteis

### Docker
```bash
./deploy.sh          # Deploy
./deploy.sh logs     # Ver logs
./deploy.sh stop     # Parar
./backup.sh          # Backup
./cleanup.sh         # Limpeza
```

### Vercel
```bash
./deploy-vercel.sh        # Deploy produção
./deploy-vercel.sh dev    # Deploy desenvolvimento
./deploy-vercel.sh logs   # Ver logs
./deploy-vercel.sh status # Status
```

## 🧪 Testes

### Testar API Local
```bash
# Testar endpoints
python3 test-vercel.py

# Testar com URL específica
python3 test-vercel.py https://seu-projeto.vercel.app
```

### Testar Deploy
```bash
# Docker
curl http://localhost:8081/api/health

# Vercel
curl https://seu-projeto.vercel.app/api/health
```

## 📈 Monitoramento

### Docker
```bash
# Status
docker-compose ps

# Logs
docker-compose logs -f app

# Recursos
docker stats
```

### Vercel
```bash
# Logs
vercel logs

# Status
vercel ls

# Métricas no painel: https://vercel.com/dashboard
```

## 🔍 Troubleshooting

### Problemas Comuns

**Docker não inicia:**
```bash
# Verificar Docker
docker --version
docker-compose --version

# Rebuild
docker-compose build --no-cache
```

**Vercel não faz deploy:**
```bash
# Verificar CLI
vercel --version

# Login
vercel login

# Deploy manual
vercel --prod
```

**API não responde:**
```bash
# Testar localmente
python3 api/index.py

# Verificar logs
./deploy.sh logs
# ou
vercel logs
```

## 📝 Próximos Passos

### Após Deploy

1. **Configurar domínio** (se necessário)
2. **Configurar SSL** (Vercel automático)
3. **Configurar monitoramento**
4. **Configurar backup** (Docker)
5. **Configurar CI/CD** (opcional)

### Melhorias Futuras

- **Cache Redis** (para Docker)
- **CDN** (para Vercel)
- **Monitoring** (Prometheus/Grafana)
- **Logs centralizados**
- **Backup automático**

## 🎉 Deploy Concluído!

### Docker
- **URL**: http://localhost:8081
- **API**: http://localhost:8081/api/data
- **Health**: http://localhost:8081/api/health

### Vercel
- **URL**: https://seu-projeto.vercel.app
- **API**: https://seu-projeto.vercel.app/api/data
- **Health**: https://seu-projeto.vercel.app/api/health

---

**Aplicação rodando com sucesso!** 🚀
