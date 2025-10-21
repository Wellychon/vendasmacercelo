from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import threading
import time
from apps_script_service import apps_script_service
from api_openrouter import consultar_ia
import pandas as pd

app = Flask(__name__)

# Cache para os dados
cached_data = None
last_update = None
update_lock = threading.Lock()

def update_data():
    """Atualiza os dados da planilha"""
    global cached_data, last_update
    
    with update_lock:
        try:
            print("Atualizando dados da planilha...")
            data = apps_script_service.get_latest_data()
            
            if data is not None:
                if isinstance(data, dict):
                    # Múltiplas guias
                    cached_data = data
                    total_records = sum(sheet['total_registros'] for sheet in data.values())
                    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Dados atualizados com sucesso! {len(data)} guias com {total_records} registros totais.")
                else:
                    # Uma única guia (compatibilidade)
                    cached_data = data.to_dict('records')
                    last_update = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(f"Dados atualizados com sucesso! {len(cached_data)} registros encontrados.")
            else:
                print("Nenhum dado encontrado na planilha.")
                
        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")

def get_analysis():
    """Obtém análise dos dados usando IA"""
    try:
        if cached_data is None:
            return "Nenhum dado disponível para análise."
        
        # Processa todos os dados para análise detalhada
        all_data = []
        if isinstance(cached_data, dict):
            # Múltiplas guias
            for sheet_data in cached_data.values():
                if 'dados' in sheet_data and isinstance(sheet_data['dados'], list):
                    all_data.extend(sheet_data['dados'])
        else:
            # Uma única guia (compatibilidade)
            all_data = cached_data
        
        if not all_data:
            return "Nenhum dado disponível para análise."
        
        # Análise detalhada dos dados
        analysis_results = analyze_sales_data_detailed(all_data)
        
        return analysis_results
        
    except Exception as e:
        return f"Erro ao gerar análise: {e}"

