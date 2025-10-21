"""
Agente de Vendas - API para Vercel
Versão otimizada para serverless
"""

from flask import Flask, jsonify, request
import json
from datetime import datetime
import os
import sys

# Adicionar diretório pai ao path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Imports locais
try:
    from apps_script_service import apps_script_service
    from api_openrouter import consultar_ia
    import pandas as pd
except ImportError as e:
    print(f"Import error: {e}")
    # Fallback para desenvolvimento
    apps_script_service = None
    consultar_ia = None
    pd = None

app = Flask(__name__)

# Cache global para dados
cached_data = None
last_update = None

def update_data():
    """Atualiza os dados da planilha"""
    global cached_data, last_update
    
    try:
        if apps_script_service:
            print("Atualizando dados da planilha...")
            data = apps_script_service.get_latest_data()
            
            if data is not None:
                if isinstance(data, dict):
                    cached_data = data
                    total_records = sum(sheet['total_registros'] for sheet in data.values())
                    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Dados atualizados: {len(data)} guias com {total_records} registros")
                else:
                    cached_data = data.to_dict('records') if hasattr(data, 'to_dict') else data
                    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Dados atualizados: {len(cached_data)} registros")
            else:
                print("Nenhum dado encontrado")
                cached_data = []
        else:
            # Dados mock para desenvolvimento
            cached_data = [
                {
                    "Cliente": "Cliente Teste",
                    "Produto": "Produto A",
                    "Receita Total": "1000.00",
                    "Quantidade": 5,
                    "Região": "São Paulo",
                    "Categoria": "Categoria A",
                    "Vendedor": "Vendedor 1",
                    "Data": "2024-01-15"
                }
            ]
            last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("Usando dados mock para desenvolvimento")
                
    except Exception as e:
        print(f"Erro ao atualizar dados: {e}")
        cached_data = []

def get_analysis():
    """Obtém análise dos dados usando IA"""
    try:
        if not cached_data:
            return "Nenhum dado disponível para análise."
        
        # Análise básica dos dados
        if isinstance(cached_data, dict):
            all_data = []
            for sheet_data in cached_data.values():
                if 'dados' in sheet_data and isinstance(sheet_data['dados'], list):
                    all_data.extend(sheet_data['dados'])
        else:
            all_data = cached_data
        
        if not all_data:
            return "Nenhum dado disponível para análise."
        
        # Análise simples
        total_records = len(all_data)
        total_revenue = 0
        
        for row in all_data:
            try:
                revenue = float(str(row.get('Receita Total', '0')).replace(',', '.').replace('R$', '').strip()) or 0
                total_revenue += revenue
            except (ValueError, TypeError):
                pass
        
        avg_ticket = total_revenue / total_records if total_records > 0 else 0
        
        analysis = f"""# 📊 Análise de Vendas

## Métricas Principais
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {avg_ticket:,.2f}
- **Última Atualização**: {last_update}

## Insights
- Base de dados sólida com {total_records:,} transações
- Receita total de R$ {total_revenue:,.2f}
- Ticket médio de R$ {avg_ticket:,.2f}

*Análise gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        
        return analysis
        
    except Exception as e:
        return f"Erro na análise: {e}"

@app.route('/')
def index():
    """Página principal"""
    return jsonify({
        "message": "Agente de Vendas API",
        "version": "1.0.0",
        "status": "online",
        "endpoints": {
            "/api/data": "Dados da planilha",
            "/api/analysis": "Análise dos dados",
            "/api/chat": "Chat com IA",
            "/api/update": "Atualizar dados"
        }
    })

@app.route('/api/data')
def get_data():
    """API para obter dados da planilha"""
    global cached_data, last_update
    
    if cached_data is None:
        update_data()
    
    if isinstance(cached_data, dict):
        return jsonify({
            'data': cached_data,
            'last_update': last_update,
            'total_sheets': len(cached_data),
            'total_records': sum(sheet['total_registros'] for sheet in cached_data.values()),
            'sheets_info': {k: {'nome': v['nome'], 'registros': v['total_registros']} for k, v in cached_data.items()}
        })
    else:
        return jsonify({
            'data': cached_data or [],
            'last_update': last_update,
            'count': len(cached_data) if cached_data else 0
        })

@app.route('/api/update', methods=['POST'])
def update_data_endpoint():
    """API para forçar atualização dos dados"""
    try:
        update_data()
        
        if isinstance(cached_data, dict):
            return jsonify({
                'success': True,
                'message': 'Dados atualizados com sucesso!',
                'last_update': last_update,
                'total_sheets': len(cached_data),
                'total_records': sum(sheet['total_registros'] for sheet in cached_data.values())
            })
        else:
            return jsonify({
                'success': True,
                'message': 'Dados atualizados com sucesso!',
                'last_update': last_update,
                'count': len(cached_data) if cached_data else 0
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar dados: {str(e)}'
        }), 500

@app.route('/api/analysis', methods=['GET', 'POST'])
def get_analysis_endpoint():
    """API para obter análise dos dados"""
    try:
        analysis = get_analysis()
        return jsonify({
            'analysis': analysis,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'error': f'Erro ao gerar análise: {str(e)}'
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """API para chat com IA"""
    try:
        data = request.get_json()
        user_message = data.get('message', '') if data else ''
        
        if not user_message:
            return jsonify({
                'error': 'Mensagem não fornecida'
            }), 400
        
        # Resposta simples para desenvolvimento
        if not consultar_ia:
            return jsonify({
                'response': f"Olá! Recebi sua mensagem: '{user_message}'. A IA está em modo de desenvolvimento.",
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        # Usar IA real se disponível
        try:
            context = f"Dados disponíveis: {len(cached_data) if cached_data else 0} registros"
            prompt = f"Contexto: {context}\nPergunta: {user_message}\nResponda em português:"
            ai_response = consultar_ia(prompt)
        except Exception as e:
            ai_response = f"Erro na IA: {e}. Mensagem recebida: {user_message}"
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar mensagem: {str(e)}'
        }), 500

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'data_loaded': cached_data is not None
    })

# Inicializar dados na primeira execução
if __name__ == '__main__':
    print("Inicializando Agente de Vendas API...")
    update_data()
    print("API pronta!")
else:
    # Para Vercel, inicializar dados
    update_data()
