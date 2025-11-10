PRODUTOS = [
    {
        "id": 1,
        "usuario_id": 1, 
        "nome": "Alface Crespa",
        "preco": "2,50",
        "unidade": "un",
        "categoria": "verduras", 
        "descricao": "Alface fresquinha colhida hoje.",
        "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Lactuca_sativa_%27Ashbrook%27.jpg/640px-Lactuca_sativa_%27Ashbrook%27.jpg"
    },
    {
        "id": 2,
        "usuario_id": 1, 
        "nome": "Beterraba",
        "preco": "3,00",
        "unidade": "kg",
        "categoria": "legumes", 
        "descricao": "Beterraba orgânica.",
        "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Beets-Bundle.jpg/640px-Beets-Bundle.jpg"
    },
    {
        "id": 3,
        "usuario_id": 1, 
        "nome": "Banana Prata",
        "preco": "5,00",
        "unidade": "penca",
        "categoria": "frutas", 
        "descricao": "Penca de banana prata madura.",
        "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Banana-Single.jpg/1024px-Banana-Single.jpg"
    },
    {
        "id": 4,
        "usuario_id": 1, 
        "nome": "Filé de Tilápia",
        "preco": "25,00",
        "unidade": "kg",
        "categoria": "peixes", 
        "descricao": "Filé de tilápia fresco, sem espinhos.",
        "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Cardona%2CRizalFishPortjf5152_08.JPG/640px-Cardona%2CRizalFishPortjf5152_08.JPG"
    },
    {
        "id": 5,
        "usuario_id": 1, 
        "nome": "Mel Silvestre",
        "preco": "15,00",
        "unidade": "un", 
        "categoria": "outros", 
        "descricao": "Pote de 500g de mel silvestre puro.",
        "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/%D0%92%D1%8B%D1%81%D0%BE%D0%BA%D0%BE%D0%B3%D0%BE%D1%80%D0%BD%D1%8B%D0%B9_%D0%BC%D1%91%D0%B4.jpg/640px-%D0%92%D1%8B%D1%81%D0%BE%D0%BA%D0%BE%D0%B3%D0%BE%D1%80%D0%BD%D1%8B%D0%B9_%D0%BC%D1%91%D0%B4.jpg"
    }
]


CATEGORIAS = ["frutas", "verduras", "legumes", "peixes", "outros"]
UNIDADES = ["un", "kg", "maco", "penca", "duzia", "bandeja", "pacote", "litro"]

def buscar_produtos_por_ids(lista_de_ids: list):
    """
    Recebe uma lista de IDs (ex: [1, 3, 5]) e retorna
    a lista completa dos dicionários desses produtos.
    """
    produtos_encontrados = []
    # Faz um loop pela lista de IDs que o usuário selecionou
    for produto_id in lista_de_ids:
        # Procura o produto na base de dados
        produto = next((p for p in PRODUTOS if p["id"] == produto_id), None)
        # Se o produto for encontrado, adiciona à lista
        if produto:
            produtos_encontrados.append(produto)
    return produtos_encontrados