from flask import Blueprint, render_template

home_route = Blueprint('home', __name__)

#rota Login
@home_route.route('/')
def login_feirante():
    return render_template('loginFeirante.html')

#Rota cadastre-se
@home_route.route('/cadastro')
def cadastro_usuario():
    return render_template('cadastroUsuario.html')
#Rota esqueci a senha
@home_route.route('/esqueciSenha')
def esqueci_senha():
    return render_template('esqueciSenha.html')
#Rota 
@home_route.route('/menuUsuario')
def menu_usuario():
    return render_template('menuUsuario.html')