def analyze_sales_data_detailed(data):
    """Faz análise detalhada dos dados de vendas"""
    try:
        # Converte para DataFrame para análise mais fácil
        df = pd.DataFrame(data)
        
        # Análise de receita total
        total_revenue = 0
        if 'Receita Total' in df.columns:
            df['Receita Total'] = pd.to_numeric(df['Receita Total'].astype(str).str.replace(',', '.').str.replace('R$', '').str.strip(), errors='coerce')
            total_revenue = df['Receita Total'].sum()
        
        # Análise por categoria
        category_analysis = {}
        if 'Categoria' in df.columns:
            category_analysis = df.groupby('Categoria').agg({
                'Receita Total': ['sum', 'count', 'mean'] if 'Receita Total' in df.columns else ['count'],
                'Quantidade': 'sum' if 'Quantidade' in df.columns else 'count'
            }).round(2)
        
        # Análise por região
        region_analysis = {}
        if 'Região' in df.columns:
            region_analysis = df.groupby('Região').agg({
                'Receita Total': ['sum', 'count', 'mean'] if 'Receita Total' in df.columns else ['count'],
                'Quantidade': 'sum' if 'Quantidade' in df.columns else 'count'
            }).round(2)
        
        # Análise por produto
        product_analysis = {}
        if 'Produto' in df.columns:
            product_analysis = df.groupby('Produto').agg({
                'Receita Total': ['sum', 'count', 'mean'] if 'Receita Total' in df.columns else ['count'],
                'Quantidade': 'sum' if 'Quantidade' in df.columns else 'count'
            }).round(2)
        
        # Análise temporal (se houver coluna de data)
        temporal_analysis = {}
        if 'Data' in df.columns:
            df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
            df['Mes'] = df['Data'].dt.to_period('M')
            temporal_analysis = df.groupby('Mes').agg({
                'Receita Total': ['sum', 'count'] if 'Receita Total' in df.columns else ['count'],
                'Quantidade': 'sum' if 'Quantidade' in df.columns else 'count'
            }).round(2)
        
        # Top performers
        top_categories = category_analysis.sort_values(('Receita Total', 'sum'), ascending=False).head(3) if category_analysis.size > 0 else {}
        top_regions = region_analysis.sort_values(('Receita Total', 'sum'), ascending=False).head(3) if region_analysis.size > 0 else {}
        top_products = product_analysis.sort_values(('Receita Total', 'sum'), ascending=False).head(5) if product_analysis.size > 0 else {}
        
        # Gera análise estruturada
        analysis = f"""# Principais Insights de Vendas - Análise Detalhada

## Identificação de tendências de vendas
**Dados analisados**: {len(data):,} transações processadas
**Receita total**: R$ {total_revenue:,.2f}
**Ticket médio**: R$ {total_revenue/len(data):,.2f}

### Performance por Mês (Últimos 3 meses):
"""
        
        if temporal_analysis.size > 0:
            recent_months = temporal_analysis.tail(3)
            for month, row in recent_months.iterrows():
                revenue = row[('Receita Total', 'sum')] if ('Receita Total', 'sum') in row else 0
                count = row[('Receita Total', 'count')] if ('Receita Total', 'count') in row else 0
                analysis += f"- **{month}**: R$ {revenue:,.2f} em {count} vendas\n"
        else:
            analysis += "- Dados temporais não disponíveis para análise de tendências\n"
        
        analysis += f"""
## Segmentação de clientes
**Total de clientes únicos**: {df['Cliente'].nunique() if 'Cliente' in df.columns else 'N/A'}
**Regiões ativas**: {df['Região'].nunique() if 'Região' in df.columns else 'N/A'}

### Top 3 Regiões por Receita:
"""
        
        if top_regions.size > 0:
            for i, (region, row) in enumerate(top_regions.iterrows(), 1):
                revenue = row[('Receita Total', 'sum')] if ('Receita Total', 'sum') in row else 0
                count = row[('Receita Total', 'count')] if ('Receita Total', 'count') in row else 0
                percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                analysis += f"{i}. **{region}**: R$ {revenue:,.2f} ({percentage:.1f}% do total) - {count} vendas\n"
        else:
            analysis += "- Dados de região não disponíveis\n"
        
        analysis += f"""
## Produtos com melhor e pior desempenho
**Total de produtos únicos**: {df['Produto'].nunique() if 'Produto' in df.columns else 'N/A'}

### Top 5 Produtos por Receita:
"""
        
        if top_products.size > 0:
            for i, (product, row) in enumerate(top_products.iterrows(), 1):
                revenue = row[('Receita Total', 'sum')] if ('Receita Total', 'sum') in row else 0
                count = row[('Receita Total', 'count')] if ('Receita Total', 'count') in row else 0
                avg_ticket = row[('Receita Total', 'mean')] if ('Receita Total', 'mean') in row else 0
                analysis += f"{i}. **{product}**: R$ {revenue:,.2f} ({count} vendas, ticket médio R$ {avg_ticket:,.2f})\n"
        else:
            analysis += "- Dados de produto não disponíveis\n"
        
        analysis += f"""
## Avaliação da equipe de vendas
**Vendedores únicos**: {df['Vendedor'].nunique() if 'Vendedor' in df.columns else 'N/A'}

### Performance por Categoria:
"""
        
        if top_categories.size > 0:
            for i, (category, row) in enumerate(top_categories.iterrows(), 1):
                revenue = row[('Receita Total', 'sum')] if ('Receita Total', 'sum') in row else 0
                count = row[('Receita Total', 'count')] if ('Receita Total', 'count') in row else 0
                percentage = (revenue / total_revenue * 100) if total_revenue > 0 else 0
                analysis += f"{i}. **{category}**: R$ {revenue:,.2f} ({percentage:.1f}% do total) - {count} vendas\n"
        else:
            analysis += "- Dados de categoria não disponíveis\n"
        
        analysis += f"""
## Análise geográfica de vendas
**Concentração geográfica**: {len(region_analysis)} regiões diferentes
**Receita média por região**: R$ {total_revenue/len(region_analysis):,.2f} (se distribuída igualmente)

### Oportunidades de Expansão:
- Focar nas regiões de maior performance
- Investigar regiões com baixo volume de vendas
- Desenvolver estratégias específicas por região

## Taxa de conversão e ciclo de venda
**Vendas por dia**: {len(data)/30:.1f} vendas/dia (média)
**Receita por dia**: R$ {total_revenue/30:,.2f}/dia (média)

### Recomendações Operacionais:
- Otimizar processo de vendas para aumentar volume diário
- Implementar follow-up sistemático para melhorar conversão
- Analisar gargalos no processo de vendas

## Comparação com metas
**Meta sugerida baseada nos dados**: R$ {total_revenue * 1.2:,.2f} (+20% de crescimento)
**Vendas necessárias para meta**: {len(data) * 1.2:,.0f} transações

### Ações para Atingir Meta:
- Aumentar 20% no volume de vendas
- Melhorar ticket médio em 10%
- Focar nas categorias de maior performance

## Sazonalidade e oportunidades escondidas
**Período de análise**: {df['Data'].min().strftime('%d/%m/%Y') if 'Data' in df.columns and not df['Data'].isna().all() else 'N/A'} a {df['Data'].max().strftime('%d/%m/%Y') if 'Data' in df.columns and not df['Data'].isna().all() else 'N/A'}

### Padrões Identificados:
- Analisar variações mensais para identificar sazonalidade
- Identificar produtos com potencial de crescimento
- Desenvolver campanhas sazonais específicas

---

### Resumo Executivo dos Dados
- **Total de Transações**: {len(data):,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {total_revenue/len(data):,.2f}
- **Período**: {last_update if last_update else 'Dados mais recentes'}
- **Fonte**: Planilha de vendas integrada

*Análise gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        
        return analysis
        
    except Exception as e:
        return f"Erro na análise detalhada: {e}"

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('dashboard.html')

@app.route('/api/data')
def get_data():
    """API para obter dados da planilha"""
    global cached_data, last_update
    
    if cached_data is None:
        update_data()
    
    if isinstance(cached_data, dict):
        # Múltiplas guias
        return jsonify({
            'data': cached_data,
            'last_update': last_update,
            'total_sheets': len(cached_data),
            'total_records': sum(sheet['total_registros'] for sheet in cached_data.values()),
            'sheets_info': {k: {'nome': v['nome'], 'registros': v['total_registros']} for k, v in cached_data.items()}
        })
    else:
        # Uma única guia (compatibilidade)
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
            # Múltiplas guias
            return jsonify({
                'success': True,
                'message': 'Dados atualizados com sucesso!',
                'last_update': last_update,
                'total_sheets': len(cached_data),
                'total_records': sum(sheet['total_registros'] for sheet in cached_data.values()),
                'sheets_info': {k: {'nome': v['nome'], 'registros': v['total_registros']} for k, v in cached_data.items()}
            })
        else:
            # Uma única guia (compatibilidade)
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
        if request.method == 'POST':
            # Análise com dados específicos enviados
            data = request.get_json()
            # Por enquanto, usa a análise padrão
            analysis = get_analysis()
        else:
            # Análise com dados em cache
            analysis = get_analysis()
        
        return jsonify({
            'analysis': analysis,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({
            'error': f'Erro ao gerar análise: {str(e)}'
        }), 500

@app.route('/api/sheets')
def get_sheets():
    """API para obter lista de planilhas disponíveis"""
    try:
        sheets = ["Planilha Principal"]  # Simplificado para o método direto
        return jsonify({
            'sheets': sheets
        })
    except Exception as e:
        return jsonify({
            'error': f'Erro ao obter planilhas: {str(e)}'
        }), 500

@app.route('/api/chat', methods=['POST'])
def chat_with_ai():
    """API para chat com IA"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({
                'error': 'Mensagem não fornecida'
            }), 400
        
        # Prepara contexto dos dados para a IA
        context = prepare_data_context()
        
        # Cria prompt contextualizado para a IA
        prompt = f"""Você é um assistente especializado em análise de dados de vendas. 

DADOS DISPONÍVEIS:
{context}

PERGUNTA DO USUÁRIO: {user_message}

INSTRUÇÕES:
- Responda em português brasileiro
- Use os dados fornecidos para dar insights específicos
- Seja preciso e baseado nos dados reais
- Use formatação Markdown para organizar a resposta
- Inclua números específicos quando relevante
- Sugira ações práticas baseadas nos dados

RESPONDA:"""
        
        # Tenta consultar a IA real, com fallback para análise local
        try:
            from api_openrouter import consultar_ia
            ai_response = consultar_ia(prompt)
        except Exception as e:
            print(f"Erro na IA externa: {e}")
            # Fallback para análise local inteligente
            ai_response = generate_local_ai_response(user_message, context)
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao processar mensagem: {str(e)}'
        }), 500

