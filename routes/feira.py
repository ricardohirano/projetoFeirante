from flask import (
    Blueprint, render_template, request, 
    redirect, url_for, flash, session
)
from datetime import datetime
# Importa os "bancos de dados"
from database.feira import (
    CIDADES, FEIRAS_REGISTRO, FEIRANTE_AGENDA, 
    buscar_feira_por_id, DIAS_SEMANA_MAP
)
from database.produto import PRODUTOS, CATEGORIAS, buscar_produtos_por_ids
from routes.usuario import buscar_usuario_por_id

feira_route = Blueprint('feira', __name__, url_prefix='/feira')


# --- ROTA 1: PÁGINA 1 (Selecionar Feira e Data) ---
@feira_route.route('/', methods=["GET", "POST"])
def selecionar_feira():
    if 'usuario_id' not in session:
        flash("Você precisa estar logado.", "error")
        return redirect(url_for("home.login_feirante"))
        
    if request.method == "POST":
        feira_id = int(request.form.get("feira_id"))
        data_str = request.form.get("data")
        
        try:
            data_obj = datetime.strptime(data_str, '%Y-%m-%d')
            dia_semana_escolhido = data_obj.weekday() 
            feira = buscar_feira_por_id(feira_id)
            dia_semana_requerido = feira.get("dia_semana_num")
            if dia_semana_escolhido != dia_semana_requerido:
                dia_requerido_nome = DIAS_SEMANA_MAP[dia_semana_requerido]
                dia_escolhido_nome = DIAS_SEMANA_MAP[dia_semana_escolhido]
                data_formatada_flash = data_obj.strftime('%d/%m/%Y')
                flash(f"Data inválida! A '{feira['nome']}' só acontece às {dia_requerido_nome}s, mas a data {data_formatada_flash} é uma {dia_escolhido_nome}.", "error")
                return redirect(url_for('feira.selecionar_feira'))
        except ValueError:
            flash("Formato de data inválido.", "error")
            return redirect(url_for('feira.selecionar_feira'))
        
        session['feira_agendamento_temp'] = {
            "feira_id": feira_id,
            "data": data_str
        }
        
        return redirect(url_for('feira.selecionar_produtos'))

    # --- ATUALIZAÇÃO DO MENU SIDENAV ---
    # (Removido "Meus Agendamentos")
    links_sidenav = [
        {"url": url_for('home.painel_usuario'), "titulo": "Inicial", "ativo": False},
        {"url": url_for('feira.selecionar_feira'), "titulo": "Feiras", "ativo": True},
        {"url": url_for('produto.lista_produtos'), "titulo": "Produtos", "ativo": False},
        {"url": url_for('home.dados_usuarios'), "titulo": "Dados Usuarios", "ativo": False}
    ]
    
    hoje_str = datetime.now().strftime('%Y-%m-%d')
    
    return render_template(
        "agendar_feira.html",
        menu=links_sidenav,
        cidades=CIDADES, 
        feiras_disponiveis=FEIRAS_REGISTRO,
        min_date=hoje_str
    )

