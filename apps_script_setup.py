"""
Configuração completa do Google Apps Script para acessar a planilha
"""
import json

def create_apps_script_code():
    """
    Gera o código do Google Apps Script
    """
    spreadsheet_id = "1B0k2LbBkGCUu4lmR4P67xx7OjQ5HXbsr6JrLwEiRUIM"
    
    script_code = f"""
function doGet() {{
  try {{
    // Abre a planilha
    var spreadsheet = SpreadsheetApp.openById('{spreadsheet_id}');
    var sheets = spreadsheet.getSheets();
    
    var result = {{
      success: true,
      timestamp: new Date().toISOString(),
      totalSheets: sheets.length,
      sheets: []
    }};
    
    // Processa cada guia
    for (var i = 0; i < sheets.length; i++) {{
      var sheet = sheets[i];
      var data = sheet.getDataRange().getValues();
      
      if (data.length > 1) {{ // Se tem dados (mais que apenas cabeçalho)
        var sheetData = {{
          name: sheet.getName(),
          gid: sheet.getSheetId(),
          totalRows: data.length - 1, // Exclui cabeçalho
          columns: data[0], // Primeira linha são os cabeçalhos
          data: data.slice(1) // Dados sem cabeçalho
        }};
        
        result.sheets.push(sheetData);
      }}
    }}
    
    return ContentService
      .createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
      
  }} catch (error) {{
    var result = {{
      success: false,
      error: error.toString(),
      timestamp: new Date().toISOString()
    }};
    
    return ContentService
      .createTextOutput(JSON.stringify(result))
      .setMimeType(ContentService.MimeType.JSON);
  }}
}}

function doPost(e) {{
  // Para requisições POST, retorna os mesmos dados
  return doGet();
}}
"""
    return script_code

def show_setup_instructions():
    """
    Mostra instruções detalhadas para configurar o Google Apps Script
    """
    print("🔧 CONFIGURAÇÃO DO GOOGLE APPS SCRIPT")
    print("=" * 70)
    print("📋 PASSO A PASSO:")
    print("=" * 70)
    print()
    print("1️⃣ ACESSE O GOOGLE APPS SCRIPT:")
    print("   🌐 https://script.google.com/")
    print("   👤 Faça login com sua conta Google")
    print()
    print("2️⃣ CRIE UM NOVO PROJETO:")
    print("   ➕ Clique em 'Novo Projeto'")
    print("   📝 Renomeie para 'Dashboard Vendas API'")
    print()
    print("3️⃣ COLE O CÓDIGO:")
    print("   📋 Copie o código abaixo")
    print("   📝 Cole na função (substitua o código existente)")
    print("   💾 Salve (Ctrl+S)")
    print()
    print("4️⃣ IMPLANTE O PROJETO:")
    print("   🚀 Clique em 'Implantar' > 'Nova Implantação'")
    print("   ⚙️  Tipo: 'Aplicativo Web'")
    print("   👤 Execute como: 'Eu'")
    print("   🌍 Quem tem acesso: 'Qualquer pessoa'")
    print("   🚀 Clique em 'Implantar'")
    print()
    print("5️⃣ COPIE A URL:")
    print("   📋 Copie a URL gerada")
    print("   📝 Cole no arquivo 'apps_script_url.txt'")
    print()
    print("📋 CÓDIGO DO APPS SCRIPT:")
    print("-" * 50)
    print(create_apps_script_code())
    print("-" * 50)
    print()
    print("✅ APÓS CONFIGURAR:")
    print("   🔄 Execute: python3 test_apps_script.py")
    print("   🌐 Acesse: http://localhost:8080")
    print("=" * 70)

if __name__ == "__main__":
    show_setup_instructions()
