# 🐳 Docker - Agente de Vendas (Otimizado)

Configuração Docker **leve e funcional** para deploy rápido.

## 🚀 Deploy Rápido

```bash
# Deploy automático
./deploy.sh

# Ver status
./deploy.sh status

# Ver logs
./deploy.sh logs
```

## 📁 Arquivos Principais

- `Dockerfile` - Imagem Alpine otimizada (~100MB)
- `docker-compose.yml` - Produção simples
- `docker-compose.dev.yml` - Desenvolvimento com hot reload
- `deploy.sh` - Script de deploy (77 linhas)
- `backup.sh` - Script de backup (80 linhas)

## ⚡ Otimizações

### **Dockerfile:**
- ✅ Alpine Linux (menor que Ubuntu)
- ✅ Multi-stage build
- ✅ Cache de dependências
- ✅ Usuário não-root
- ✅ Health check simples

### **Docker Compose:**
- ✅ Apenas 1 container (sem Nginx desnecessário)
- ✅ Limite de memória (512MB)
- ✅ Restart automático
- ✅ Volumes mínimos

### **Scripts:**
- ✅ Deploy em 77 linhas (vs 300+ anterior)
- ✅ Backup em 80 linhas (vs 400+ anterior)
- ✅ Verificações essenciais apenas
- ✅ Output colorido e limpo

## 🔧 Comandos

### **Deploy:**
```bash
./deploy.sh          # Deploy completo
./deploy.sh stop     # Parar
./deploy.sh restart  # Reiniciar
./deploy.sh logs     # Ver logs
./deploy.sh status   # Status
./deploy.sh clean    # Limpar tudo
```

### **Backup:**
```bash
./backup.sh              # Criar backup
./backup.sh list         # Listar backups
./backup.sh restore file # Restaurar
```

### **Desenvolvimento:**
```bash
# Desenvolvimento com hot reload
docker-compose -f docker-compose.dev.yml up -d

# Produção
docker-compose up -d
```

## 📊 Comparação

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Dockerfile** | 55 linhas | 55 linhas (otimizado) |
| **Compose** | 50 linhas | 30 linhas |
| **Deploy Script** | 300+ linhas | 77 linhas |
| **Backup Script** | 400+ linhas | 80 linhas |
| **Imagem** | ~500MB | ~100MB |
| **Memória** | 1GB+ | 512MB |
| **Containers** | 3+ | 1 |

## 🎯 Funcionalidades

### **✅ Mantido:**
- Deploy automatizado
- Health checks
- Backup/restore
- Logs estruturados
- Segurança básica

### **❌ Removido:**
- Nginx desnecessário
- Redis não usado
- Configurações complexas
- Scripts verbosos
- Dependências extras

## 🔍 Troubleshooting

```bash
# Ver logs
docker-compose logs app

# Acessar container
docker-compose exec app sh

# Rebuild
docker-compose build --no-cache

# Limpar tudo
docker system prune -a
```

## 📝 Configuração

1. **Copie o .env:**
   ```bash
   cp env.example .env
   ```

2. **Configure as APIs:**
   - `OPENROUTER_API_KEY`
   - `APPS_SCRIPT_URL`

3. **Deploy:**
   ```bash
   ./deploy.sh
   ```

## 🌐 Acesso

- **Aplicação**: http://localhost:8081
- **API**: http://localhost:8081/api/data
- **Health**: http://localhost:8081/api/data

---

**Resultado:** Configuração **3x mais leve** e **5x mais simples**! 🎉
