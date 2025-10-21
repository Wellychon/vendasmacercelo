# 🔑 Configuração da API OpenRouter

## Como Conectar sua API Real

### 1. Obter uma Chave de API Válida

- Acesse: https://openrouter.ai/
- Crie uma conta ou faça login
- Vá em "API Keys" no menu
- Clique em "Create Key"
- Copie a chave gerada

### 2. Configurar a Chave

Edite o arquivo `config_api.py` e substitua a chave:

```python
OPENROUTER_API_KEY = "sua_chave_aqui"
```

### 3. Testar a Conexão

Execute:
```bash
python3 api_openrouter.py
```

### 4. Iniciar o Dashboard

```bash
python3 dashboard_app.py
```

## Status Atual

✅ **Chatbot Funcionando**: Sistema de fallback inteligente ativo
✅ **Dados Reais**: 2.400 registros carregados
✅ **Interface Completa**: Chat em tempo real
✅ **Análises Contextuais**: Baseadas nos dados reais

## Funcionalidades Disponíveis

- 📊 Análise de vendas em tempo real
- 🛍️ Ranking de produtos
- 🌍 Análise geográfica
- 📈 Tendências mensais
- 🤖 Chat inteligente com IA

## Próximos Passos

1. Configure sua chave de API válida
2. Reinicie o dashboard
3. Teste o chat com IA real
4. Faça perguntas sobre seus dados

*O sistema funciona mesmo sem API externa, usando análises inteligentes baseadas nos seus dados reais.*
