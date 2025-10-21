"""
Script para configurar as credenciais do Google Sheets API
"""
import os
import json

def create_credentials_template():
    """Cria um template para as credenciais do Google Sheets"""
    
    print("🔧 Configuração das Credenciais do Google Sheets API")
    print("=" * 50)
    
    print("\n📋 Para acessar a planilha do Google Drive, você precisa:")
    print("1. Criar um projeto no Google Cloud Console")
    print("2. Habilitar a Google Sheets API e Google Drive API")
    print("3. Criar uma conta de serviço")
    print("4. Baixar o arquivo JSON de credenciais")
    
    print("\n🌐 Links úteis:")
    print("• Google Cloud Console: https://console.cloud.google.com/")
    print("• Google Sheets API: https://developers.google.com/sheets/api")
    print("• Google Drive API: https://developers.google.com/drive/api")
    
    print("\n📝 Instruções detalhadas:")
    print("1. Acesse o Google Cloud Console")
    print("2. Crie um novo projeto ou selecione um existente")
    print("3. Vá para 'APIs e Serviços' > 'Biblioteca'")
    print("4. Procure e habilite 'Google Sheets API' e 'Google Drive API'")
    print("5. Vá para 'APIs e Serviços' > 'Credenciais'")
    print("6. Clique em 'Criar Credenciais' > 'Conta de Serviço'")
    print("7. Preencha os detalhes da conta de serviço")
    print("8. Na aba 'Chaves', clique em 'Adicionar Chave' > 'JSON'")
    print("9. Baixe o arquivo JSON e renomeie para 'credentials.json'")
    print("10. Coloque o arquivo 'credentials.json' na pasta do projeto")
    
    print("\n🔐 Alternativa - Variáveis de Ambiente:")
    print("Você também pode configurar as credenciais usando variáveis de ambiente:")
    print("export GOOGLE_PROJECT_ID='seu-project-id'")
    print("export GOOGLE_PRIVATE_KEY_ID='sua-private-key-id'")
    print("export GOOGLE_PRIVATE_KEY='sua-private-key'")
    print("export GOOGLE_CLIENT_EMAIL='sua-client-email'")
    print("export GOOGLE_CLIENT_ID='seu-client-id'")
    print("export GOOGLE_CLIENT_X509_CERT_URL='sua-cert-url'")
    
    print("\n📁 Estrutura do arquivo credentials.json:")
    credentials_template = {
        "type": "service_account",
        "project_id": "seu-project-id",
        "private_key_id": "sua-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nsua-private-key\n-----END PRIVATE KEY-----\n",
        "client_email": "sua-conta-servico@seu-project.iam.gserviceaccount.com",
        "client_id": "seu-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/sua-conta-servico%40seu-project.iam.gserviceaccount.com"
    }
    
    print(json.dumps(credentials_template, indent=2))
    
    print("\n✅ Após configurar as credenciais, execute:")
    print("python dashboard_app.py")
    
    print("\n🚀 O dashboard estará disponível em: http://localhost:5000")

if __name__ == "__main__":
    create_credentials_template()
