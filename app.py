from flask import Flask

from methods import get_ads_by_platform, get_ads_by_platform_summary


app = Flask(__name__)


@app.route('/')
def presentation() -> str:
    return ('Nome: Lucas de Souza Oliveira Ramos'
            'E-mail: lucassouzaramos7@gmail.com'
            'LinkedIn: https://www.linkedin.com/in/lucas-ramos-959116203/')


@app.route('/<platform>')
def get_ads(platform):
    return get_ads_by_platform(platform)


@app.route('/<platform>/resumo')
def get_ads_summary(platform):
    return get_ads_by_platform_summary(platform)


'''
app.route(/{{plataforma/resumo}})
Tabela similar, somando os campos numéricos e retornando vazios os campos de texto, exceto o nome da conta

app.route(/geral)
Retorna todos os anúncios de todas as plataformas, com colunas para identificar por nome a plataforma

app.route(/geral/resumo)
Similar a plataforma/resumo
'''
