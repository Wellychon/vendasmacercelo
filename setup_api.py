#!/usr/bin/env python3
"""
Script para configurar a API do OpenRouter
"""

def setup_api_key():
    print("🔑 Configuração da API OpenRouter")
    print("=" * 50)
    print()
    print("Para usar a API real do OpenRouter, você precisa de uma chave válida.")
    print()
    print("📋 Passos para obter uma chave:")
    print("1. Acesse: https://openrouter.ai/")
    print("2. Crie uma conta ou faça login")
    print("3. Vá em 'API Keys' no menu")
    print("4. Clique em 'Create Key'")
    print("5. Copie a chave gerada")
    print()
    
    api_key = input("🔑 Cole sua chave de API aqui: ").strip()
    
    if api_key:
        # Atualiza o arquivo de configuração
        config_content = f'''# Configuração da API OpenRouter
# Substitua pela sua chave de API válida do OpenRouter

# Para obter uma chave válida:
# 1. Acesse https://openrouter.ai/
# 2. Crie uma conta
# 3. Gere uma nova chave de API
# 4. Substitua o valor abaixo pela sua chave

OPENROUTER_API_KEY = "{api_key}"

# Instruções:
# 1. Acesse https://openrouter.ai/
# 2. Faça login ou crie uma conta
# 3. Vá em "API Keys" 
# 4. Gere uma nova chave
# 5. Substitua o valor acima pela sua chave real
'''
        
        with open('config_api.py', 'w') as f:
            f.write(config_content)
        
        print("✅ Chave de API configurada com sucesso!")
        print("🔄 Reinicie o dashboard para usar a API real.")
        
        # Testa a chave
        print("\n🧪 Testando a chave de API...")
        try:
            from api_openrouter import consultar_ia
            resposta = consultar_ia("Olá! Teste de conexão com a API.")
            print("✅ API funcionando! Resposta recebida.")
            print(f"📝 Resposta: {resposta[:100]}...")
        except Exception as e:
            print(f"❌ Erro na API: {e}")
            print("🔧 Verifique se a chave está correta.")
    else:
        print("❌ Nenhuma chave fornecida. Usando fallback local.")

if __name__ == "__main__":
    setup_api_key()
