from flask import Flask, render_template, request, redirect, session
import pyodbc
connect = ("Driver={SQL Server};"
          "Server=localhost\SQLEXPRESS;"
          "Database=Login")
conexao = pyodbc.connect(connect)
cursor = conexao.cursor()
app = Flask(__name__)
app.secret_key = 'Tonny'
@app.route('/')
def home():
    return render_template('home.html', texto_aviso=None)
@app.route('/login.html', methods=['POST','GET'])
def login():
    texto_aviso = ' '
    texto_aviso_2 = ' '
    if request.method == 'POST':
        try:
            email = request.form.get('femail')
            senha = request.form.get('fsenha')
            selecionar_email = f"""SELECT email, senha FROM Dados_Usuário WHERE email = '{email}' and senha = '{senha}'"""
            cursor.execute(selecionar_email)
            verificador = cursor.fetchone()
            if verificador is None:
                texto_aviso = 'Usuario Inválido!' 
                texto_aviso_2 = 'E-mail e/ou Senha Incorretos!'
                return render_template('home.html', texto_aviso=texto_aviso, texto_aviso_2 = texto_aviso_2)
            else:
                session['email'] = email
                return redirect('inicio.html')
        except Exception:
            pass

@app.route('/inicio.html', methods=['POST','GET'])
def inicio():
    email = session['email']
    nome_usuario = f"""SELECT nome FROM Dados_Usuário WHERE email = '{email}' """
    cursor.execute(nome_usuario)
    user = cursor.fetchone()
    username = user[0]
    x = 1
    y = 0
    while username[y] != ' ':
        x+=1
        y+=1
    username = username[:y]
        
    return render_template('inicio.html', username = username)
   

@app.route('/cadastro.html', methods=['post','get'])
def cadastrar():
    if request.method == 'POST':
        try:
            nome = request.form.get('fname')
            senha = request.form.get('fsenha')
            data = request.form.get('fdata')
            genero = request.form.get('fsexo')
            email = request.form.get('femail')
            comando = f"""INSERT INTO Dados_Usuário(nome,senha,data_nascimento,sexo,email) 
                          VALUES('{nome}','{senha}','{data}','{genero}','{email}')"""
            
            cursor.execute(comando)
            conexao.commit()  
            return render_template('home.html')
        except Exception:
            pass
    else:
        return render_template('cadastro.html')
if __name__ == '__main__':
    app.run()
