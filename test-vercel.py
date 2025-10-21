#!/usr/bin/env python3
"""
Teste da API para Vercel
"""

import requests
import json
import sys

def test_api(base_url="http://localhost:8081"):
    """Testa todos os endpoints da API"""
    
    print("🧪 Testando API do Agente de Vendas...")
    print(f"URL base: {base_url}")
    print("-" * 50)
    
    # Teste 1: Health check
    try:
        response = requests.get(f"{base_url}/api/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health Check: {data['status']}")
        else:
            print(f"❌ Health Check: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check: {e}")
    
    # Teste 2: Dados
    try:
        response = requests.get(f"{base_url}/api/data", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Dados: {data.get('count', 0)} registros")
        else:
            print(f"❌ Dados: {response.status_code}")
    except Exception as e:
        print(f"❌ Dados: {e}")
    
    # Teste 3: Análise
    try:
        response = requests.get(f"{base_url}/api/analysis", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Análise: {len(data.get('analysis', ''))} caracteres")
        else:
            print(f"❌ Análise: {response.status_code}")
    except Exception as e:
        print(f"❌ Análise: {e}")
    
    # Teste 4: Chat
    try:
        response = requests.post(
            f"{base_url}/api/chat",
            json={"message": "Olá, teste!"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Chat: {len(data.get('response', ''))} caracteres")
        else:
            print(f"❌ Chat: {response.status_code}")
    except Exception as e:
        print(f"❌ Chat: {e}")
    
    # Teste 5: Página inicial
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Inicial: {data.get('message', 'OK')}")
        else:
            print(f"❌ Inicial: {response.status_code}")
    except Exception as e:
        print(f"❌ Inicial: {e}")
    
    print("-" * 50)
    print("🎉 Teste concluído!")

if __name__ == "__main__":
    # Se passou URL como argumento, usar ela
    if len(sys.argv) > 1:
        test_api(sys.argv[1])
    else:
        test_api()
