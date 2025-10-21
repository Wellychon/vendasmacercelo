# 🐳 Deploy com Docker - Agente de Vendas

Este guia explica como fazer o deploy da aplicação Agente de Vendas usando Docker.

## 📋 Pré-requisitos

- Docker instalado (versão 20.10+)
- Docker Compose instalado (versão 2.0+)
- Arquivos de credenciais do Google Sheets
- Chave da API OpenRouter

## 🚀 Deploy Rápido

### 1. Preparar Arquivos de Configuração

```bash
# Copiar arquivo de exemplo de variáveis de ambiente
cp env.example .env

# Editar as variáveis necessárias
nano .env
```

### 2. Configurar Credenciais

Certifique-se de que os seguintes arquivos estão presentes:
- `credentials.json` - Credenciais do Google Sheets API
- `token.json` - Token de autenticação (gerado automaticamente)
- `apps_script_url.txt` - URL do Apps Script

### 3. Deploy com Docker Compose

```bash
# Construir e iniciar os serviços
docker-compose up -d

# Verificar status dos containers
docker-compose ps

# Ver logs da aplicação
docker-compose logs -f app
```

### 4. Acessar a Aplicação

- **Aplicação**: http://localhost:8081
- **Com Nginx**: http://localhost (porta 80)

## 🔧 Comandos Úteis

### Gerenciamento de Containers

```bash
# Parar todos os serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v

# Reiniciar apenas a aplicação
docker-compose restart app

# Ver logs em tempo real
docker-compose logs -f app

# Acessar container da aplicação
docker-compose exec app bash
```

### Build e Deploy

```bash
# Rebuild da imagem
docker-compose build --no-cache

# Deploy apenas da aplicação (sem nginx)
docker-compose up -d app

# Deploy completo
docker-compose up -d
```

### Monitoramento

```bash
# Status dos containers
docker-compose ps

# Uso de recursos
docker stats

# Health check
curl http://localhost:8081/api/data
```

## 🛠️ Configurações Avançadas

### Variáveis de Ambiente

Edite o arquivo `.env` para configurar:

```env
# Configurações da aplicação
FLASK_ENV=production
APP_PORT=8081

# APIs externas
OPENROUTER_API_KEY=sua_chave_aqui
APPS_SCRIPT_URL=sua_url_do_apps_script

# Configurações de segurança
SECRET_KEY=sua_chave_secreta_aqui
```

### Nginx (Opcional)

Para usar o Nginx como proxy reverso:

```bash
# Deploy com Nginx
docker-compose up -d

# Acessar via Nginx
curl http://localhost
```

### SSL/HTTPS

Para configurar HTTPS:

1. Coloque os certificados SSL na pasta `ssl/`
2. Descomente as linhas de SSL no `nginx.conf`
3. Reinicie os containers

## 🔍 Troubleshooting

### Problemas Comuns

**Container não inicia:**
```bash
# Verificar logs
docker-compose logs app

# Verificar configuração
docker-compose config
```

**Erro de permissão:**
```bash
# Ajustar permissões
sudo chown -R $USER:$USER .
```

**Porta já em uso:**
```bash
# Verificar portas em uso
netstat -tulpn | grep :8081

# Alterar porta no docker-compose.yml
```

### Logs e Debugging

```bash
# Logs da aplicação
docker-compose logs -f app

# Logs do Nginx
docker-compose logs -f nginx

# Acessar container para debug
docker-compose exec app bash
```

## 📊 Monitoramento

### Health Checks

A aplicação inclui health checks automáticos:

```bash
# Verificar saúde da aplicação
curl http://localhost:8081/api/data

# Health check do Docker
docker inspect agente-vendas-app | grep Health -A 10
```

### Métricas

```bash
# Uso de CPU e memória
docker stats agente-vendas-app

# Espaço em disco
docker system df
```

## 🔄 Atualizações

### Atualizar Aplicação

```bash
# Parar serviços
docker-compose down

# Atualizar código
git pull

# Rebuild e iniciar
docker-compose up -d --build
```

### Backup

```bash
# Backup dos logs
docker cp agente-vendas-app:/app/logs ./backup_logs_$(date +%Y%m%d)

# Backup dos dados (se houver)
docker-compose exec app tar -czf /tmp/backup.tar.gz /app/data
```

## 🚀 Deploy em Produção

### Configurações Recomendadas

1. **Usar variáveis de ambiente** para configurações sensíveis
2. **Configurar SSL** para HTTPS
3. **Implementar backup** regular dos dados
4. **Monitorar logs** e performance
5. **Usar secrets** do Docker para credenciais

### Exemplo de Deploy em Servidor

```bash
# No servidor de produção
git clone <seu-repositorio>
cd agente-vendas

# Configurar .env com valores de produção
cp env.example .env
nano .env

# Deploy
docker-compose up -d

# Verificar
curl http://seu-servidor:8081/api/data
```

## 📝 Notas Importantes

- A aplicação roda na porta 8081 por padrão
- Os logs são salvos na pasta `logs/`
- As credenciais são montadas como volumes read-only
- O Nginx é opcional mas recomendado para produção
- Use `docker-compose down` antes de fazer alterações

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs: `docker-compose logs -f app`
2. Confirme as configurações: `docker-compose config`
3. Teste a conectividade: `curl http://localhost:8081/api/data`
4. Verifique os arquivos de credenciais

---

**Deploy realizado com sucesso!** 🎉

A aplicação estará disponível em http://localhost:8081
