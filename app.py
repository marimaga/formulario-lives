from flask import Flask, render_template, request, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
from google.auth.transport.requests import AuthorizedSession

app = Flask(__name__)

# --- CONFIGURAÇÃO DO GOOGLE SHEETS ---
scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "formulario-duvidas-membros-26a23b27f193.json",
    scopes=scope
)

authed_session = AuthorizedSession(creds)
gc = gspread.Client(auth=creds)
gc.session = authed_session

sh = gc.open("Formulário Dúvidas Membros")
worksheet = sh.sheet1

# --- ROTAS DO FLASK ---
@app.route('/')
def index():
    sucesso = request.args.get('sucesso')
    return render_template('form.html', sucesso=sucesso)

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    username_discord = request.form['username_discord']
    duvida = request.form['duvida']

    worksheet.append_row([nome, username_discord, duvida])

    # redireciona de volta com parâmetro de sucesso
    return redirect(url_for('index', sucesso='1'))

if __name__ == '__main__':
    app.run(debug=True)