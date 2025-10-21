# ⚡ Quick Start - Agente de Vendas

## 🚀 Deploy em 3 Passos

### 1. Configurar
```bash
cp env.example .env
# Editar .env com suas chaves de API
```

### 2. Deploy
```bash
./deploy.sh
```

### 3. Acessar
```
http://localhost:8081
```

## 📋 Comandos Essenciais

```bash
# Deploy
./deploy.sh

# Ver logs
./deploy.sh logs

# Parar
./deploy.sh stop

# Backup
./backup.sh

# Limpeza
./cleanup.sh
```

## 🔧 Desenvolvimento

```bash
# Modo desenvolvimento (hot reload)
docker-compose -f docker-compose.dev.yml up -d

# Modo produção
docker-compose up -d
```

## 📊 Status

```bash
# Ver status
./deploy.sh status

# Ver uso de espaço
./cleanup.sh space

# Ver logs
./deploy.sh logs
```

---

**Pronto!** Aplicação rodando em http://localhost:8081 🎉
