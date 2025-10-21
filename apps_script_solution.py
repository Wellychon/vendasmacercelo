"""
Solução usando Google Apps Script para acessar planilhas privadas
"""
import requests
import pandas as pd
from datetime import datetime
import json

class AppsScriptService:
    def __init__(self):
        # ID da planilha
        self.spreadsheet_id = "1B0k2LbBkGCUu4lmR4P67xx7OjQ5HXbsr6JrLwEiRUIM"
        
    def get_apps_script_url(self):
        """
        Retorna a URL do Google Apps Script que você precisa criar
        """
        return f"https://script.google.com/macros/s/YOUR_SCRIPT_ID/exec"
    
    def create_apps_script_code(self):
        """
        Gera o código do Google Apps Script
        """
        script_code = f"""
function doGet() {{
  try {{
    // Abre a planilha
    var spreadsheet = SpreadsheetApp.openById('{self.spreadsheet_id}');
    var sheet = spreadsheet.getActiveSheet();
    
    // Obtém todos os dados
    var data = sheet.getDataRange().getValues();
    
    // Converte para JSON
    var result = {{
      success: true,
      data: data,
      timestamp: new Date().toISOString(),
      totalRows: data.length
    }};
    
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
"""
        return script_code
    
    def get_latest_data(self):
        """
        Obtém dados via Google Apps Script
        """
        print("🔄 Buscando dados via Google Apps Script...")
        
        # URL do Apps Script (você precisa criar e colocar aqui)
        script_url = self.get_apps_script_url()
        
        if "YOUR_SCRIPT_ID" in script_url:
            print("⚠️ Google Apps Script não configurado ainda")
            self.show_setup_instructions()
            return None
        
        try:
            response = requests.get(script_url, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    # Converte para DataFrame
                    rows = data.get('data', [])
                    if len(rows) > 1:
                        df = pd.DataFrame(rows[1:], columns=rows[0])
                        df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print(f"✅ Dados obtidos! {len(df)} registros")
                        return df
                    else:
                        print("⚠️ Planilha vazia")
                        return None
                else:
                    print(f"❌ Erro no Apps Script: {data.get('error')}")
                    return None
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def show_setup_instructions(self):
        """
        Mostra instruções para configurar o Google Apps Script
        """
        print("\n" + "="*70)
        print("🔧 CONFIGURAÇÃO DO GOOGLE APPS SCRIPT")
        print("="*70)
        print("1. Acesse: https://script.google.com/")
        print("2. Clique em 'Novo Projeto'")
        print("3. Cole o código abaixo na função:")
        print("4. Salve o projeto (Ctrl+S)")
        print("5. Clique em 'Implantar' > 'Nova Implantação'")
        print("6. Selecione 'Tipo: Aplicativo Web'")
        print("7. Execute como: 'Eu'")
        print("8. Quem tem acesso: 'Qualquer pessoa'")
        print("9. Clique em 'Implantar'")
        print("10. Copie a URL gerada")
        print("11. Substitua 'YOUR_SCRIPT_ID' no arquivo apps_script_solution.py")
        print("\n📋 CÓDIGO DO APPS SCRIPT:")
        print("-" * 50)
        print(self.create_apps_script_code())
        print("-" * 50)
        print("="*70)

# Instância global
apps_script_service = AppsScriptService()
