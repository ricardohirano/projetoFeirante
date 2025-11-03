from flask import Blueprint, render_template, request, abort
from database.usuario import USUARIOS

usuario_route = Blueprint("usuario", __name__)

def buscar_usuario_por_id(usuario_id: int):
    return next((u for u in USUARIOS if u["id"] == usuario_id), None)

@usuario_route.route("/")
def listar_usuarios():
    return render_template("listaUsuarios.html", usuarios=USUARIOS)

@usuario_route.get("/<int:usuario_id>", endpoint="editar_usuario")
def editar_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        abort(404)
    return render_template("_usuario_form.html", usuario=usuario)

@usuario_route.route("/<int:usuario_id>", methods=["PUT"], endpoint="atualizar_usuario")
def atualizar_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        abort(404)

    nome = request.form.get("nome", "").strip()
    email = request.form.get("email", "").strip()
    tipo = request.form.get("tipo", "").strip()
    if not nome or not email or not tipo:
        abort(400, description="Campos obrigatórios faltando")

    usuario["nome"] = nome
    usuario["email"] = email
    usuario["tipo"] = tipo
    return render_template("_usuario_row.html", usuario=usuario)

@usuario_route.route("/<int:usuario_id>", methods=["DELETE"], endpoint="excluir_usuario")
def excluir_usuario(usuario_id):
    usuario = buscar_usuario_por_id(usuario_id)
    if not usuario:
        abort(404)
    USUARIOS.remove(usuario)
    return "", 204

# GET /usuario/cadastro → mostra o formulário de cadastro
@usuario_route.get("/cadastro", endpoint="formulario_usuario")
def formulario_usuario():
    return render_template("cadastroUsuario.html")
