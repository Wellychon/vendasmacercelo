"""
Serviço híbrido que tenta múltiplos métodos para acessar a planilha
"""
import requests
import pandas as pd
from datetime import datetime
import json

class HybridSheetsService:
    def __init__(self):
        # ID da planilha
        self.spreadsheet_id = "1B0k2LbBkGCUu4lmR4P67xx7OjQ5HXbsr6JrLwEiRUIM"
        
    def method_1_public_csv(self):
        """
        Método 1: Acesso via CSV público
        """
        try:
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&gid=0"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
            }
            
            response = requests.get(csv_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                from io import StringIO
                csv_data = StringIO(response.text)
                df = pd.read_csv(csv_data)
                
                if not df.empty:
                    print("✅ Método 1 (CSV Público): Sucesso!")
                    return df
                    
        except Exception as e:
            print(f"❌ Método 1 falhou: {e}")
            
        return None
    
    def method_2_public_html(self):
        """
        Método 2: Acesso via HTML público
        """
        try:
            public_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            response = requests.get(public_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Procura por dados JSON na página
                import re
                pattern = r'window\._docs_initialData\s*=\s*({.*?});'
                match = re.search(pattern, response.text, re.DOTALL)
                
                if match:
                    data_json = match.group(1)
                    data = json.loads(data_json)
                    
                    # Extrai dados da planilha
                    sheets = data.get('sheets', [])
                    if sheets:
                        sheet = sheets[0]
                        rows = sheet.get('data', [{}])[0].get('rowData', [])
                        
                        if rows:
                            data_rows = []
                            for row in rows:
                                values = row.get('values', [])
                                if values:
                                    row_data = [cell.get('formattedValue', '') for cell in values]
                                    data_rows.append(row_data)
                            
                            if data_rows:
                                df = pd.DataFrame(data_rows[1:], columns=data_rows[0])
                                print("✅ Método 2 (HTML Público): Sucesso!")
                                return df
                                
        except Exception as e:
            print(f"❌ Método 2 falhou: {e}")
            
        return None
    
    def method_3_direct_api(self, gid=0):
        """
        Método 3: Tentativa de acesso direto à API para uma guia específica
        """
        try:
            # URL alternativa para dados de uma guia específica
            api_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/gviz/tq?tqx=out:csv&gid={gid}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
            }
            
            response = requests.get(api_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                from io import StringIO
                csv_data = StringIO(response.text)
                df = pd.read_csv(csv_data)
                
                if not df.empty:
                    print(f"✅ Método 3 (API Direta) - Guia {gid}: Sucesso!")
                    return df
                    
        except Exception as e:
            print(f"❌ Método 3 falhou para guia {gid}: {e}")
            
        return None
    
    def get_all_sheets_data(self):
        """
        Obtém dados de todas as 12 guias da planilha
        """
        print("🔄 Buscando dados de todas as 12 guias...")
        print("=" * 60)
        
        all_data = {}
        successful_sheets = 0
        
        # Tenta acessar cada guia (0 a 11)
        for gid in range(12):
            print(f"\n📊 Processando guia {gid + 1}/12...")
            
            # Tenta o método da API direta para cada guia
            df = self.method_3_direct_api(gid)
            
            if df is not None and not df.empty:
                # Adiciona informações da guia
                df['guia'] = f"vendas_{gid + 1:02d}_2025"
                df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                all_data[f"guia_{gid}"] = {
                    'nome': f"vendas_{gid + 1:02d}_2025",
                    'gid': gid,
                    'dados': df.to_dict('records'),
                    'total_registros': len(df),
                    'colunas': df.columns.tolist()
                }
                
                successful_sheets += 1
                print(f"✅ Guia {gid + 1}: {len(df)} registros")
            else:
                print(f"⚠️ Guia {gid + 1}: Sem dados ou inacessível")
        
        print(f"\n📈 RESUMO:")
        print(f"✅ Guias com dados: {successful_sheets}/12")
        print(f"📊 Total de registros: {sum(sheet['total_registros'] for sheet in all_data.values())}")
        
        return all_data if successful_sheets > 0 else None
    
    def get_latest_data(self):
        """
        Obtém dados de todas as guias da planilha
        """
        # Primeiro tenta obter todas as guias
        all_sheets = self.get_all_sheets_data()
        
        if all_sheets:
            return all_sheets
        
        # Se não conseguir todas as guias, tenta métodos individuais
        print("🔄 Tentando métodos individuais...")
        
        # Lista de métodos para tentar
        methods = [
            ("CSV Público", self.method_1_public_csv),
            ("HTML Público", self.method_2_public_html),
            ("API Direta", lambda: self.method_3_direct_api(0)),
        ]
        
        for method_name, method_func in methods:
            print(f"\n🔍 Tentando: {method_name}")
            df = method_func()
            
            if df is not None and not df.empty:
                df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"🎉 Sucesso com {method_name}!")
                print(f"📊 {len(df)} registros obtidos")
                return df
        
        # Se nenhum método funcionou
        print("\n" + "="*60)
        print("❌ NENHUM MÉTODO FUNCIONOU")
        print("="*60)
        print("💡 SOLUÇÕES POSSÍVEIS:")
        print("1. Torne a planilha pública (mais simples)")
        print("2. Use Google Apps Script (mais seguro)")
        print("3. Configure credenciais do Google Cloud")
        print("\n🔓 PARA TORNAR PÚBLICA:")
        print("1. Abra a planilha no Google Sheets")
        print("2. Clique em 'Compartilhar'")
        print("3. 'Alterar para qualquer pessoa com o link'")
        print("4. Selecione 'Visualizador'")
        print("5. Clique em 'Concluído'")
        print("="*60)
        
        return None

# Instância global
hybrid_sheets_service = HybridSheetsService()
