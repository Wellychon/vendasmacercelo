import sys
import os

# Adiciona o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa a aplicação Flask
from dashboard_app import app

# Exporta para Vercel
app = app

