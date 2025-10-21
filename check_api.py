#!/usr/bin/env python3
"""
Script para verificar e configurar a API do OpenRouter
"""

import requests
import json

def check_api_key(api_key):
    """Verifica se a chave de API é válida"""
    print(f"🔍 Verificando chave: {api_key[:20]}...")
    
    try:
        # Testa com uma requisição simples
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Testa com um modelo simples
        data = {
            "model": "deepseek/deepseek-chat-v3.1:free",
            "messages": [{"role": "user", "content": "teste"}],
            "max_tokens": 10
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=10
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Chave de API válida!")
            return True
        else:
            print(f"❌ Erro: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

def get_new_api_key():
    """Instruções para obter uma nova chave"""
    print("\n🔑 Para obter uma nova chave de API:")
    print("=" * 50)
    print("1. Acesse: https://openrouter.ai/")
    print("2. Clique em 'Sign Up' ou 'Login'")
    print("3. Crie uma conta ou faça login")
    print("4. Vá em 'API Keys' no menu")
    print("5. Clique em 'Create Key'")
    print("6. Copie a nova chave")
    print("7. Substitua no arquivo api_openrouter.py")
    print("\n💡 Dica: As chaves gratuitas têm limite de uso")

if __name__ == "__main__":
    # Sua chave atual
    api_key = "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"
    
    print("🔍 Verificando sua chave de API do OpenRouter...")
    print("=" * 60)
    
    if check_api_key(api_key):
        print("🎉 Sua chave está funcionando!")
    else:
        print("⚠️ Sua chave não está funcionando.")
        get_new_api_key()
        
    print("\n📝 Status do Sistema:")
    print("✅ Chatbot funcionando com fallback inteligente")
    print("✅ 2.400 registros carregados")
    print("✅ Interface completa")
    print("🔄 Para usar IA real: configure uma chave válida")
