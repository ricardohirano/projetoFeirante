from flask import Blueprint, render_template

home_route = Blueprint('home', __name__)

#rota Login
@home_route.route('/')
def login_feirante():
    return render_template('loginFeirante.html')
    
#Rota esqueci a senha
@home_route.route('/esqueciSenha')
def esqueci_senha():
    return render_template('esqueciSenha.html')

# rota temporária pra abrir o menu direto
@home_route.route("/menu")
def menu_usuario():
    # apenas renderiza o template, sem depender de id ou sessão
    return render_template("menuUsuario.html")