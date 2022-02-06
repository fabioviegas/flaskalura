from crypt import methods

from flask import Flask, render_template, \
    request, redirect, session, flash, url_for  # importando a classe Flask do pacote flask

app = Flask(__name__)
# essa secret_key é necessária para o flask poder encriptar o objeto session
app.secret_key = 'qualquer_coisa'


class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console


class Usuario:
    def __init__(self, id, nome, senha):
        self.id = id
        self.nome = nome
        self.senha = senha


usuario1 = Usuario('fabio.viegas', 'Fábio Viegas', '1234')
usuario2 = Usuario('fulano.silva', 'Fulano Silva', '4321')
usuario3 = Usuario('caju.zeiro', 'Cão Caju', 'ossos')

usuarios = {usuario1.id: usuario1,
            usuario2.id: usuario2,
            usuario3.id: usuario3}

jogo1 = Jogo('Super Mario', 'Ação', 'Super Nintendo')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GBA')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'Super Nintendo')
lista = [jogo1, jogo2, jogo3]


# ATENCAO: EH CONVENSAO TER UMA PASTA TEMPLATES COM OS .HTML DENTRO!
# Outra convenção: ter na pasta static os css, js, imagens e etc.
@app.route('/')
def index():
    return render_template('lista.html',
                           titulo='Jogos',
                           jogos=lista)  # esses parametros nomeados vão lá para a view lista.html


@app.route('/novo')
def novo():
    # verificar se o usuario não está na sessao ou se fez logout
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        # é mais elegante pegar essas rotas utilizado o url_for
        # o qual vai receber o nome da funçao que quero ir, sem os ()
        # e se precisar passar uma parâmetro, passa como se fosse render_template
        # forma antiga: return redirect('/login?proxima=novo')
        return redirect(url_for('login', proxima_pagina=url_for('novo')))

    return render_template('novo.html', titulo='Novo Jogo')


# PEGANDO INFORMACAO QUE ESTÁ VINDO DA VIEW (REQUEST)
# Por padrão uma rota só aceita GET, tem que colocar POST
@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']

    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)

    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima_pagina')  # pegando o atributo que passei em novo()
    return render_template('login.html', proxima_pagina=proxima)


@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if usuario.senha == request.form['senha']:
            # essa sessao fica num cookie, no cliente
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima_pagina']
            return redirect(proxima_pagina)
        else:
            flash('Login ou senha incorretos.')
            return redirect(url_for('login'))  # isso aqui redireciona para a rota de login!


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


# app.run(debug=True)
app.run(host="192.168.0.18")
