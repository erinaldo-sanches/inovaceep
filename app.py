from flask import Flask, render_template, request, redirect, url_for
import csv
from collections import Counter, defaultdict

app = Flask(__name__)

CSV_FILE = 'dados.csv'

# Perguntas fixas do questionário
PERGUNTAS = [
    "Organização do evento",
    "Qualidade dos projetos",
    "Atendimento dos alunos",
    "Estrutura física"
]

@app.route('/')
def index():
    return render_template('index.html', perguntas=PERGUNTAS)

@app.route('/salvar', methods=['POST'])
def salvar():
    respostas = [request.form.get(p) for p in PERGUNTAS]
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(respostas)
    return redirect(url_for('resultado'))

@app.route('/resultado')
def resultado():
    try:
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            dados = list(csv.reader(f))
    except FileNotFoundError:
        dados = []

    estatisticas = []
    for i, pergunta in enumerate(PERGUNTAS):
        respostas = [linha[i] for linha in dados if len(linha) > i]
        total = len(respostas)
        contagem = Counter(respostas)
        percentuais = {
            op: round((contagem[op] / total) * 100, 1) if total > 0 else 0
            for op in ['Excelente', 'Regular', 'Fraca']
        }
        estatisticas.append({
            'pergunta': pergunta,
            'total': total,
            'contagem': contagem,
            'percentuais': percentuais
        })

    return render_template('resultado.html', estatisticas=estatisticas)

if __name__ == '__main__':
    app.run(debug=True)