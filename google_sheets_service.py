import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from datetime import datetime
import os

class GoogleSheetsService:
    def __init__(self):
        # Configuração das credenciais do Google Sheets
        self.scope = [
            "https://www.googleapis.com/auth/spreadsheets.readonly",
            "https://www.googleapis.com/auth/drive.readonly"
        ]
        
        # Você precisará criar um arquivo de credenciais JSON do Google Cloud
        # e colocar o caminho aqui ou usar variáveis de ambiente
        self.credentials_file = os.getenv('GOOGLE_CREDENTIALS_FILE', 'credentials.json')
        
        # ID da planilha extraído do link do Google Drive
        self.spreadsheet_id = "1Kmis7paV6a6z3yazvGGS85D0sKB168Om"
        
        self.client = None
        self.spreadsheet = None
        
    def authenticate(self):
        """Autentica com o Google Sheets API"""
        try:
            if os.path.exists(self.credentials_file):
                creds = Credentials.from_service_account_file(
                    self.credentials_file, 
                    scopes=self.scope
                )
            else:
                # Fallback para autenticação via variáveis de ambiente
                creds_dict = {
                    "type": "service_account",
                    "project_id": os.getenv('GOOGLE_PROJECT_ID'),
                    "private_key_id": os.getenv('GOOGLE_PRIVATE_KEY_ID'),
                    "private_key": os.getenv('GOOGLE_PRIVATE_KEY').replace('\\n', '\n'),
                    "client_email": os.getenv('GOOGLE_CLIENT_EMAIL'),
                    "client_id": os.getenv('GOOGLE_CLIENT_ID'),
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                    "client_x509_cert_url": os.getenv('GOOGLE_CLIENT_X509_CERT_URL')
                }
                creds = Credentials.from_service_account_info(creds_dict, scopes=self.scope)
            
            self.client = gspread.authorize(creds)
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            return True
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return False
    
    def get_sheet_data(self, sheet_name=None):
        """Obtém dados da planilha"""
        try:
            if not self.client:
                if not self.authenticate():
                    return None
            
            # Se não especificar a planilha, pega a primeira
            if sheet_name:
                worksheet = self.spreadsheet.worksheet(sheet_name)
            else:
                worksheet = self.spreadsheet.sheet1
            
            # Obtém todos os dados da planilha
            data = worksheet.get_all_records()
            
            # Converte para DataFrame do pandas
            df = pd.DataFrame(data)
            
            return df
            
        except Exception as e:
            print(f"Erro ao obter dados da planilha: {e}")
            return None
    
    def get_sheet_names(self):
        """Obtém lista de nomes das planilhas"""
        try:
            if not self.client:
                if not self.authenticate():
                    return []
            
            worksheets = self.spreadsheet.worksheets()
            return [ws.title for ws in worksheets]
            
        except Exception as e:
            print(f"Erro ao obter nomes das planilhas: {e}")
            return []
    
    def get_latest_data(self):
        """Obtém os dados mais recentes da planilha"""
        try:
            df = self.get_sheet_data()
            if df is not None and not df.empty:
                # Adiciona timestamp da última atualização
                df['ultima_atualizacao'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return df
            return None
        except Exception as e:
            print(f"Erro ao obter dados mais recentes: {e}")
            return None

# Instância global do serviço
sheets_service = GoogleSheetsService()