# --- ROTA 2: PÁGINA 2 (Selecionar Produtos) ---
@feira_route.route('/selecionar-produtos', methods=["GET"])
def selecionar_produtos():
    if 'usuario_id' not in session:
        return redirect(url_for("home.login_feirante"))

    agendamento_temp = session.get('feira_agendamento_temp')
    if not agendamento_temp:
        flash("Por favor, selecione a feira e a data primeiro.", "info")
        return redirect(url_for('feira.selecionar_feira'))

    id_logado = session['usuario_id']
    feira_info = buscar_feira_por_id(agendamento_temp['feira_id'])
    
    data_str = agendamento_temp['data']
    data_obj = datetime.strptime(data_str, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d/%m/%Y')
    
    meus_produtos_cadastrados = []
    for p in PRODUTOS:
        if p.get('usuario_id') == id_logado:
            meus_produtos_cadastrados.append(p)

    produtos_agrupados = {}
    for cat in CATEGORIAS:
        produtos_desta_categoria = []
        for p in meus_produtos_cadastrados:
            if p.get('categoria') == cat:
                produtos_desta_categoria.append(p)
        
        if produtos_desta_categoria:
            produtos_agrupados[cat] = produtos_desta_categoria

    return render_template(
        "confirmar_feira_produtos.html",
        feira=feira_info,
        data_formatada=data_formatada,
        produtos_agrupados=produtos_agrupados
    )

# --- ROTA 3: PÁGINA 3 (Preview) ---
@feira_route.route('/preview-agendamento', methods=["POST"])
def preview_agendamento():
    if 'usuario_id' not in session:
        return redirect(url_for("home.login_feirante"))

    id_logado = session['usuario_id']
    
    agendamento_temp = session.get('feira_agendamento_temp')
    if not agendamento_temp:
        return redirect(url_for('feira.selecionar_feira'))

    produtos_selecionados_ids = request.form.getlist("produto_ids")
    produtos_ids_int = [int(id_str) for id_str in produtos_selecionados_ids]

    session['feira_agendamento_temp']['produtos_ids'] = produtos_ids_int
    session.modified = True

    usuario_info = buscar_usuario_por_id(id_logado)
    feira_info = buscar_feira_por_id(agendamento_temp['feira_id'])
    
    data_obj = datetime.strptime(agendamento_temp['data'], '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d/%m/%Y')

    produtos_selecionados_detalhes = buscar_produtos_por_ids(produtos_ids_int)

    produtos_agrupados_preview = {}
    for cat in CATEGORIAS:
        produtos_desta_categoria = []
        for p in produtos_selecionados_detalhes:
            if p.get('categoria') == cat:
                produtos_desta_categoria.append(p)
        
        if produtos_desta_categoria:
            produtos_agrupados_preview[cat] = produtos_desta_categoria

    return render_template(
        "preview_agendamento.html",
        usuario=usuario_info,
        feira=feira_info,
        data=data_formatada,
        produtos_agrupados=produtos_agrupados_preview 
    )

# --- ROTA 4: SALVAR FINAL (Botão "Confirmar" da Página 3) ---
@feira_route.route('/salvar-agendamento-final', methods=["POST"])
def salvar_agendamento_final():
    if 'usuario_id' not in session:
        return redirect(url_for("home.login_feirante"))

    id_logado = session['usuario_id']
    
    agendamento_final = session.get('feira_agendamento_temp')
    if not agendamento_final:
        return redirect(url_for('feira.selecionar_feira'))

    # Salva no "banco de dados"
    ultimo_id = FEIRANTE_AGENDA[-1]["id_agenda"] if FEIRANTE_AGENDA else 0
    novo_agendamento = {
        "id_agenda": ultimo_id + 1,
        "usuario_id": id_logado,
        "feira_id": agendamento_final['feira_id'],
        "data_escolhida": agendamento_final['data'],
        "produtos_selecionados": agendamento_final['produtos_ids'],
        "status": "pendente"
    }
    FEIRANTE_AGENDA.append(novo_agendamento)
    
    session.pop('feira_agendamento_temp', None)
    
    flash("Agendamento enviado para moderação!", "success")
    return redirect(url_for('feira.minhas_feiras'))

# --- ROTA 5: CANCELAR (do Preview) ---
@feira_route.route('/cancelar-agendamento-final', methods=["POST"])
def cancelar_agendamento_final():
    session.pop('feira_agendamento_temp', None)
    flash("Agendamento cancelado.", "info")
    return redirect(url_for('home.painel_usuario'))


# --- ROTA 6: PÁGINA "Meus Agendamentos" ---
@feira_route.route('/minhas-feiras', methods=["GET"])
def minhas_feiras():
    if 'usuario_id' not in session:
        flash("Você precisa estar logado.", "error")
        return redirect(url_for("home.login_feirante"))
        
    id_logado = session['usuario_id']
    usuario_info = buscar_usuario_por_id(id_logado)

    agendamentos_pendentes = []
    for agendamento in FEIRANTE_AGENDA:
        if (agendamento.get('usuario_id') == id_logado and
            agendamento.get('status') == 'pendente'):
            
            feira_info = buscar_feira_por_id(agendamento['feira_id'])
            # --- CORREÇÃO: Lê os produtos do SNAPSHOT ---
            produtos_lista = agendamento.get('produtos_snapshot', []) 
            data_obj = datetime.strptime(agendamento['data_escolhida'], '%Y-%m-%d')
            data_formatada = data_obj.strftime('%d/%m/%Y')
            
            produtos_agrupados = {}
            for cat in CATEGORIAS:
                produtos_cat = [p for p in produtos_lista if p.get('categoria') == cat]
                if produtos_cat:
                    produtos_agrupados[cat] = produtos_cat
            
            agendamentos_pendentes.append({
                "id_agenda": agendamento['id_agenda'],
                "feira": feira_info,
                "data": data_formatada,
                "usuario": usuario_info,
                "produtos_agrupados": produtos_agrupados
            })

    # --- ATUALIZAÇÃO DO MENU SIDENAV ---
    # (Removido "Meus Agendamentos" e corrigido "ativo")
    links_sidenav = [
        {"url": url_for('home.painel_usuario'), "titulo": "Inicial", "ativo": False},
        {"url": url_for('feira.selecionar_feira'), "titulo": "Feiras", "ativo": True}, # A "mãe" está ativa
        {"url": url_for('produto.lista_produtos'), "titulo": "Produtos", "ativo": False},
        {"url": url_for('home.dados_usuarios'), "titulo": "Dados Usuarios", "ativo": False}
    ]
    
    return render_template(
        "minhas_feiras.html",
        menu=links_sidenav,
        agendamentos=agendamentos_pendentes
    )

# --- ROTA 7: CANCELAR AGENDAMENTO SALVO ---
@feira_route.route('/deletar-agendamento-salvo/<int:agendamento_id>', methods=["POST"])
def deletar_agendamento_salvo(agendamento_id):
    if 'usuario_id' not in session:
        return redirect(url_for("home.login_feirante"))
    
    id_logado = session['usuario_id']
    
    agendamento = next((a for a in FEIRANTE_AGENDA if a["id_agenda"] == agendamento_id), None)
    
    if not agendamento or agendamento['usuario_id'] != id_logado:
        flash("Erro ao cancelar agendamento.", "error")
    else:
        FEIRANTE_AGENDA.remove(agendamento)
        flash("Agendamento cancelado com sucesso.", "success")
        
    return redirect(url_for('feira.minhas_feiras'))