######################################################################################################################
def FormatoCartao():
    card_style = """
    <style>
        @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
        
        .card {
            border-radius: 10px;
            padding: 20px;
            margin: 10px;
            text-align: left;
            background-color: #f9f9f9;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
        }
        .icon {
            font-size: 30px;
            margin-bottom: 10px;
            color: #007bff;
        }
        .metric {
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
            color: #333;
            display: flex;
            align-items: center;
        }
        .value {
            font-size: 25px;
            font-weight: bold;
        }
    </style>
    """
    return card_style

def CriarCartao(titulo, valor, icone_material, tipo_sinal):
    if tipo_sinal == 'KG':
        valor_formatado = FormatoQuilograma(valor)
    elif tipo_sinal == 'U$':
        valor_formatado = FormatoDolar(valor)
    else:
        valor_formatado = f"{valor:.2f}".replace('.', ',')

    return f"""<div class="card">
        <div class="metric">
            <span class="material-icons icon">{icone_material}</span>
            {titulo}
        </div>
        <div class="value">{valor_formatado}</div>
    </div>"""

def FormatoQuilograma(valor):
    abs_valor = abs(valor)
    
    if abs_valor >= 1_000_000_000:
        valor_str = f"{valor / 1_000_000_000:.2f}".replace('.', ',') + " Bi"
    elif abs_valor >= 1_000_000:
        valor_str = f"{valor / 1_000_000:.2f}".replace('.', ',') + " Mi"
    elif abs_valor >= 1_000:
        valor_str = f"{valor / 1_000:.2f}".replace('.', ',') + " K"
    else:
        valor_str = f"{valor:.2f}".replace('.', ',')

    return f"{valor_str}"

def FormatoDolar(valor):
    abs_valor = abs(valor)

    if abs_valor >= 1_000_000_000:
        valor_str = f"{valor / 1_000_000_000:.2f}".replace('.', ',') + " Bi"
    elif abs_valor >= 1_000_000:
        valor_str = f"{valor / 1_000_000:.2f}".replace('.', ',') + " Mi"
    elif abs_valor >= 1_000:
        valor_str = f"{valor / 1_000:.2f}".replace('.', ',') + " K"
    else:
        valor_str = f"{valor:.2f}".replace('.', ',')

    return f"{valor_str}"