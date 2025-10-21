# 🚀 Guia de Deploy - Vercel

## ✅ Configuração Completa

O projeto está configurado para deploy no Vercel com todos os arquivos necessários:

### 📁 Arquivos de Deploy
- `app.py` - Entrypoint principal (Flask)
- `vercel.json` - Configuração do Vercel
- `requirements.txt` - Dependências Python
- `.vercelignore` - Arquivos ignorados
- `Procfile` - Compatibilidade adicional

## 🚀 Deploy no Vercel

### Método 1: Deploy via GitHub (Recomendado)

1. **Acesse o Vercel**
   - Vá para [vercel.com](https://vercel.com)
   - Faça login com sua conta GitHub

2. **Importe o Projeto**
   - Clique em "New Project"
   - Selecione o repositório: `Wellychon/assistentedevendas`
   - Clique em "Import"

3. **Configuração Automática**
   - O Vercel detectará automaticamente:
     - Framework: Python Flask
     - Entrypoint: `app.py`
     - Python Version: 3.9

4. **Deploy**
   - Clique em "Deploy"
   - Aguarde o processo (2-3 minutos)
   - Seu app estará disponível em: `https://seu-projeto.vercel.app`

### Método 2: Deploy via CLI

1. **Instale o Vercel CLI**
```bash
npm i -g vercel
```

2. **Login no Vercel**
```bash
vercel login
```

3. **Deploy**
```bash
vercel
```

4. **Deploy de Produção**
```bash
vercel --prod
```

## 🔧 Configurações Importantes

### Variáveis de Ambiente
Configure no painel do Vercel:

```env
OPENROUTER_API_KEY=sua_chave_aqui
GOOGLE_SHEETS_URL=sua_url_aqui
```

### Domínio Personalizado
- Acesse: Project Settings > Domains
- Adicione seu domínio personalizado
- Configure DNS conforme instruções

## 📊 Funcionalidades no Deploy

### ✅ Funcionando
- ✅ Dashboard responsivo
- ✅ Chat com IA (OpenRouter)
- ✅ Sistema de fallback inteligente
- ✅ APIs REST funcionais
- ✅ Interface moderna

### ⚠️ Limitações do Vercel
- **Timeout**: 10 segundos por requisição
- **Memória**: 1GB RAM
- **CPU**: Limitado
- **Arquivos**: Apenas leitura (exceto /tmp)

## 🛠️ Troubleshooting

### Erro: "No Flask entrypoint found"
- ✅ **Resolvido**: Arquivo `app.py` criado
- ✅ **Configurado**: `vercel.json` com entrypoint correto

### Erro: "Module not found"
- Verifique se todas as dependências estão no `requirements.txt`
- Reinstale as dependências localmente para testar

### Erro: "Timeout"
- Otimize consultas demoradas
- Use cache para dados frequentes
- Implemente paginação para grandes datasets

## 🎯 Otimizações para Produção

### Performance
- Cache de dados em memória
- Compressão gzip ativada
- Minificação de assets
- CDN global do Vercel

### Segurança
- Chaves de API em variáveis de ambiente
- HTTPS obrigatório
- Headers de segurança configurados

## 📈 Monitoramento

### Vercel Analytics
- Acesse: Project > Analytics
- Monitore performance e erros
- Configure alertas

### Logs
- Acesse: Project > Functions > Logs
- Monitore erros em tempo real
- Debug de problemas

## 🔄 Deploy Contínuo

### GitHub Integration
- Push para `main` = Deploy automático
- Preview de PRs = Deploy de teste
- Rollback fácil via interface

### Custom Domains
- Configure DNS
- SSL automático
- Redirecionamentos

## 🎉 Status do Deploy

**✅ PRONTO PARA DEPLOY**

- [x] Entrypoint configurado (`app.py`)
- [x] Dependências otimizadas
- [x] Configuração Vercel
- [x] Rotas funcionais
- [x] APIs REST ativas
- [x] Interface responsiva

**🚀 Seu Assistente de Vendas está pronto para produção!**
