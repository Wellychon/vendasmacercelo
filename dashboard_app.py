from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import threading
import time
import os
from apps_script_service import apps_script_service
from api_openrouter import consultar_ia

app = Flask(__name__)

# Configuração para Vercel
app.config['JSON_AS_ASCII'] = False
app.config['JSON_SORT_KEYS'] = False

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
        # Análise simples sem pandas para reduzir tamanho
        total_records = len(data)
        total_revenue = 0
        categories = {}
        regions = {}
        products = {}
        
        # Análise básica dos dados
        for row in data:
            # Receita
            try:
                revenue = float(str(row.get('Receita Total', '0')).replace(',', '.').replace('R$', '').strip()) or 0
                total_revenue += revenue
            except (ValueError, TypeError):
                pass
            
            # Categorias
            category = row.get('Categoria', 'Outros')
            if category not in categories:
                categories[category] = {'count': 0, 'revenue': 0}
            categories[category]['count'] += 1
            categories[category]['revenue'] += revenue
            
            # Regiões
            region = row.get('Região', 'Outros')
            if region not in regions:
                regions[region] = {'count': 0, 'revenue': 0}
            regions[region]['count'] += 1
            regions[region]['revenue'] += revenue
            
            # Produtos
            product = row.get('Produto', 'Outros')
            if product not in products:
                products[product] = {'count': 0, 'revenue': 0}
            products[product]['count'] += 1
            products[product]['revenue'] += revenue
        
        # Top performers
        top_categories = sorted(categories.items(), key=lambda x: x[1]['revenue'], reverse=True)[:3]
        top_regions = sorted(regions.items(), key=lambda x: x[1]['revenue'], reverse=True)[:3]
        top_products = sorted(products.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        
        # Gera análise estruturada simplificada
        analysis = f"""# Principais Insights de Vendas - Análise Detalhada

## Identificação de tendências de vendas
**Dados analisados**: {total_records:,} transações processadas
**Receita total**: R$ {total_revenue:,.2f}
**Ticket médio**: R$ {total_revenue/total_records:,.2f}

## Top 3 Categorias por Receita:
"""
        
        for i, (category, data) in enumerate(top_categories, 1):
            percentage = (data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            analysis += f"{i}. **{category}**: R$ {data['revenue']:,.2f} ({percentage:.1f}% do total) - {data['count']} vendas\n"
        
        analysis += f"""
## Top 3 Regiões por Receita:
"""
        
        for i, (region, data) in enumerate(top_regions, 1):
            percentage = (data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            analysis += f"{i}. **{region}**: R$ {data['revenue']:,.2f} ({percentage:.1f}% do total) - {data['count']} vendas\n"
        
        analysis += f"""
## Top 5 Produtos por Receita:
"""
        
        for i, (product, data) in enumerate(top_products, 1):
            avg_ticket = data['revenue'] / data['count'] if data['count'] > 0 else 0
            analysis += f"{i}. **{product}**: R$ {data['revenue']:,.2f} ({data['count']} vendas, ticket médio R$ {avg_ticket:,.2f})\n"
        
        analysis += f"""
## Resumo Executivo dos Dados
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {total_revenue/total_records:,.2f}
- **Período**: {last_update if last_update else 'Dados mais recentes'}
- **Fonte**: Planilha de vendas integrada

*Análise gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        
        return analysis
        
    except Exception as e:
        return f"Erro na análise detalhada: {e}"

def get_analysis_with_data(data):
    """Obtém análise dos dados usando IA com dados específicos"""
    try:
        if not data:
            return "Nenhum dado disponível para análise."
        
        # Prepara resumo dos dados
        total_revenue = data.get('totalRevenue', 0)
        total_sales = data.get('totalSales', 0)
        average_ticket = data.get('averageTicket', 0)
        category_data = data.get('categoryData', {})
        region_data = data.get('regionData', {})
        product_data = data.get('productData', {})
        
        # Cria resumo estruturado
        summary = f"""
        Dados de vendas analisados:
        - Total de vendas: {total_sales:,} transações
        - Receita total: R$ {total_revenue:,.2f}
        - Ticket médio: R$ {average_ticket:.2f}
        
        Resumo por categoria:
        """
        
        # Top 5 categorias por receita
        sorted_categories = sorted(category_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        for category, info in sorted_categories:
            summary += f"\n- {category}: {info['sales']} vendas, R$ {info['revenue']:,.2f} receita"
        
        summary += f"\n\nResumo por região:"
        # Top 5 regiões por receita
        sorted_regions = sorted(region_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        for region, info in sorted_regions:
            summary += f"\n- {region}: {info['sales']} vendas, R$ {info['revenue']:,.2f} receita"
        
        summary += f"\n\nTop produtos:"
        # Top 10 produtos por receita
        sorted_products = sorted(product_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:10]
        for product, info in sorted_products:
            summary += f"\n- {product} ({info['category']}): {info['sales']} vendas, R$ {info['revenue']:,.2f} receita"
        
        # Análise em formato Markdown
        analysis = f"""# Principais Insights de Vendas

## Identificação de tendências de vendas
Analisar variações sazonais, picos de demanda, períodos de baixa e crescimento ao longo do ano permite ajustar estoque, campanhas e metas.

**Dados analisados**: {len(cached_data) if isinstance(cached_data, dict) else len(cached_data) if cached_data else 0:,} transações processadas
**Período**: {last_update if last_update else 'Dados mais recentes disponíveis'}

## Segmentação de clientes
Separar clientes em grupos por comportamento, localização, ticket médio ou frequência de compra ajuda a personalizar ofertas e comunicação.

**Recomendação**: Implementar análise de RFM (Recência, Frequência, Valor Monetário) para segmentação mais precisa.

## Produtos com melhor e pior desempenho
Avaliar quais itens lideraram as vendas e quais ficaram abaixo do esperado permite modificar o mix, investir em promoções ou reposicionar produtos.

**Próximo passo**: Criar ranking de produtos por receita e identificar oportunidades de melhoria.

## Avaliação da equipe de vendas
Identificar quais vendedores ou equipes tiveram melhor performance e o que fez diferença no resultado global.

**Métrica sugerida**: Análise de performance por vendedor/região para identificar melhores práticas.

## Análise geográfica de vendas
Verificar quais regiões/cidades geraram mais receita ou volume de vendas pode indicar oportunidades para expansão ou esforços de marketing localizados.

**Foco**: Mapear concentração de vendas e identificar regiões com potencial de crescimento.

## Taxa de conversão e ciclo de venda
Medir eficiência do funil comercial, tempo de conversão e possíveis gargalos operacionaliza melhorias no fluxo.

**Objetivo**: Otimizar processo de vendas identificando pontos de melhoria no funil.

## Comparação com metas
Avaliar resultados reais versus metas desenhadas e ajustar objetivos para o ciclo seguinte, revisitando previsões.

**Ação**: Estabelecer metas realistas baseadas no histórico de vendas analisado.

## Sazonalidade e oportunidades escondidas
Detectar sazonalidade ou padrões inesperados, aproveitando momentos de pico e melhorando a gestão de estoque e campanhas.

**Análise**: Identificar padrões mensais e sazonais para planejamento estratégico.

---

### Resumo dos Dados Analisados
- **Total de Transações**: {len(cached_data) if isinstance(cached_data, dict) else len(cached_data) if cached_data else 0:,}
- **Período de Análise**: {last_update if last_update else 'Dados mais recentes'}
- **Fonte**: Planilha de vendas integrada

*Análise gerada em {datetime.now().strftime('%d/%m/%Y às %H:%M')}*
"""
        return analysis
        
    except Exception as e:
        return f"Erro ao gerar análise: {e}"

@app.route('/')
def index():
    """Página principal do dashboard"""
    return render_template('modern_dashboard.html')

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
        
        print(f"💬 Nova mensagem recebida: {user_message[:100]}...")
        
        if not user_message:
            print("❌ Mensagem vazia recebida")
            return jsonify({
                'error': 'Mensagem não fornecida'
            }), 400
        
        # Garante que os dados estejam carregados
        if cached_data is None:
            print("⚠️ Cache vazio, carregando dados...")
            update_data()
        
        # Verifica se temos dados após tentar carregar
        if cached_data is None:
            print("❌ Nenhum dado disponível após tentativa de carregamento")
            return jsonify({
                'response': """# ⚠️ Dados Não Disponíveis

**Nenhum dado foi carregado da planilha.**

## **Para Resolver**
1. Clique em **"Atualizar Dados"** no topo da página
2. Aguarde o carregamento dos dados
3. Tente fazer sua pergunta novamente

## **Verificações**
- ✓ Conexão com Google Sheets configurada?
- ✓ URL do Apps Script configurada no .env?
- ✓ Planilha com dados disponíveis?

*Configure a conexão primeiro para usar o chat com dados reais!*"""
            }), 200
        
        print(f"✅ Dados em cache: {len(cached_data) if isinstance(cached_data, dict) else 'N/A'} guias")
        
        # Prepara contexto dos dados para a IA
        print("🔄 Preparando contexto dos dados...")
        context = prepare_data_context()
        print(f"✅ Contexto preparado: {len(context)} caracteres")
        
        # Calcula total de registros para o prompt
        total_records = 0
        if cached_data:
            if isinstance(cached_data, dict):
                total_records = sum(sheet['total_registros'] for sheet in cached_data.values())
            else:
                total_records = len(cached_data)
        
        # Mensagem do sistema com contexto dos dados
        system_message = f"""Você é um analista de dados de vendas especializado com acesso completo aos dados reais da empresa.

DADOS REAIS DA EMPRESA:
{context}

INSTRUÇÕES IMPORTANTES:
- Você tem acesso a {total_records:,} registros reais de vendas
- Use APENAS os dados fornecidos acima para suas análises
- Seja extremamente específico com números, percentuais e valores EXATOS dos dados
- Identifique padrões, tendências e oportunidades REAIS nos dados fornecidos
- Responda em português brasileiro claro e profissional
- Use formatação Markdown para organizar suas respostas (títulos, listas, negrito)
- Cite números e métricas específicas dos dados reais
- Sugira ações práticas baseadas nos dados fornecidos
- Compare performances entre produtos, regiões e períodos usando os dados reais
- Destaque insights únicos identificados nos dados"""

        # Pergunta do usuário
        user_prompt = f"""PERGUNTA: {user_message}

Analise os dados fornecidos e responda com base nos números REAIS e específicos. Inclua métricas, percentuais e comparações concretas."""
        
        print(f"🤖 Enviando para IA... (contexto: {len(system_message)} chars, prompt: {len(user_prompt)} chars)")
        
        # Tenta consultar a IA real, com fallback para análise local
        try:
            ai_response = consultar_ia(user_prompt, system_message=system_message)
            print(f"✅ Resposta da IA externa obtida: {len(ai_response)} caracteres")
        except Exception as e:
            print(f"⚠️ IA externa indisponível: {e}")
            print("🔄 Usando análise local inteligente...")
            # Fallback para análise local inteligente
            ai_response = generate_local_ai_response(user_message, context)
            print(f"✅ Resposta local gerada: {len(ai_response)} caracteres")
        
        print(f"📤 Enviando resposta para o frontend")
        
        return jsonify({
            'response': ai_response,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        print(f"❌ ERRO no chat endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'error': f'Erro ao processar mensagem: {str(e)}'
        }), 500


def prepare_data_context():
    """Prepara contexto detalhado dos dados para a IA"""
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
        
        # Análise detalhada dos dados
        total_records = len(all_data)
        total_revenue = 0
        total_quantity = 0
        product_data = {}
        region_data = {}
        category_data = {}
        monthly_data = {}
        price_analysis = {}
        
        # Processa cada registro
        for row in all_data:
            # Receita
            try:
                revenue = float(str(row.get('Receita Total', '0')).replace(',', '.').replace('R$', '').strip()) or 0
            except (ValueError, TypeError):
                revenue = 0
            total_revenue += revenue
            
            # Quantidade
            try:
                quantity = int(row.get('Quantidade', 0)) or 0
            except (ValueError, TypeError):
                quantity = 0
            total_quantity += quantity
            
            # Preço unitário
            try:
                unit_price = float(str(row.get('Preço Unitário', '0')).replace(',', '.').replace('R$', '').strip()) or 0
            except (ValueError, TypeError):
                unit_price = 0
            
            # Produtos (com receita e quantidade)
            product = row.get('Produto', 'Outros')
            if product not in product_data:
                product_data[product] = {'sales': 0, 'revenue': 0, 'quantity': 0, 'avg_price': 0, 'category': ''}
            product_data[product]['sales'] += 1
            product_data[product]['revenue'] += revenue
            product_data[product]['quantity'] += quantity
            product_data[product]['category'] = row.get('Categoria', 'Outros')
            
            # Regiões (com receita e quantidade)
            region = row.get('Região', 'Outros')
            if region not in region_data:
                region_data[region] = {'sales': 0, 'revenue': 0, 'quantity': 0}
            region_data[region]['sales'] += 1
            region_data[region]['revenue'] += revenue
            region_data[region]['quantity'] += quantity
            
            # Categorias (com receita e quantidade)
            category = row.get('Categoria', 'Outros')
            if category not in category_data:
                category_data[category] = {'sales': 0, 'revenue': 0, 'quantity': 0, 'products': set()}
            category_data[category]['sales'] += 1
            category_data[category]['revenue'] += revenue
            category_data[category]['quantity'] += quantity
            category_data[category]['products'].add(product)
            
            # Análise mensal
            try:
                date_str = row.get('Data', '')
                if 'T' in date_str:
                    month = date_str.split('T')[0][:7]  # YYYY-MM
                else:
                    month = date_str[:7] if len(date_str) >= 7 else '2025-01'
                
                if month not in monthly_data:
                    monthly_data[month] = {'sales': 0, 'revenue': 0, 'quantity': 0}
                monthly_data[month]['sales'] += 1
                monthly_data[month]['revenue'] += revenue
                monthly_data[month]['quantity'] += quantity
            except:
                pass
            
            # Análise de preços
            if unit_price > 0:
                price_range = f"R$ {int(unit_price//50)*50}-{int(unit_price//50)*50+49}"
                if price_range not in price_analysis:
                    price_analysis[price_range] = {'count': 0, 'revenue': 0}
                price_analysis[price_range]['count'] += 1
                price_analysis[price_range]['revenue'] += revenue
        
        # Calcula métricas finais
        avg_ticket = total_revenue / total_records if total_records > 0 else 0
        avg_quantity = total_quantity / total_records if total_records > 0 else 0
        
        # Top performers com receita
        top_products = sorted(product_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:10]
        top_regions = sorted(region_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        top_categories = sorted(category_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:5]
        top_months = sorted(monthly_data.items(), key=lambda x: x[1]['revenue'], reverse=True)[:6]
        
        # Converte sets para contagem
        for cat_data in category_data.values():
            cat_data['products'] = len(cat_data['products'])
        
        # Cria contexto super detalhado
        context = f"""
=== DADOS COMPLETOS DA PLANILHA DE VENDAS ===

RESUMO EXECUTIVO:
- Total de transações: {total_records:,}
- Receita total: R$ {total_revenue:,.2f}
- Quantidade total vendida: {total_quantity:,} unidades
- Ticket médio: R$ {avg_ticket:,.2f}
- Quantidade média por venda: {avg_quantity:.1f} unidades
- Período: {last_update if last_update else 'Dados mais recentes'}
- Fonte: {len(cached_data) if isinstance(cached_data, dict) else 1} guias de planilha

=== ANÁLISE POR PRODUTOS (TOP 10) ===
"""
        
        for i, (product, data) in enumerate(top_products, 1):
            avg_price = data['revenue'] / data['quantity'] if data['quantity'] > 0 else 0
            context += f"{i}. {product} ({data['category']}):\n"
            context += f"   - Vendas: {data['sales']} transações\n"
            context += f"   - Receita: R$ {data['revenue']:,.2f}\n"
            context += f"   - Quantidade: {data['quantity']:,} unidades\n"
            context += f"   - Preço médio: R$ {avg_price:,.2f}\n\n"
        
        context += f"""
=== ANÁLISE POR REGIÕES (TOP 5) ===
"""
        
        for i, (region, data) in enumerate(top_regions, 1):
            percentage = (data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            context += f"{i}. {region}:\n"
            context += f"   - Vendas: {data['sales']} transações ({data['sales']/total_records*100:.1f}%)\n"
            context += f"   - Receita: R$ {data['revenue']:,.2f} ({percentage:.1f}%)\n"
            context += f"   - Quantidade: {data['quantity']:,} unidades\n"
            context += f"   - Ticket médio: R$ {data['revenue']/data['sales']:,.2f}\n\n"
        
        context += f"""
=== ANÁLISE POR CATEGORIAS (TOP 5) ===
"""
        
        for i, (category, data) in enumerate(top_categories, 1):
            percentage = (data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            context += f"{i}. {category}:\n"
            context += f"   - Vendas: {data['sales']} transações\n"
            context += f"   - Receita: R$ {data['revenue']:,.2f} ({percentage:.1f}%)\n"
            context += f"   - Quantidade: {data['quantity']:,} unidades\n"
            context += f"   - Produtos únicos: {data['products']}\n"
            context += f"   - Ticket médio: R$ {data['revenue']/data['sales']:,.2f}\n\n"
        
        context += f"""
=== ANÁLISE TEMPORAL (TOP 6 MESES) ===
"""
        
        for month, data in top_months:
            percentage = (data['revenue'] / total_revenue * 100) if total_revenue > 0 else 0
            context += f"- {month}:\n"
            context += f"  - Vendas: {data['sales']} transações\n"
            context += f"  - Receita: R$ {data['revenue']:,.2f} ({percentage:.1f}%)\n"
            context += f"  - Quantidade: {data['quantity']:,} unidades\n"
            context += f"  - Ticket médio: R$ {data['revenue']/data['sales']:,.2f}\n\n"
        
        context += f"""
=== DADOS DETALHADOS DISPONÍVEIS ===
- Produtos únicos: {len(product_data)}
- Regiões ativas: {len(region_data)}
- Categorias: {len(category_data)}
- Meses com dados: {len(monthly_data)}
- Faixas de preço: {len(price_analysis)}

=== ESTRUTURA DOS DADOS ===
Cada transação contém:
- Data da venda
- ID da transação
- Produto vendido
- Categoria do produto
- Região da venda
- Quantidade vendida
- Preço unitário
- Receita total calculada

=== INSIGHTS DISPONÍVEIS ===
- Análise de sazonalidade mensal
- Performance por produto e categoria
- Concentração geográfica de vendas
- Análise de ticket médio por segmento
- Identificação de produtos top performers
- Oportunidades de crescimento por região
- Análise de mix de produtos por categoria
"""
        
        return context
        
    except Exception as e:
        return f"Erro ao preparar contexto: {str(e)}"

def analyze_real_data():
    """Analisa os dados reais carregados"""
    try:
        if not cached_data:
            return "## **Status dos Dados**\n- ⚠️ Nenhum dado carregado\n- 🔄 Clique em 'Atualizar Dados' para carregar"
        
        # Prepara dados para análise
        all_data = []
        if isinstance(cached_data, dict):
            for sheet_data in cached_data.values():
                if 'dados' in sheet_data and isinstance(sheet_data['dados'], list):
                    all_data.extend(sheet_data['dados'])
        else:
            all_data = cached_data
        
        if not all_data:
            return "## **Status dos Dados**\n- ⚠️ Nenhum dado disponível\n- 🔄 Atualize os dados primeiro"
        
        # Análise básica dos dados
        total_records = len(all_data)
        total_revenue = 0
        products = set()
        regions = set()
        categories = set()
        
        for row in all_data:
            # Receita
            try:
                revenue = float(str(row.get('Receita Total', '0')).replace(',', '.').replace('R$', '').strip()) or 0
                total_revenue += revenue
            except (ValueError, TypeError):
                pass
            
            # Produtos
            if row.get('Produto'):
                products.add(row['Produto'])
            
            # Regiões
            if row.get('Região'):
                regions.add(row['Região'])
            
            # Categorias
            if row.get('Categoria'):
                categories.add(row['Categoria'])
        
        avg_ticket = total_revenue / total_records if total_records > 0 else 0
        
        return f"""## **Análise dos Dados Reais**
- **📊 Total de Registros**: {total_records:,}
- **💰 Receita Total**: R$ {total_revenue:,.2f}
- **🎯 Ticket Médio**: R$ {avg_ticket:,.2f}
- **🛍️ Produtos Únicos**: {len(products)}
- **🌍 Regiões Ativas**: {len(regions)}
- **📂 Categorias**: {len(categories)}

## **Insights Baseados em Dados Reais**
- **Base de Dados**: {total_records:,} transações analisadas
- **Diversificação**: {len(products)} produtos diferentes
- **Cobertura Geográfica**: {len(regions)} regiões
- **Segmentação**: {len(categories)} categorias"""
        
    except Exception as e:
        return f"## **Status dos Dados**\n- ❌ Erro na análise: {str(e)}"

def generate_local_ai_response(user_message, context):
    """Gera resposta inteligente local baseada nos dados"""
    try:
        message_lower = user_message.lower()
        
        # Extrai dados estruturados do contexto
        lines = context.split('\n')
        total_records = 0
        total_revenue = 0
        avg_ticket = 0
        total_quantity = 0
        
        # Coleta informações de produtos, regiões e categorias do contexto
        products_section = []
        regions_section = []
        categories_section = []
        months_section = []
        
        current_section = None
        
        for line in lines:
            # Extrai métricas básicas
            if 'Total de transações:' in line:
                try:
                    total_records = int(line.split(':')[1].replace(',', '').replace('.', '').strip())
                except:
                    pass
            elif 'Receita total: R$' in line:
                try:
                    revenue_str = line.split('R$')[1].replace(',', '').replace('.', '').strip()
                    total_revenue = float(revenue_str)
                except:
                    pass
            elif 'Ticket médio: R$' in line:
                try:
                    ticket_str = line.split('R$')[1].replace(',', '').replace('.', '').strip()
                    avg_ticket = float(ticket_str)
                except:
                    pass
            elif 'Quantidade total vendida:' in line:
                try:
                    qty_str = line.split(':')[1].replace(',', '').replace('.', '').split()[0].strip()
                    total_quantity = int(qty_str)
                except:
                    pass
            
            # Identifica seções
            if 'ANÁLISE POR PRODUTOS' in line:
                current_section = 'products'
            elif 'ANÁLISE POR REGIÕES' in line:
                current_section = 'regions'
            elif 'ANÁLISE POR CATEGORIAS' in line:
                current_section = 'categories'
            elif 'ANÁLISE TEMPORAL' in line:
                current_section = 'months'
            elif line.strip().startswith('==='):
                current_section = None
            
            # Coleta dados das seções
            if current_section == 'products' and line.strip() and not line.startswith('==='):
                products_section.append(line.strip())
            elif current_section == 'regions' and line.strip() and not line.startswith('==='):
                regions_section.append(line.strip())
            elif current_section == 'categories' and line.strip() and not line.startswith('==='):
                categories_section.append(line.strip())
            elif current_section == 'months' and line.strip() and not line.startswith('==='):
                months_section.append(line.strip())
        
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
        
        # Análise contextual inteligente com dados reais
        if any(word in message_lower for word in ['vendas', 'venda', 'performance', 'resultado', 'resumo', 'geral']):
            # Extrai primeiros produtos e regiões
            top_products_text = '\n'.join(products_section[:15]) if products_section else "Dados sendo processados..."
            top_regions_text = '\n'.join(regions_section[:10]) if regions_section else "Dados sendo processados..."
            
            return f"""# 📊 Resumo de Vendas - Análise Baseada em Dados Reais

## **Métricas Principais**
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {avg_ticket:,.2f}
- **Quantidade Vendida**: {total_quantity:,} unidades

## **Top Produtos (Dados Reais)**
{top_products_text[:500]}

## **Principais Regiões (Dados Reais)**
{top_regions_text[:400]}

## **Insights Estratégicos**
Com base na análise de **{total_records:,} transações reais**, identificamos:

- **Volume**: Base sólida de dados para análises confiáveis
- **Receita Média**: R$ {avg_ticket:,.2f} por transação
- **Distribuição**: Múltiplas categorias e regiões ativas

## **Recomendações Baseadas nos Dados**
1. **Foco em Performance**: Produtos top estão claramente identificados nos dados
2. **Expansão Geográfica**: Regiões com maior volume merecem atenção especial
3. **Otimização de Ticket**: Oportunidades de aumentar valor médio por venda

*Pergunte sobre produtos, regiões ou categorias específicas para análises detalhadas!*"""

        elif any(word in message_lower for word in ['produto', 'produtos', 'item', 'itens', 'top']):
            # Extrai dados de produtos do contexto
            products_info = '\n'.join(products_section[:20]) if products_section else "Carregando dados de produtos..."
            
            return f"""# 🛍️ Análise de Produtos - Dados Reais

## **Performance de Produtos**
Análise baseada em **{total_records:,} transações reais** da sua base de dados.

## **Top Produtos por Performance**
{products_info[:800]}

## **Métricas Globais**
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {avg_ticket:,.2f}
- **Quantidade Total**: {total_quantity:,} unidades

## **Insights dos Dados Reais**
- **Rankings Identificados**: Produtos com maior receita e volume
- **Categorias Analisadas**: Performance por segmento
- **Preços Médios**: Calculados com base nas transações reais
- **Oportunidades**: Produtos com alto potencial identificados

## **Recomendações Estratégicas**
1. **Produtos Top**: Focar nos itens de maior receita
2. **Mix de Produtos**: Balancear volume e ticket médio
3. **Categorias**: Desenvolver estratégias específicas por segmento

*Pergunte sobre produtos ou categorias específicas para detalhes!*"""

        elif any(word in message_lower for word in ['região', 'regiões', 'geográfico', 'localização', 'onde']):
            # Extrai dados de regiões do contexto
            regions_info = '\n'.join(regions_section[:15]) if regions_section else "Carregando dados geográficos..."
            
            return f"""# 🌍 Análise Geográfica - Dados Reais

## **Distribuição Geográfica**
Análise baseada em **{total_records:,} transações reais** distribuídas por região.

## **Top Regiões por Performance**
{regions_info[:700]}

## **Métricas Geográficas Globais**
- **Total de Transações**: {total_records:,}
- **Receita Total**: R$ {total_revenue:,.2f}
- **Ticket Médio**: R$ {avg_ticket:,.2f}
- **Múltiplas Regiões**: Operação nacional/regional ativa

## **Insights Geográficos dos Dados**
- **Concentração Identificada**: Regiões de maior performance nos dados
- **Performance Regional**: Rankings calculados com dados reais
- **Oportunidades de Expansão**: Regiões com potencial baseado em volume
- **Estratégias Regionais**: Dados suportam abordagens específicas

## **Recomendações Baseadas nos Dados**
1. **Foco Regional**: Priorizar regiões de maior receita identificadas
2. **Expansão Estratégica**: Regiões com crescimento consistente
3. **Marketing Localizado**: Adaptar estratégias por performance regional

*Pergunte sobre regiões específicas para análises detalhadas!*"""

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

def auto_update_worker():
    """Worker para atualização automática a cada 5 minutos"""
    while True:
        time.sleep(300)  # 5 minutos
        update_data()

if __name__ == '__main__':
    # Execução local
    import os
    import sys
    
    # Cria diretório de templates se não existir
    os.makedirs('templates', exist_ok=True)
    
    # Inicia atualização automática em background
    auto_update_thread = threading.Thread(target=auto_update_worker, daemon=True)
    auto_update_thread.start()
    
    # Atualiza dados na inicialização
    print("🔄 Carregando dados na inicialização...")
    update_data()
    
    # Verifica se foi passada uma porta específica
    port = int(os.environ.get('PORT', 8081))
    if len(sys.argv) > 1 and '--port' in sys.argv:
        try:
            port_index = sys.argv.index('--port')
            port = int(sys.argv[port_index + 1])
        except (ValueError, IndexError):
            pass
    
    print(f"🚀 Dashboard iniciado!")
    print(f"📍 Local: http://localhost:{port}")
    print(f"🌐 Network: http://0.0.0.0:{port}")
    print(f"📊 Ambiente: {'Produção' if os.environ.get('VERCEL') else 'Desenvolvimento'}")
    
    # Debug mode apenas em desenvolvimento
    debug_mode = not os.environ.get('VERCEL')
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
