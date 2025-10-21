"""
Solução para acessar planilhas do Google Sheets sem credenciais
Funciona com planilhas públicas ou que podem ser tornadas públicas
"""
import requests
import pandas as pd
from datetime import datetime
import json

class PublicSheetsService:
    def __init__(self):
        # ID da planilha
        self.spreadsheet_id = "1B0k2LbBkGCUu4lmR4P67xx7OjQ5HXbsr6JrLwEiRUIM"
        
    def make_public_and_access(self):
        """
        Instruções para tornar a planilha pública e acessá-la
        """
        print("🔓 INSTRUÇÕES PARA TORNAR A PLANILHA PÚBLICA:")
        print("=" * 60)
        print("1. Abra sua planilha no Google Sheets")
        print("2. Clique em 'Compartilhar' (canto superior direito)")
        print("3. Clique em 'Alterar para qualquer pessoa com o link'")
        print("4. Selecione 'Visualizador'")
        print("5. Clique em 'Concluído'")
        print("6. Execute novamente este script")
        print("=" * 60)
        
        return None
    
    def get_public_sheet_data(self):
        """
        Acessa planilha pública via CSV
        """
        try:
            # URL para exportar como CSV (funciona apenas com planilhas públicas)
            csv_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/export?format=csv&gid=0"
            
            print(f"🔗 Acessando: {csv_url}")
            
            # Headers para simular navegador
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/csv,text/plain,*/*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            }
            
            # Faz a requisição
            response = requests.get(csv_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                # Lê o CSV
                from io import StringIO
                csv_data = StringIO(response.text)
                df = pd.read_csv(csv_data)
                
                if not df.empty:
                    print(f"✅ Dados obtidos! {len(df)} registros")
                    df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    return df
                else:
                    print("⚠️ Planilha vazia")
                    return None
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                if response.status_code == 400:
                    print("💡 A planilha precisa ser pública para este método funcionar")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def get_sheet_data_alternative(self):
        """
        Método alternativo usando API pública do Google Sheets
        """
        try:
            # URL da planilha pública
            public_url = f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}/edit"
            
            print(f"🔗 Tentando método alternativo...")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            
            response = requests.get(public_url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                print("✅ Planilha acessível!")
                # Aqui você poderia implementar parsing do HTML
                # Mas é mais complexo, então vamos focar no método CSV
                return None
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Erro: {e}")
            return None
    
    def get_latest_data(self):
        """
        Obtém dados usando o melhor método disponível
        """
        print("🔄 Buscando dados da planilha...")
        
        # Tenta primeiro o método CSV (mais confiável)
        df = self.get_public_sheet_data()
        if df is not None:
            return df
        
        # Se não funcionar, mostra instruções
        print("\n" + "="*60)
        print("❌ NÃO FOI POSSÍVEL ACESSAR A PLANILHA")
        print("="*60)
        self.make_public_and_access()
        return None

# Instância global
public_sheets_service = PublicSheetsService()
