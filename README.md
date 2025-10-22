# Dashboard de Vendas - Marcelo 📊

Dashboard inteligente de vendas com análise de dados em tempo real e assistente de IA integrado.

## 🚀 Recursos

- **Dashboard Interativo**: Visualização de KPIs, gráficos e tabelas dinâmicas
- **Análise Inteligente**: IA para análise automática de dados de vendas
- **Chat com IA**: Assistente virtual para responder perguntas sobre seus dados
- **Integração Google Sheets**: Dados sempre atualizados via Apps Script
- **Interface Moderna**: Design dark com UI/UX profissional

## 📋 Pré-requisitos

- Python 3.9+
- Conta no Google (para Google Sheets)
- Chave API do OpenRouter (opcional, para IA avançada)
- Conta na Vercel (para deploy)

## 🛠️ Instalação Local

1. **Clone o repositório**
```bash
git clone <seu-repositorio>
cd "Projeto Marcelo | Agente de Vendas"
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. **Execute a aplicação**
```bash
python dashboard_app.py
```

Acesse: http://localhost:8081

## 🌐 Deploy na Vercel

### Opção 1: Deploy via CLI

1. **Instale o Vercel CLI**
```bash
npm i -g vercel
```

2. **Faça login na Vercel**
```bash
vercel login
```

3. **Configure as variáveis de ambiente**
```bash
vercel env add APPS_SCRIPT_URL
vercel env add OPENROUTER_API_KEY
```

4. **Faça o deploy**
```bash
vercel --prod
```

### Opção 2: Deploy via GitHub

1. **Conecte seu repositório no GitHub**
2. **Importe no Vercel**: https://vercel.com/new
3. **Configure as variáveis de ambiente** no dashboard da Vercel:
   - `APPS_SCRIPT_URL`: URL do seu Google Apps Script
   - `OPENROUTER_API_KEY`: Sua chave da OpenRouter

## 🔑 Variáveis de Ambiente

| Variável | Descrição | Obrigatória |
|----------|-----------|-------------|
| `APPS_SCRIPT_URL` | URL do Google Apps Script deployment | Sim |
| `OPENROUTER_API_KEY` | Chave API do OpenRouter para IA | Não* |

*Se não configurada, usa fallback local para análises

## 📊 Configuração do Google Apps Script

1. Acesse sua planilha no Google Sheets
2. Vá em **Extensões** > **Apps Script**
3. Cole o seguinte código:

```javascript
function doGet(e) {
  try {
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    const sheets = ss.getSheets();
    const result = {
      success: true,
      totalSheets: sheets.length,
      sheets: []
    };
    
    sheets.forEach(sheet => {
      const data = sheet.getDataRange().getValues();
      const headers = data[0];
      const rows = data.slice(1);
      
      const sheetData = rows.map(row => {
        const obj = {};
        headers.forEach((header, index) => {
          obj[header] = row[index];
        });
        return obj;
      });
      
      result.sheets.push({
        name: sheet.getName(),
        gid: sheet.getSheetId(),
        columns: headers,
        data: sheetData
      });
    });
    
    return ContentService.createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (error) {
    return ContentService.createTextOutput(JSON.stringify({
      success: false,
      error: error.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}
```

4. **Deploy**:
   - Clique em **Implantar** > **Nova implantação**
   - Tipo: **Aplicativo da Web**
   - Executar como: **Eu**
   - Quem tem acesso: **Qualquer pessoa**
   - Copie a URL fornecida

5. **Configure no .env**:
```bash
APPS_SCRIPT_URL=https://script.google.com/macros/s/SEU_SCRIPT_ID/exec
```

## 📁 Estrutura do Projeto

```
Projeto Marcelo | Agente de Vendas/
├── dashboard_app.py           # Aplicação Flask principal
├── api_openrouter.py          # Cliente API OpenRouter
├── apps_script_service.py     # Serviço Google Apps Script
├── requirements.txt           # Dependências Python
├── vercel.json               # Configuração Vercel
├── .env.example              # Exemplo de variáveis
├── .gitignore                # Arquivos ignorados
├── .vercelignore             # Arquivos ignorados no deploy
└── templates/
    └── modern_dashboard.html  # Interface do dashboard
```

## 🎯 Funcionalidades

### Dashboard Principal
- KPIs em tempo real (Receita, Vendas, Produtos, Regiões)
- Gráfico de vendas mensais
- Tabelas interativas por categoria, região e produtos
- Filtros temporais (3, 6, 12 meses)

### Assistente IA
- **Análise Automática**: Gera insights automáticos dos dados
- **Chat Interativo**: Faça perguntas sobre seus dados
- **Respostas Inteligentes**: IA treinada em análise de vendas
- **Markdown Support**: Respostas formatadas e organizadas

### Integrações
- Google Sheets via Apps Script
- OpenRouter AI (modelos gratuitos incluídos)
- Atualização automática a cada 5 minutos

## 🔧 Desenvolvimento

### Executar localmente
```bash
python dashboard_app.py
```

### Testar com porta específica
```bash
python dashboard_app.py --port 8080
```

### Atualizar dependências
```bash
pip freeze > requirements.txt
```

## 🐛 Troubleshooting

### Erro: "URL do Apps Script não configurada"
- Verifique se a variável `APPS_SCRIPT_URL` está configurada no `.env`
- Confirme que a URL está correta e acessível

### Erro: "Nenhum dado encontrado"
- Verifique se sua planilha tem dados
- Confirme que o Apps Script está implantado corretamente
- Teste a URL do Apps Script no navegador

### Erro de IA: "Modelo não disponível"
- A aplicação usa fallback local automaticamente
- Verifique a chave `OPENROUTER_API_KEY` se quiser usar IA externa

## 📝 License

MIT License - veja [LICENSE](LICENSE) para detalhes

## 👤 Autor

**Marcelo Vendas**
- GitHub: [@Wellychon](https://github.com/Wellychon)

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.

---

**Feito com ❤️ para otimizar análise de vendas**

