"""
Entry point otimizado para Vercel
"""
from dashboard_app import app

# Para o Vercel, precisamos expor o app Flask
handler = app

# Também podemos usar diretamente
if __name__ == "__main__":
    app.run()
