# core/context_processors.py

def variaveis_base(request):
    return {
        'VARIAVEIS_BASE': {
            'template_name': 'Meu Site',
            'template_suffix': 'Administração',
            'template_description': 'Descrição do site',
            'template_keyword': 'palavras-chave, do, site',
            'product_page': 'https://www.meusite.com',
        }
    }
