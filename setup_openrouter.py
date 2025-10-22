#!/usr/bin/env python3
"""
Script para configurar a API do OpenRouter
"""

import os
import sys

def setup_openrouter():
    """Configura a API do OpenRouter"""
    print("🔑 Configuração da API OpenRouter")
    print("=" * 50)
    print()
    print("Para usar IA real no chat, você precisa de uma chave válida do OpenRouter.")
    print()
    print("📋 Passos para obter uma chave:")
    print("1. Acesse: https://openrouter.ai/")
    print("2. Clique em 'Sign Up' ou 'Login'")
    print("3. Crie uma conta ou faça login")
    print("4. Vá em 'API Keys' no menu")
    print("5. Clique em 'Create Key'")
    print("6. Copie a nova chave")
    print()
    
    api_key = input("🔑 Cole sua chave de API aqui (ou pressione Enter para pular): ").strip()
    
    if api_key:
        # Atualiza o arquivo api_openrouter.py
        try:
            with open('api_openrouter.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Substitui a chave antiga pela nova
            import re
            pattern = r'API_KEY = "[^"]*"'
            new_key_line = f'API_KEY = "{api_key}"'
            new_content = re.sub(pattern, new_key_line, content)
            
            with open('api_openrouter.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Chave de API atualizada com sucesso!")
            print("🔄 Reinicie o servidor para aplicar as mudanças.")
            
            # Testa a nova chave
            print("\n🧪 Testando a nova chave...")
            test_api_key(api_key)
            
        except Exception as e:
            print(f"❌ Erro ao atualizar chave: {e}")
    else:
        print("⏭️ Pulando configuração da API.")
        print("💡 O chat funcionará com análise local inteligente.")

def test_api_key(api_key):
    """Testa se a chave de API funciona"""
    try:
        from openai import OpenAI
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://localhost", 
                "X-Title": "Bot Consultor de planilha", 
            },
            model="deepseek/deepseek-chat-v3.1:free",
            messages=[
                {
                    "role": "user",
                    "content": "teste"
                }
            ],
            max_tokens=10
        )
        
        print("✅ Chave de API funcionando!")
        print("🎉 Chat com IA real ativado!")
        
    except Exception as e:
        print(f"❌ Erro ao testar chave: {e}")
        print("⚠️ Verifique se a chave está correta e tem créditos disponíveis.")

if __name__ == "__main__":
    setup_openrouter()
