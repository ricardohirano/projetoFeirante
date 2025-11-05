from flask import Blueprint, render_template, request, abort
from database.usuario import USUARIOS

usuario_route = Blueprint("usuario", __name__)

def buscar_usuario_por_id(usuario_id: int):
    return next((u for u in USUARIOS if u["id"] == usuario_id), None)

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
@usuario_route.get("/cadastro", endpoint="formulario_usuario")
def formulario_usuario():
    return render_template("cadastroUsuario.html")
