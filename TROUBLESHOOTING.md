# 🔧 Troubleshooting - Deploy Vercel

## ⚠️ Problemas Comuns e Soluções

### 1. **Deploy Demorando Muito**

#### **Causas Possíveis:**
- Dependências pesadas (pandas, openai)
- Primeira instalação
- Servidor sobrecarregado

#### **Soluções:**
```bash
# Aguarde mais tempo (até 10 minutos)
# Verifique logs no Vercel Dashboard
# Tente deploy manual
```

### 2. **Erro: "No Flask entrypoint found"**

#### **Solução:**
- ✅ **Resolvido**: Arquivo `app.py` criado
- ✅ **Configurado**: `vercel.json` com entrypoint correto

### 3. **Erro: "Module not found"**

#### **Solução:**
```bash
# Verifique requirements.txt
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements"
git push
```

### 4. **Erro: "Timeout"**

#### **Solução:**
- Otimize consultas demoradas
- Use cache para dados frequentes
- Implemente paginação

### 5. **Deploy Falhando**

#### **Teste Local Primeiro:**
```bash
python3 app.py
# Teste: http://localhost:8081
```

#### **Verifique Logs:**
1. Acesse Vercel Dashboard
2. Clique no projeto
3. Veja "Functions" > "Logs"
4. Identifique o erro

## 🚀 Deploy Manual

### **Método 1: Vercel CLI**
```bash
npm i -g vercel
vercel login
vercel
vercel --prod
```

### **Método 2: GitHub Integration**
1. Acesse [vercel.com](https://vercel.com)
2. "New Project"
3. Import: `Wellychon/assistentedevendas`
4. Deploy

### **Método 3: Deploy Simples**
```bash
# Use o arquivo test_vercel.py
# Renomeie vercel_simple.json para vercel.json
# Faça deploy
```

## 🔍 Debugging

### **Verificar Status:**
```bash
# Local
python3 app.py
curl http://localhost:8081

# Vercel
# Acesse a URL do deploy
# Verifique console do navegador
```

### **Logs Importantes:**
- **Build Logs**: Instalação de dependências
- **Function Logs**: Erros em runtime
- **Deployment Logs**: Processo de deploy

## ⚡ Otimizações

### **Para Deploy Mais Rápido:**
1. **Reduza dependências** no requirements.txt
2. **Use cache** para dados frequentes
3. **Otimize imports** no código
4. **Configure timeout** adequado

### **Requirements.txt Otimizado:**
```
Flask==2.3.3
requests==2.31.0
openai==1.3.0
# Remova pandas se não essencial
```

## 🎯 Status Atual

### **✅ Funcionando Localmente:**
- App rodando em http://localhost:8081
- APIs funcionais
- Chatbot operacional

### **⏳ Deploy Vercel:**
- Configuração otimizada
- Arquivos corretos
- Aguardando deploy

## 🆘 Se Ainda Não Funcionar

### **Deploy Alternativo:**
1. **Heroku**: `git push heroku main`
2. **Railway**: Deploy via GitHub
3. **Render**: Deploy automático
4. **PythonAnywhere**: Upload manual

### **Contato:**
- Verifique logs no Vercel Dashboard
- Teste localmente primeiro
- Use deploy simples (test_vercel.py)

## 📊 Monitoramento

### **Vercel Dashboard:**
- **Analytics**: Performance
- **Functions**: Logs de erro
- **Domains**: Configuração DNS

### **Métricas Importantes:**
- **Response Time**: < 2 segundos
- **Error Rate**: < 1%
- **Uptime**: > 99%

---

**💡 Dica**: Se o deploy demorar mais de 10 minutos, tente um novo deploy ou use uma plataforma alternativa.
