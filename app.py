from flask import Flask, render_template, request, redirect, url_for
import os
import json
import gspread
from google.oauth2.service_account import Credentials

app = Flask(__name__)

# Escopos para Google Sheets
SCOPES = [
  "https://www.googleapis.com/auth/spreadsheets",
  "https://www.googleapis.com/auth/drive"
]

# Pega credenciais do Render
service_account_info = json.loads(os.environ["GOOGLE_CREDENTIALS"])
creds = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)

# Cliente gspread
gc = gspread.authorize(creds)

# Abre a planilha
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
        worksheet.append_row([username, duvida])
        return redirect(url_for('index', sucesso=1))
    
    return redirect(url_for('index'))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000)) 
    app.run(host="0.0.0.0", port=port, debug=True)