from flask import (Blueprint, render_template, request, abort, flash, session, redirect, url_for)
from werkzeug.security import generate_password_hash
from database.usuario import USUARIOS


usuario_route = Blueprint("usuario", __name__)

def buscar_usuario_por_id(usuario_id: int):
    return next((u for u in USUARIOS if u["id"] == usuario_id), None)

def buscar_usuario_por_email(email: str):
    for u in USUARIOS:
        if u.get("email") == email:
            return u
    return None

@usuario_route.route("/")
def listar_usuarios():
    return render_template("listaUsuarios.html", usuarios=USUARIOS)

@usuario_route.get("/<int:usuario_id>")
def editar_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        abort(404)
    return render_template("_usuario_row.html", usuario=usuario)

@usuario_route.put("/<int:usuario_id>")
def atualizar_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        abort(404)

    data = request.get_json(force=True)
    usuario["nome"] = data.get("nome", usuario["nome"])
    usuario["email"] = data.get("email", usuario["email"])
    usuario["tipo"] = data.get("tipo", usuario["tipo"])
    return render_template("_usuario_row.html", usuario=usuario)

@usuario_route.delete("/<int:usuario_id>")
def excluir_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        abort(404)
    USUARIOS.remove(usuario)
    return "", 204

# GET /usuario/cadastro → mostra o formulário de cadastro
@usuario_route.route(
    "/cadastro", 
    methods=["GET", "POST"], 
    endpoint="cadastrar_usuario"
)
#cadastro vindo do formulario
def cadastrar_usuario():
    
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        confirme_email = request.form.get("confirme_email")
        senha = request.form.get("senha")
        confirme_senha = request.form.get("confirme_senha")
        cpf = request.form.get("cpf")
        telefone = request.form.get("telefone")

        if email != confirme_email:
            flash("os emails não conferem!", "error")
            return render_template("cadastroUsuario.html")
        if senha != confirme_senha:
            flash("As senhas não conferem!", "error")
            return render_template("cadastroUsuario.html")
        
        if buscar_usuario_por_email(email):
            flash("Este email já está cadastrado. Tente outro.", "erro")
            return render_template("cadastroUsuario.html") 
        
        hash_da_senha = generate_password_hash(senha)
        #novo_id e novo_usuario com tipo:feirante como default 

        ultimo_id = USUARIOS[-1]["id"] if USUARIOS else 0
        novo_id = ultimo_id +1

        novo_usuario = {
            "id" : novo_id,
            "nome" : nome,
            "email" : email, 
            "cpf_cnpj": cpf, 
            "telefone": telefone, 
            "tipo" : "feirante",
            "senha" : hash_da_senha
        }

        USUARIOS.append(novo_usuario)

        flash("Cadastro realizado com sucesso! Faça seu login.", "successo")
        return redirect(url_for("home.login_feirante"))
    return render_template("cadastroUsuario.html")
