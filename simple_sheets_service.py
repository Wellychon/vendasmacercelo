"""
Serviço simplificado para acessar planilhas do Google Sheets
sem necessidade de credenciais complexas
"""
import requests
import pandas as pd
from datetime import datetime
import json

class SimpleSheetsService:
    def __init__(self):
        # ID da planilha extraído do link
        self.spreadsheet_id = "1Kmis7paV6a6z3yazvGGS85D0sKB168Om"
        
    def get_sheet_data_csv(self, sheet_id="0"):
        """
        Obtém dados da planilha via CSV público
        """
        try:
            # URL para exportar como CSV
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&gid={sheet_id}"
            
            print(f"🔗 Tentando acessar: {csv_url}")
            
            # Headers para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Faz a requisição
            response = requests.get(csv_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Lê o CSV
                from io import StringIO
                csv_data = StringIO(response.text)
                df = pd.read_csv(csv_data)
                
                print(f"✅ Dados obtidos com sucesso! {len(df)} registros")
                return df
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"Resposta: {response.text[:200]}...")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao acessar planilha: {e}")
            return None
    
    def get_sheet_data_public(self):
        """
        Tenta acessar a planilha como público
        """
        try:
            # URL da planilha pública
            public_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit#gid=0"
            
            print(f"🔗 Tentando acessar planilha pública...")
            
            # Headers para simular um navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
            }
            
            # Faz a requisição
            response = requests.get(public_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print("✅ Planilha acessível como pública!")
                # Tenta extrair dados da página HTML (método alternativo)
                return self._extract_data_from_html(response.text)
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao acessar planilha pública: {e}")
            return None
    
    def _extract_data_from_html(self, html_content):
        """
        Extrai dados do HTML da planilha (método alternativo)
        """
        try:
            # Procura por dados JSON na página
            import re
            
            # Padrão para encontrar dados da planilha
            pattern = r'window\._docs_initialData\s*=\s*({.*?});'
            match = re.search(pattern, html_content, re.DOTALL)
            
            if match:
                data_json = match.group(1)
                data = json.loads(data_json)
                print("✅ Dados extraídos do HTML!")
                return self._parse_google_sheets_data(data)
            else:
                print("⚠️ Não foi possível extrair dados do HTML")
                return None
                
        except Exception as e:
            print(f"❌ Erro ao extrair dados do HTML: {e}")
            return None
    
    def _parse_google_sheets_data(self, data):
        """
        Converte dados do Google Sheets para DataFrame
        """
        try:
            # Navega pela estrutura de dados do Google Sheets
            sheets = data.get('sheets', [])
            if not sheets:
                return None
            
            # Pega a primeira planilha
            sheet = sheets[0]
            rows = sheet.get('data', [{}])[0].get('rowData', [])
            
            if not rows:
                return None
            
            # Extrai os dados das linhas
            data_rows = []
            for row in rows:
                values = row.get('values', [])
                if values:
                    row_data = []
                    for cell in values:
                        cell_value = cell.get('formattedValue', '')
                        row_data.append(cell_value)
                    data_rows.append(row_data)
            
            if not data_rows:
                return None
            
            # Cria DataFrame
            df = pd.DataFrame(data_rows[1:], columns=data_rows[0])
            print(f"✅ DataFrame criado com {len(df)} registros")
            return df
            
        except Exception as e:
            print(f"❌ Erro ao processar dados: {e}")
            return None
    
    def get_latest_data(self):
        """
        Obtém os dados mais recentes usando o melhor método disponível
        """
        print("🔄 Tentando acessar planilha...")
        
        # Tenta primeiro via CSV
        df = self.get_sheet_data_csv()
        if df is not None and not df.empty:
            df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return df
        
        # Se não funcionar, tenta como público
        print("🔄 Tentando método alternativo...")
        df = self.get_sheet_data_public()
        if df is not None and not df.empty:
            df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return df
        
        print("❌ Não foi possível acessar a planilha")
        return None

# Instância global do serviço
simple_sheets_service = SimpleSheetsService()
