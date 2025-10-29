from flask import Blueprint, render_template
from database.usuario import USUARIOS

usuario_route = Blueprint('usuario', __name__)

#   /usuario/ (get)- listar os usuarios 
@usuario_route.route('/')
def listar_usuarios():
    return render_template('listaUsuarios.html', usuarios=USUARIOS)

#   /usuario/ (post)- inserir o usuario no servidor  
@usuario_route.route('/', methods=['POST'])
def inserir_usuario():
    pass


#   /usuario/new (get)- mostrar o formulario de cadastro do usuario
@usuario_route.route('/cadastro')
def formulario_usuario():
    return render_template('cadastroUsuario.html')

'''
#   /usuario/<id> (get)- pagina inicial  do usuario
@usuario_route.route('/<int:usuario_id>')
def dados_usuario():
    return render_template('menuUsuario.html')
'''

#   /usuario/<id>/edit (get)- editar o usuario
@usuario_route.route('/<int:usuario_id>')
def editar_usuario():
    return render_template('edicaoUsuario.html')


#   /usuario/<id>/update (put)- atualizar o usuario
@usuario_route.route('/<int:usuario_id>', methods=['PUT'])
def update_usuario():
    pass


#   /usuario/<id>/delete (delete) -deletar o registro do usuario
@usuario_route.route('/<int:usuario_id>', methods=['DELETE'])
def delete_usuario():
    pass
