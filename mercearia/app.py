from flask import Flask, render_template, request, redirect, url_for, Response
import io
import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

app = Flask(__name__)

# Simulação de banco de dados em memória
vendas = []
fiados = []
pagamentos_fiado = []  # valores pagos de fiado

@app.route("/sobre")
def sobre():
    return "Esta é a página Sobre."

@app.route('/')
def index():
    return render_template('index.html')

# Registrar venda
@app.route('/vendas', methods=['GET', 'POST'])
def registrar_venda():
    if request.method == 'POST':
        produto = request.form['produto']
        valor = float(request.form['valor'])
        vendas.append({'produto': produto, 'valor': valor})
        return redirect(url_for('registrar_venda'))
    return render_template('vendas.html', vendas=vendas)

# Registrar fiado
@app.route('/fiado', methods=['GET', 'POST'])
def registrar_fiado():
    if request.method == 'POST':
        cliente = request.form['cliente']
        valor = float(request.form['valor'])
        fiados.append({'cliente': cliente, 'valor': valor})
        return redirect(url_for('registrar_fiado'))
    return render_template('fiado.html', fiados=fiados)

@app.route('/pagar_fiado/<int:index>')
def pagar_fiado(index):
    if 0 <= index < len(fiados):
        valor_pago = fiados[index]['valor']
        pagamentos_fiado.append(valor_pago)
        fiados.pop(index)
    return redirect(url_for('registrar_fiado'))

# Resumo do dia
@app.route('/resumo')
def resumo():
    total_vendas = sum(v['valor'] for v in vendas)
    total_fiado = sum(f['valor'] for f in fiados)
    total_pago_fiado = sum(pagamentos_fiado)

    return render_template(
        'resumo.html',
        total_vendas=total_vendas,
        total_fiado=total_fiado,
        total_pago_fiado=total_pago_fiado,
        fiados=fiados,
        pagamentos_fiado=pagamentos_fiado
    )

# Download do histórico em PDF
@app.route('/download_pdf')
def download_pdf():
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    largura, altura = A4

    # Cabeçalho
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, altura - 50, "Relatório do Dia")

    # Data
    data_hoje = datetime.date.today().strftime("%d/%m/%Y")
    p.setFont("Helvetica", 12)
    p.drawString(100, altura - 80, f"Data: {data_hoje}")

    # Vendas
    y = altura - 120
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Vendas:")
    y -= 20
    p.setFont("Helvetica", 12)
    for venda in vendas:
        linha = f"{venda['produto']} - R$ {venda['valor']:.2f}"
        p.drawString(100, y, linha)
        y -= 20
    p.drawString(100, y - 10, f"Total de Vendas: R$ {sum(v['valor'] for v in vendas):.2f}")
    y -= 40

    # Fiados
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Fiados em aberto:")
    y -= 20
    p.setFont("Helvetica", 12)
    for fiado in fiados:
        linha = f"{fiado['cliente']} - R$ {fiado['valor']:.2f}"
        p.drawString(100, y, linha)
        y -= 20
    p.drawString(100, y - 10, f"Total Fiado: R$ {sum(f['valor'] for f in fiados):.2f}")
    y -= 40

    # Pagamentos de fiado
    p.setFont("Helvetica-Bold", 14)
    p.drawString(100, y, "Pagamentos de Fiado:")
    y -= 20
    p.setFont("Helvetica", 12)
    for pago in pagamentos_fiado:
        linha = f"Pagamento: R$ {pago:.2f}"
        p.drawString(100, y, linha)
        y -= 20
    p.drawString(100, y - 10, f"Total Pago Fiado: R$ {sum(pagamentos_fiado):.2f}")

    # Finaliza PDF
    p.showPage()
    p.save()
    buffer.seek(0)

    return Response(buffer, mimetype='application/pdf',
                    headers={"Content-Disposition": "attachment;filename=relatorio_dia.pdf"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)