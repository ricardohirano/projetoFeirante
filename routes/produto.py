from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
# IMPORTANTE: Importe CATEGORIAS e UNIDADES
from database.produto import PRODUTOS, CATEGORIAS, UNIDADES
# --- 1. NOVA IMPORTAÇÃO ---
# Precisamos de aceder à agenda de feiras para verificar se o produto está a ser usado
from database.feira import FEIRANTE_AGENDA 
from routes.usuario import buscar_usuario_por_id

produto_route = Blueprint('produto', __name__, url_prefix='/produto')

# --- ROTA DA LISTA DE PRODUTOS ---
@produto_route.route('/')
def lista_produtos():
    if 'usuario_id' not in session:
        flash("Voce precisa estar logado.", "error")
        return redirect(url_for("home.login_feirante"))
    
    id_logado = session['usuario_id']

    # (A lógica de agrupamento está correta)
    produtos_do_usuario = []
    for p in PRODUTOS:
        if p.get('usuario_id') == id_logado:
            produtos_do_usuario.append(p)
    
    produtos_agrupados = {}
    for cat in CATEGORIAS:
        produtos_desta_categoria = []
        for p in produtos_do_usuario:
            if p.get('categoria') == cat:
                produtos_desta_categoria.append(p)
        
        if produtos_desta_categoria:
            produtos_agrupados[cat] = produtos_desta_categoria

    # --- 2. CORREÇÃO DO MENU SIDENAV ---
    # (Removido "Meus Agendamentos")
    links_sidenav = [
        {"url": url_for('home.painel_usuario'), "titulo": "Inicial", "ativo": False},
        {"url": url_for('feira.selecionar_feira'), "titulo": "Agendar Feira", "ativo": False},
        {"url": url_for('produto.lista_produtos'), "titulo": "Produtos", "ativo": True},
        {"url": url_for('home.dados_usuarios'), "titulo": "Dados Usuarios", "ativo": False}
    ]
    
    return render_template(
        "lista_produtos.html",
        produtos_agrupados=produtos_agrupados, 
        menu=links_sidenav
    )

# --- Rota criar o form para produtos ---
@produto_route.route('/form', defaults={'produto_id': None}, methods=["GET"])
@produto_route.route('/form/<int:produto_id>', methods=["GET"])
def form_produto(produto_id):
    if 'usuario_id' not in session:
        flash("Você precisa estar logado", "error")
        return redirect(url_for("home.login_feirante"))
    id_logado = session['usuario_id']

    if produto_id:
        produto = next((p for p in PRODUTOS if p['id'] == produto_id), None)
        if not produto or produto['usuario_id'] != id_logado:
            flash("Produto não encontrado.", "error")
            return redirect(url_for('produto.lista_produtos'))
        
        page_title = "Editar Produto"
    else:
        produto = {}
        page_title = "Cadastro de Produto" 
        
    return render_template(
        "form_produto.html",
        page_title=page_title,
        produto=produto,
        categorias=CATEGORIAS,
        unidades=UNIDADES
        )

# --- Rota processar o form ---
@produto_route.route('/form', defaults={'produto_id': None}, methods=["POST"])
@produto_route.route('/form/<int:produto_id>', methods=["POST"])
def processar_form_produto(produto_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home.login_feirante"))
    
    id_logado = session['usuario_id'] 

    nome = request.form.get("nome")
    preco = request.form.get("preco")
    categoria = request.form.get("categoria")
    unidade = request.form.get("unidade")
    descricao = request.form.get("descricao")
    imagem_url = request.form.get("imagem_url")

    if produto_id:
        produto = next((p for p in PRODUTOS if p['id'] == produto_id), None)
        if not produto or produto['usuario_id'] != id_logado:
            abort(404) 
        
        produto['nome'] = nome
        produto['preco'] = preco
        produto['categoria'] = categoria
        produto['unidade'] = unidade
        produto['descricao'] = descricao
        produto['imagem_url'] = imagem_url
        
        flash("Produto atualizado com sucesso!", "success")
    else:
        ultimo_id = PRODUTOS[-1]["id"] if PRODUTOS else 0
        novo_id = ultimo_id + 1
        
        novo_produto = {
            "id": novo_id,
            "usuario_id": id_logado,
            "nome": nome,
            "preco": preco,
            "unidade": unidade,
            "categoria": categoria,
            "descricao": descricao,
            "imagem_url": imagem_url
        }
        PRODUTOS.append(novo_produto)
        flash("Produto cadastrado com sucesso!", "success")

    return redirect(url_for('produto.lista_produtos'))

# --- 3. CORREÇÃO DA ROTA DELETAR ---
@produto_route.route('/delete/<int:produto_id>', methods=["POST"])
def deletar_produto(produto_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home.login_feirante"))
    
    id_logado = session['usuario_id']
    
    produto = next((p for p in PRODUTOS if p['id'] == produto_id), None)
    
    if not produto or produto['usuario_id'] != id_logado:
        flash("Erro ao deletar produto.", "error")
        return redirect(url_for('produto.lista_produtos'))
    
    # --- NOVA LÓGICA DE VERIFICAÇÃO ---
    is_agendado = False
    for agendamento in FEIRANTE_AGENDA:
        # Verifica se o produto está na lista de agendamentos deste usuário
        if (agendamento.get('usuario_id') == id_logado and 
            agendamento.get('status') == 'pendente' and
            produto_id in agendamento.get('produtos_selecionados', [])):
            
            is_agendado = True
            break # Encontrou, não precisa de procurar mais
    
    if is_agendado:
        # Se está agendado, NÃO deixa apagar
        flash(f"O produto '{produto.get('nome')}' não pode ser deletado, pois está incluído num agendamento pendente. Cancele o agendamento primeiro.", "error")
    else:
        # Se não está agendado, apaga
        PRODUTOS.remove(produto)
        flash("Produto deletado com sucesso.", "success")
        
    return redirect(url_for('produto.lista_produtos'))