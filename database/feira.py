from datetime import datetime

CIDADES = ["Registro"]

FEIRAS_REGISTRO = [
    {
        "id": 1,
        "nome": "Feira do Produtor Rural",
        "dia_semana_num": 3, # Quinta-feira
        "horario": "Quintas-feiras, 16:00–20:00",
        "endereco": "Rua Haguemu Matsuzawa, 875 - Vila Ribeiropolis, Registro - SP",
        "mapa_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3630.426960252465!2d-47.842829224640404!3d-24.505304278162846!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94c53483d32b663d%3A0x2c7761c257f57d8a!2sR.%20Haguemu%20Matsuzawa%2C%20875%20-%20Vila%20Ribeiropolis!5e0!3m2!1spt-BR!2sbr!4v1762723555856!5m2!1spt-BR!2sbr"
    },
    {
        "id": 2,
        "nome": "Feira Sabores da Terra",
        "dia_semana_num": 5, # Sábado
        "horario": "Sábados, 09:00–13:00",
        "endereco": "Rua José Suguinoshita, 126-210 - Vila Alay Jose Correa, Registro - SP",
        "mapa_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14523.834597521009!2d-47.85132678138166!3d-24.48688955225139!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94c5347669aa0f69%3A0xdcc204dc30b6b1c4!2sR.%20Jos%C3%A9%20Suguinoshita%2C%20126-210%20-%20Vila%20Alay%20Jose%20Correa%2C%20Registro%20-%20SP%2C%2011900-000!5e0!3m2!1spt-BR!2sbr!4v1762723668301!5m2!1spt-BR!2sbr"
    },
    {
        "id": 3,
        "nome": "Feira da Lua",
        "dia_semana_num": 4, # Sexta-feira
        "horario": "Sextas-feiras, 17:00–23:30",
        "endereco": "Rua Pio Onze, 143 - Centro, Registro - SP",
        "mapa_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14523.455893039976!2d-47.85171528138017!3d-24.49016955221674!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94c534778d603bb1%3A0x89427ebff517c4fe!2sR.%20Pio%20Onze%2C%20143%20-%20Centro%2C%20Registro%20-%20SP%2C%2011900-000!5e0!3m2!1spt-BR!2sbr!4v1762723737605!5m2!1spt-BR!2sbr"
    },
    {
        "id": 4,
        "nome": "Feira Livre de Quarta (Vila São Francisco)",
        "dia_semana_num": 2, # Quarta-feira
        "horario": "Quartas-feiras, 15:00–19:00",
        "endereco": "Rua da Saudade - Vila Sao Francisco, Registro - SP",
        "mapa_embed_url": "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3630.7186815147325!2d-47.8470352!3d-24.495202300000003!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94c5338687dd70f7%3A0xb4bf8dee6a2139f9!2sFeira%20Livre%20de%20Quarta!5e0!3m2!1spt-BR!2sbr!4v1762724000193!5m2!1spt-BR!2sbr"
    },
    {
        "id": 5,
        "nome": "Feira do Produtor (Vila Fátima)",
        "dia_semana_num": 3, # Quinta-feira
        "horario": "Quintas-feiras, 15:00–19:00",
        "endereco": "Rua São Paulo, 2-62 - Vila Fátima, Registro - SP",
        "mapa_embed_url" : "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d14522.8747687406!2d-47.854743921704774!3d-24.49520193042398!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x94c53384909b924f%3A0x75a1cb0f1bdf8ca7!2sFeira%20do%20Produtor!5e0!3m2!1spt-BR!2sbr!4v1762724073895!5m2!1spt-BR!2sbr"
    },
    {
        "id": 6,
        "nome": "Feira do Produtor (Centro)",
        "dia_semana_num": 6, # Domingo
        "horario": "Domingos, 06:00–11:00",
        "endereco": "Rua José Antônio de Campos - Centro, Registro - SP",
        "mapa_embed_url": "https://www.google.com/maps/embed?pb=!1m10!1m8!1m3!1d226.92029094490385!2d-47.8460755!3d-24.4949954!3m2!1i1024!2i768!4f13.1!5e0!3m2!1spt-BR!2sbr!4v1762728864733!5m2!1spt-BR!2sbr"
    }
]

# --- ATUALIZAÇÃO DA ESTRUTURA ---
# 'produtos_selecionados' mudou para 'produtos_snapshot'
# e agora guarda uma cópia (dicionário) dos produtos.
FEIRANTE_AGENDA = [
    {
        "id_agenda": 1,
        "usuario_id": 1,
        "feira_id": 1, 
        "data_escolhida": "2025-11-13",
        "status": "pendente",
        "produtos_snapshot": [
            {
                "id": 1,
                "nome": "Alface Crespa",
                "preco": "2,50",
                "unidade": "un",
                "categoria": "verduras",
                "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Lactuca_sativa_%27Ashbrook%27.jpg/640px-Lactuca_sativa_%27Ashbrook%27.jpg"
            },
            {
                "id": 2,
                "nome": "Beterraba",
                "preco": "3,00",
                "unidade": "kg",
                "categoria": "legumes",
                "imagem_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/21/Beets-Bundle.jpg/640px-Beets-Bundle.jpg"
            }
        ]
    }
]

# Função helper para encontrar uma feira pelo ID
def buscar_feira_por_id(feira_id: int):
    return next((f for f in FEIRAS_REGISTRO if f["id"] == feira_id), None)

# Mapeamento dos dias da semana (para as mensagens de erro)
DIAS_SEMANA_MAP = [
    "Segunda-feira", "Terça-feira", "Quarta-feira", 
    "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
]