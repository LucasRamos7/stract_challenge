from flask import Flask

from methods import get_ads_by_platform, get_ads_by_platform_summary, get_all_ads, get_all_ads_summary


app = Flask(__name__)


@app.route('/')
def presentation() -> dict:
    return {
        'Nome': 'Lucas de Souza Oliveira Ramos',
        'E-mail': 'lucassouzaramos7@gmail.com',
        'LinkedIn': 'https://www.linkedin.com/in/lucas-ramos-959116203/'
    }


@app.route('/<string:platform>')
def get_account_ads(platform):
    return get_ads_by_platform(platform)


@app.route('/<string:platform>/resumo')
def get_account_ads_summary(platform):
    return get_ads_by_platform_summary(platform)


@app.route('/geral')
def get_ads():
    return get_all_ads()


@app.route('/geral/resumo')
def get_ads_summary():
    return get_all_ads_summary()
