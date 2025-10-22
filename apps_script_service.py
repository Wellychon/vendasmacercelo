"""
Serviço para acessar dados via Google Apps Script
"""
import requests
import pandas as pd
from datetime import datetime
import json
import os
import dotenv

# Carrega variáveis de ambiente
dotenv.load_dotenv()

class AppsScriptService:
    def __init__(self):
        self.spreadsheet_id = "1B0k2LbBkGCUu4lmR4P67xx7OjQ5HXbsr6JrLwEiRUIM"
        self.script_url = self.load_script_url()
        
    def load_script_url(self):
        """
        Carrega a URL do Apps Script da variável de ambiente
        """
        # Tenta carregar do .env primeiro
        url = os.getenv('APPS_SCRIPT_URL')
        
        if url and 'script.google.com' in url:
            return url
        
        # Fallback: tenta carregar do arquivo (retrocompatibilidade)
        try:
            if os.path.exists('apps_script_url.txt'):
                with open('apps_script_url.txt', 'r') as f:
                    url = f.read().strip()
                    if url and 'script.google.com' in url:
                        return url
        except:
            pass
        
        return None
    
    def save_script_url(self, url):
        """
        Salva a URL do Apps Script (apenas para retrocompatibilidade)
        """
        try:
            with open('apps_script_url.txt', 'w') as f:
                f.write(url)
            return True
        except:
            return False
    
    def get_latest_data(self):
        """
        Obtém dados via Google Apps Script
        """
        if not self.script_url:
            print("❌ URL do Apps Script não configurada!")
            print("💡 Configure APPS_SCRIPT_URL no arquivo .env")
            return None
        
        print("🔄 Buscando dados via Google Apps Script...")
        print(f"🔗 URL: {self.script_url}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'application/json',
            }
            
            response = requests.get(self.script_url, headers=headers, timeout=60)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success'):
                    print(f"✅ Apps Script funcionando!")
                    print(f"📊 {data.get('totalSheets', 0)} guias encontradas")
                    
                    # Processa os dados
                    all_sheets = {}
                    total_records = 0
                    
                    for sheet_data in data.get('sheets', []):
                        sheet_name = sheet_data.get('name', 'Unknown')
                        sheet_gid = sheet_data.get('gid', 0)
                        rows = sheet_data.get('data', [])
                        columns = sheet_data.get('columns', [])
                        
                        if rows and columns:
                            # Cria DataFrame
                            df = pd.DataFrame(rows, columns=columns)
                            df['guia'] = sheet_name
                            df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            
                            all_sheets[f"guia_{sheet_gid}"] = {
                                'nome': sheet_name,
                                'gid': sheet_gid,
                                'dados': df.to_dict('records'),
                                'total_registros': len(df),
                                'colunas': df.columns.tolist()
                            }
                            
                            total_records += len(df)
                            print(f"✅ {sheet_name}: {len(df)} registros")
                    
                    print(f"📈 Total: {total_records} registros em {len(all_sheets)} guias")
                    return all_sheets if all_sheets else None
                else:
                    print(f"❌ Erro no Apps Script: {data.get('error')}")
                    return None
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"Resposta: {response.text[:200]}...")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def test_connection(self):
        """
        Testa a conexão com o Apps Script
        """
        if not self.script_url:
            return False, "URL não configurada"
        
        try:
            response = requests.get(self.script_url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return True, f"Conectado! {data.get('totalSheets', 0)} guias disponíveis"
                else:
                    return False, f"Erro: {data.get('error')}"
            else:
                return False, f"HTTP {response.status_code}"
        except Exception as e:
            return False, f"Erro: {e}"

# Instância global
apps_script_service = AppsScriptService()