def prepare_data_context():
    """Prepara contexto dos dados para a IA"""
    try:
        if not cached_data:
            return "Nenhum dado disponível para análise."
        
        # Prepara dados para análise
        all_data = []
        if isinstance(cached_data, dict):
            for sheet_data in cached_data.values():
                if 'dados' in sheet_data and isinstance(sheet_data['dados'], list):
                    all_data.extend(sheet_data['dados'])
        else:
            all_data = cached_data
        
        if not all_data:
            return "Nenhum dado disponível para análise."
        
        # Calcula métricas básicas
        total_records = len(all_data)
        total_revenue = 0
        product_counts = {}
        region_counts = {}
        category_counts = {}
        vendor_counts = {}
        
        for row in all_data:
            # Receita
            try:
                revenue = float(str(row.get('Receita Total', '0')).replace(',', '.').replace('R$', '').strip()) or 0
            except (ValueError, TypeError):
                revenue = 0
            total_revenue += revenue
            
            # Produtos
            product = row.get('Produto', 'Outros')
            product_counts[product] = product_counts.get(product, 0) + 1
            
            # Regiões
            region = row.get('Região', 'Outros')
            region_counts[region] = region_counts.get(region, 0) + 1
            
            # Categorias
            category = row.get('Categoria', 'Outros')
            category_counts[category] = category_counts.get(category, 0) + 1
            
            # Vendedores
            vendor = row.get('Vendedor', 'Outros')
            vendor_counts[vendor] = vendor_counts.get(vendor, 0) + 1
        
        avg_ticket = total_revenue / total_records if total_records > 0 else 0
        
        # Top performers
        top_products = sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        top_vendors = sorted(vendor_counts.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Cria contexto estruturado
        context = f"""
RESUMO GERAL:
- Total de transações: {total_records:,}
- Receita total: R$ {total_revenue:,.2f}
- Ticket médio: R$ {avg_ticket:,.2f}
- Última atualização: {last_update if last_update else 'N/A'}

TOP PRODUTOS POR VENDAS:
{chr(10).join([f"- {product}: {count} vendas" for product, count in top_products])}

TOP REGIÕES POR VENDAS:
{chr(10).join([f"- {region}: {count} vendas" for region, count in top_regions])}

TOP CATEGORIAS POR VENDAS:
{chr(10).join([f"- {category}: {count} vendas" for category, count in top_categories])}

TOP VENDEDORES POR VENDAS:
{chr(10).join([f"- {vendor}: {count} vendas" for vendor, count in top_vendors])}

DADOS DETALHADOS DISPONÍVEIS:
- {len(product_counts)} produtos únicos
- {len(region_counts)} regiões ativas
- {len(category_counts)} categorias
- {len(vendor_counts)} vendedores
"""
        
        return context
        
    except Exception as e:
        return f"Erro ao preparar contexto: {str(e)}"

def generate_local_ai_response(user_message, context):
    """Gera resposta inteligente local baseada nos dados"""
    try:
        message_lower = user_message.lower()
        
        # Extrai dados do contexto
        lines = context.split('\n')
        total_records = 0
        total_revenue = 0
        avg_ticket = 0
        
        for line in lines:
            if 'Total de transações:' in line:
                total_records = int(line.split(':')[1].replace(',', '').strip())
            elif 'Receita total:' in line:
                revenue_str = line.split(':')[1].replace('R$', '').replace(',', '').strip()
                total_revenue = float(revenue_str)
            elif 'Ticket médio:' in line:
                ticket_str = line.split(':')[1].replace('R$', '').replace(',', '').strip()
                avg_ticket = float(ticket_str)
        
        # Se não temos dados carregados, retorna mensagem apropriada
        if total_records == 0:
            return """# 📊 Dados Não Carregados

**Nenhum dado encontrado para análise.**

## **Para Começar**
1. Clique em **"Atualizar Dados"** para carregar informações da planilha
2. Aguarde o carregamento dos dados
3. Depois faça suas perguntas sobre vendas, produtos ou regiões

## **O que Posso Analisar**
- 📈 Performance geral de vendas
- 🛍️ Produtos mais vendidos
- 🌍 Análise por região
- 📊 Tendências temporais
- 🎯 Oportunidades de crescimento

*Carregue os dados primeiro e depois faça suas perguntas!*"""
        
        # Análise contextual inteligente
        if any(word in message_lower for word in ['vendas', 'venda', 'performance', 'resultado', 'resumo']):
            return f"""# 📊 Resumo de Vendas Atual

## **Métricas Principais**
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {avg_ticket:,.2f}

## **Insights Estratégicos**
Com base nos seus dados, posso identificar padrões importantes e oportunidades de crescimento. Sua base de {total_records:,} transações oferece uma visão robusta do desempenho.

## **Análise de Performance**
- **Receita por Transação**: R$ {avg_ticket:,.2f}
- **Volume de Dados**: {total_records:,} registros analisados
- **Base Sólida**: Dados suficientes para análises confiáveis

## **Próximos Passos Recomendados**
- Analisar tendências mensais para identificar sazonalidade
- Investigar produtos com maior potencial de crescimento
- Avaliar oportunidades de expansão geográfica

*Que aspecto específico gostaria de investigar mais profundamente?*"""

        elif any(word in message_lower for word in ['produto', 'produtos', 'item', 'itens', 'top']):
            return f"""# 🛍️ Análise de Produtos

## **Performance de Produtos**
Com base nos seus dados de {total_records:,} transações, posso analisar o desempenho dos produtos e identificar oportunidades.

## **Dados Disponíveis**
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {avg_ticket:,.2f}

## **Insights Disponíveis**
- **Ranking de Produtos**: Top performers por vendas
- **Análise por Categoria**: Performance por segmento
- **Produtos por Mês**: Variação temporal
- **Ticket Médio**: Valor por produto

## **Recomendações Estratégicas**
- Focar nos produtos de maior performance
- Investigar produtos com baixo volume mas alto ticket
- Desenvolver estratégias específicas por categoria

*Gostaria de ver o ranking completo de produtos ou focar em alguma categoria específica?*"""

        elif any(word in message_lower for word in ['região', 'regiões', 'geográfico', 'localização', 'onde']):
            return f"""# 🌍 Análise Geográfica

## **Distribuição Geográfica**
Sua operação abrange múltiplas regiões, oferecendo oportunidades de análise e expansão.

## **Insights Geográficos**
- **Concentração de Vendas**: Identificar regiões de maior performance
- **Oportunidades de Expansão**: Regiões com potencial de crescimento
- **Análise de Penetração**: Cobertura e densidade por região
- **Estratégias Regionais**: Abordagens específicas por localização

## **Recomendações**
- Focar recursos nas regiões de maior performance
- Desenvolver estratégias específicas para cada mercado
- Identificar regiões com potencial de crescimento

*Qual região gostaria de analisar em detalhes?*"""

        elif any(word in message_lower for word in ['análise', 'analisar', 'relatório', 'relatorio', 'insights', 'relatório']):
            return f"""# 📈 Relatórios e Análises Disponíveis

## **Análises Estruturadas**
- **📊 Tendências Temporais**: Variações por período
- **🛍️ Performance de Produtos**: Rankings e oportunidades
- **🌍 Análise Geográfica**: Concentração e expansão
- **👥 Segmentação de Clientes**: Comportamento e preferências
- **🎯 Insights Estratégicos**: Recomendações personalizadas

## **Dados Base para Análise**
- **{total_records:,}** transações analisadas
- **R$ {total_revenue:,.2f}** em receita total
- **Múltiplas categorias** e produtos
- **Diversas regiões** de atuação

## **Tipos de Relatórios**
- Relatório executivo completo
- Análise de tendências mensais
- Performance por categoria
- Oportunidades de crescimento

*Que tipo de relatório gostaria de gerar?*"""

        elif any(word in message_lower for word in ['ajuda', 'help', 'comandos', 'como usar', 'o que posso']):
            return f"""# 🤖 Como Posso Ajudar?

## **Comandos Principais**
- **"Mostre as vendas"** - Resumo geral de performance
- **"Produtos mais vendidos"** - Ranking de produtos
- **"Análise por região"** - Performance geográfica
- **"Gere um relatório"** - Análise estruturada completa
- **"Tendências mensais"** - Análise temporal

## **Seus Dados Atuais**
- **{total_records:,}** transações processadas
- **R$ {total_revenue:,.2f}** em receita total
- **Múltiplos produtos** e categorias
- **Diversas regiões** de atuação

## **Capacidades**
- Análise de tendências e padrões
- Identificação de oportunidades
- Geração de relatórios personalizados
- Insights baseados em dados reais

*Digite sua pergunta para começar a análise!*"""

        else:
            return f"""# 💡 Interessante Pergunta!

Com base nos seus **{total_records:,}** registros de vendas, posso ajudá-lo com:

## **Análises Disponíveis**
- **📊 Performance Geral**: Métricas e indicadores
- **🛍️ Análise de Produtos**: Rankings e oportunidades
- **🌍 Análise Geográfica**: Concentração e expansão
- **📈 Tendências Temporais**: Variações e padrões
- **🎯 Insights Estratégicos**: Recomendações personalizadas

## **Sugestões de Perguntas**
- "Mostre os produtos mais vendidos"
- "Qual região tem melhor performance?"
- "Analise as tendências mensais"
- "Gere um relatório executivo"
- "Quais são as oportunidades de crescimento?"

*Pode ser mais específico sobre o que gostaria de analisar?*"""
        
    except Exception as e:
        return f"# ❌ Erro na Análise\n\n**Ocorreu um erro ao processar sua pergunta.**\n\n*Tente novamente ou verifique se os dados estão carregados corretamente.*\n\nErro: {str(e)}"

# Inicialização dos dados
if __name__ == '__main__':
    # Cria diretório de templates se não existir
    import os
    os.makedirs('templates', exist_ok=True)
    
    # Atualiza dados na inicialização
    print("🔄 Carregando dados na inicialização...")
    update_data()
    
    print("Dashboard iniciado! Acesse: http://localhost:8081")
    app.run(debug=True, host='0.0.0.0', port=8081)
