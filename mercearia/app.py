from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulação de banco de dados em memória
vendas = []
fiados = []

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

# Resumo do dia
@app.route('/resumo')
def resumo():
    total_vendas = sum(v['valor'] for v in vendas)
    total_fiado = sum(f['valor'] for f in fiados)
    return render_template('resumo.html', total_vendas=total_vendas, total_fiado=total_fiado)

if __name__ == '__main__':
    app.run(debug=True)