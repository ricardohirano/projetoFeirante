from flask import (
    Blueprint, render_template, request, 
    redirect, url_for, flash, session
)
from werkzeug.security import generate_password_hash, check_password_hash
from database.usuario import USUARIOS
from routes.usuario import buscar_usuario_por_id, buscar_usuario_por_email

home_route = Blueprint('home', __name__)

#Rota login
@home_route.route('/', methods=["GET","POST"])
def login_feirante():
    if request.method == "POST":
        email = request.form.get("email")
        senha_digitada = request.form.get("senha") 
        usuario_encontrado = buscar_usuario_por_email(email)
        if (usuario_encontrado and 
            check_password_hash(usuario_encontrado.get("senha"), senha_digitada)):
            session['usuario_id'] = usuario_encontrado.get('id')
            flash("Login realizado com sucesso!","success") 
            return redirect(url_for("home.painel_usuario"))
        else:
            flash("Email ou senha inválida, tente novamente.","error")
            return render_template("loginFeirante.html")
    if 'usuario_id' in session:
        return redirect(url_for('home.painel_usuario'))
    return render_template("loginFeirante.html")

# Rota esqueci a senha
@home_route.route('/esqueciSenha', methods=["GET","POST"])
def esqueci_senha():
    if request.method == "POST":
        email = request.form.get("email")
        cpf_cnpj = request.form.get("cpf_cnpj")
        usuario = buscar_usuario_por_email(email)
        if usuario and usuario.get("cpf_cnpj") == cpf_cnpj:
            session['email_para_redefinir'] = email
            return redirect(url_for("home.redefinir_senha"))
        else:
            flash("Email ou CPF/CNPJ não confere com o cadastro", "error")
            return render_template('esqueci_senha.html')
    return render_template('esqueci_senha.html')

#Rota redefinir senha
@home_route.route('/redifinir-senha', methods=["GET", "POST"])
def redefinir_senha():
    if 'email_para_redefinir' not in session:
        flash("Você precisa verificar seu email e CPF primeiro.", "error")
        return redirect(url_for("home.esqueci_senha")) 
    
    email = session.get('email_para_redefinir')

    if request.method == "POST":
        senha = request.form.get("senha")
        confirme_senha = request.form.get("confirme_senha")

        if senha != confirme_senha:
            flash("As senhas não conferem.", "error")
            return render_template("redefinir_senha.html")
            
        usuario = buscar_usuario_por_email(email)
        
        if usuario:
            hash_da_senha = generate_password_hash(senha)
            usuario['senha'] = hash_da_senha
            session.pop('email_para_redefinir', None)
            flash("Sua senha foi redefinida com sucesso!", "success")
            return redirect(url_for("home.login_feirante"))
        else:
            flash("Erro ao encontrar usuário. Tente novamente.", "error")
            return redirect(url_for("home.login_feirante"))

    return render_template("redefinir_senha.html")

#Rota painel do feirante
@home_route.route("/painel")
def painel_usuario():
    if 'usuario_id' not in session:
        flash("Voce precisa estar logado para ver essa página.", "error")
        return redirect(url_for("home.login_feirante"))
    id_logado = session['usuario_id']
    usuario_real = buscar_usuario_por_id(id_logado)
    if not usuario_real:
        session.pop('usuario_id', None)
        flash("Usuário não encontrado. Faça login novamente.", "error")
        return redirect(url_for("home.login_feirante"))
    
    estatisticas = {
        "visualizacoes": 123, 
        "gostei": 321,
        "favoritos": 312,
        "dias_premium": 0
    }

   
    links_sidenav = [
        {"url": url_for('home.painel_usuario'), "titulo": "Inicial", "ativo": True},
        {"url": url_for('feira.selecionar_feira'), "titulo": "Agendar Feira", "ativo": False},
        {"url": url_for('produto.lista_produtos'), "titulo": "Produtos", "ativo": False},
        {"url": url_for('home.dados_usuarios'), "titulo": "Dados Usuarios", "ativo": False}
    ]

    return render_template(
        "painel_usuario.html",
        usuario = usuario_real,
        stats = estatisticas,
        menu = links_sidenav
    )

#Rota de dados do usuario
@home_route.route("/dados-usuario", methods=["GET","POST"])
def dados_usuarios():
    if 'usuario_id' not in session:
        flash("Voce precisa estar logado para ver essa página.", "error")
        return redirect(url_for("home.login_feirante"))
        
    id_logado = session['usuario_id']
    usuario_real = buscar_usuario_por_id(id_logado)

    if not usuario_real:
        session.pop('usuario_id', None)
        flash("Usuario não encontrado. Faça login novamente.", "error")
        return redirect(url_for("home.login_feirante"))
    
    if request.method == "POST":
        usuario_real['nome'] = request.form.get("nome")
        usuario_real['telefone'] = request.form.get("telefone")
        usuario_real['nome_fantasia'] = request.form.get("nome_fantasia")
        usuario_real['bio'] = request.form.get("bio")
        
        flash("Dados atualizados com sucesso!", "success")
        return redirect(url_for('home.dados_usuarios'))

 
    links_sidenav = [
        {"url": url_for('home.painel_usuario'), "titulo": "Inicial", "ativo": False},
        {"url": url_for('feira.selecionar_feira'), "titulo": "Agendar Feira", "ativo": False},
        {"url": url_for('produto.lista_produtos'), "titulo": "Produtos", "ativo": False},
        {"url": url_for('home.dados_usuarios'), "titulo": "Dados Usuarios", "ativo": True}
    ]
    
    return render_template(
        "dados_usuarios.html",
        usuario = usuario_real,
        menu = links_sidenav
    )

#Rota mudar senha
@home_route.route('/mudar-senha', methods=["GET", "POST"])
def mudar_senha():
    if 'usuario_id' not in session:
        flash("Voce precisa estar logado para ver essa página.", "error")
        return redirect(url_for("home.login_feirante"))

    id_logado = session['usuario_id']
    usuario_real = buscar_usuario_por_id(id_logado)

    if not usuario_real:
        session.pop('usuario_id', None)
        return redirect(url_for("home.login_feirante"))

    if request.method == "POST":
        senha_antiga = request.form.get("senha_antiga")
        senha_nova = request.form.get("senha_nova")
        confirme_senha_nova = request.form.get("confirme_senha_nova")

        if not check_password_hash(usuario_real.get("senha"), senha_antiga):
            flash("A sua 'Senha antiga' está incorreta.", "error")
            return render_template("mudar_senha.html")

        if senha_nova != confirme_senha_nova:
            flash("A 'Senha nova' e a 'Confirmação' não são iguais.", "error")
            return render_template("mudar_senha.html")

        hash_da_senha_nova = generate_password_hash(senha_nova)
        usuario_real['senha'] = hash_da_senha_nova
        
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for("home.dados_usuarios"))

    return render_template("mudar_senha.html")

# rota Logout
@home_route.route("/logout")
def logout():
    session.pop('usuario_id', None)
    session.pop('email_para_redefinir', None) 
    flash("Você saiu com sucesso.", "success")
    return redirect(url_for("home.login_feirante"))