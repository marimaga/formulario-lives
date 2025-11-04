from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2 import service_account
import os

app = Flask(__name__)

# Caminho para o arquivo JSON da conta de serviço
cred_path = r"C:\Users\maris\OneDrive\Documentos\Formulario vscode\formulario-duvidas-membros-14599bd38a4f.json"

# Escopos corretos para Google Sheets e Drive
scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

import os
import json
from google.oauth2.service_account import Credentials
import gspread

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Criação das credenciais e cliente gspread
if os.environ.get("SERVICE_ACCOUNT_JSON"):
    # Para Render: pega o JSON da variável de ambiente
    service_account_info = json.loads(os.environ["SERVICE_ACCOUNT_JSON"])
    creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
else:
    # Para execução local: usa o arquivo JSON
    cred_path = r"C:\Users\maris\OneDrive\Documentos\Formulario vscode\formulario-duvidas-membros-14599bd38a4f.json"
    creds = Credentials.from_service_account_file(cred_path, scopes=SCOPES)

gc = gspread.authorize(creds)

# Abrir a planilha
sh = gc.open("Formulário Dúvidas Membros")
worksheet = sh.sheet1  # primeira aba da planilha

@app.route('/')
def index():
    sucesso = request.args.get('sucesso')
    return render_template('form.html', sucesso=sucesso)

@app.route('/enviar', methods=['POST'])
def enviar():
    username = request.form.get('username')
    duvida = request.form.get('duvida')
    
    if username and duvida:
        # Adiciona a linha na planilha
        worksheet.append_row([username, duvida])
        return redirect(url_for('index', sucesso=1))
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    # Caminho relativo para pasta static
    app.static_folder = 'static'
    app.run(debug=True)
