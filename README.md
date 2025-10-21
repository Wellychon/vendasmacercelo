# 🤖 Assistente de Vendas - Dashboard Inteligente

Um sistema completo de análise de vendas com chatbot inteligente conectado à API OpenRouter, integrado com Google Sheets e interface moderna.

## 🚀 Funcionalidades

### 📊 Dashboard de Vendas
- **Interface Moderna**: Design responsivo e intuitivo
- **Dados em Tempo Real**: Atualização automática dos dados
- **Visualizações Interativas**: Gráficos e tabelas dinâmicas
- **Múltiplas Guias**: Suporte a 12 guias mensais

### 🤖 Chatbot Inteligente
- **IA Real**: Conectado à API OpenRouter
- **Análise Contextual**: Respostas baseadas nos dados reais
- **Fallback Inteligente**: Sistema local quando API falha
- **Chat em Tempo Real**: Interface de conversação moderna

### 📈 Análises Disponíveis
- **Performance de Vendas**: Métricas e tendências
- **Análise de Produtos**: Rankings e categorias
- **Análise Geográfica**: Performance por região
- **Tendências Temporais**: Variações mensais
- **Insights Estratégicos**: Recomendações baseadas em dados

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **IA**: OpenRouter API (DeepSeek, Llama, Phi-3, Gemma)
- **Dados**: Google Sheets API
- **Integração**: Google Apps Script

## 📋 Pré-requisitos

- Python 3.8+
- Conta Google (para Google Sheets)
- Chave de API OpenRouter (opcional)

## 🚀 Instalação

1. **Clone o repositório**
```bash
git clone https://github.com/Wellychon/assistentedevendas.git
cd assistentedevendas
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Configure as credenciais**
```bash
python setup_credentials.py
```

4. **Configure a API OpenRouter (opcional)**
Edite o arquivo `api_openrouter.py` e substitua pela sua chave:
```python
API_KEY = "sua_chave_aqui"
```

## 🎯 Como Usar

1. **Inicie o servidor**
```bash
python dashboard_app.py
```

2. **Acesse o dashboard**
Abra seu navegador em: `http://localhost:8081`

3. **Carregue os dados**
Clique em "Atualizar Dados" para carregar informações da planilha

4. **Inicie o chat**
Digite perguntas sobre seus dados de vendas

## 📊 Dados Suportados

- **2.400 registros** de vendas
- **12 guias mensais** (Janeiro a Dezembro 2025)
- **200 registros por mês**
- **Múltiplas colunas**: Produto, Categoria, Região, Vendedor, Receita, etc.

## 🤖 Exemplos de Perguntas para o Chatbot

- "Mostre um resumo das vendas de 2025"
- "Quais produtos venderam mais em janeiro?"
- "Qual região teve melhor performance?"
- "Analise as tendências mensais"
- "Compare os meses de maior e menor venda"
- "Quais são as oportunidades de crescimento?"

## 🔧 Configuração Avançada

### Google Sheets
1. Crie uma planilha com os dados de vendas
2. Configure o Google Apps Script
3. Atualize a URL no arquivo `apps_script_url.txt`

### API OpenRouter
1. Acesse [OpenRouter](https://openrouter.ai/)
2. Crie uma conta e gere uma chave de API
3. Substitua no arquivo `api_openrouter.py`

## 📁 Estrutura do Projeto

```
assistentedevendas/
├── dashboard_app.py          # Aplicação principal Flask
├── api_openrouter.py         # Integração com IA
├── google_sheets_service.py  # Serviço Google Sheets
├── apps_script_service.py    # Google Apps Script
├── templates/
│   └── dashboard.html        # Interface do dashboard
├── requirements.txt          # Dependências Python
├── setup_credentials.py     # Configuração de credenciais
└── README.md                # Este arquivo
```

## 🎨 Interface

- **Design Moderno**: Interface limpa e profissional
- **Responsivo**: Funciona em desktop e mobile
- **Chat Inteligente**: Interface de conversação intuitiva
- **Visualizações**: Gráficos e tabelas interativas

## 🔒 Segurança

- Credenciais armazenadas localmente
- Chaves de API em variáveis de ambiente
- Dados processados localmente
- Conexão segura com APIs externas

## 📈 Performance

- **Cache Inteligente**: Dados em memória para performance
- **Atualização Automática**: Refresh a cada 5 minutos
- **Fallback Robusto**: Sistema local quando APIs falham
- **Interface Otimizada**: Carregamento rápido

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte ou dúvidas:
- Abra uma issue no GitHub
- Entre em contato via email

## 🎉 Agradecimentos

- OpenRouter pela API de IA
- Google pela integração com Sheets
- Comunidade Python pelo suporte

---

**Desenvolvido com ❤️ para análise inteligente de vendas**