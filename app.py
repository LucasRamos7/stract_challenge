from flask import Flask
import flask_excel as excel

from methods import get_ads_by_platform, get_ads_by_platform_summary, get_all_ads, get_all_ads_summary


app = Flask(__name__)


excel.init_excel(app)


@app.route('/')
def presentation() -> dict:
    return {
        'Nome': 'Lucas de Souza Oliveira Ramos',
        'E-mail': 'lucassouzaramos7@gmail.com',
        'LinkedIn': 'https://www.linkedin.com/in/lucas-ramos-959116203/'
    }


@app.route('/<string:platform>')
def get_account_ads(platform):
    data = get_ads_by_platform(platform)
    return excel.make_response_from_array(data, 'csv')


@app.route('/<string:platform>/resumo')
def get_account_ads_summary(platform):
    data = get_ads_by_platform_summary(platform)
    return excel.make_response_from_array(data, 'csv')


@app.route('/geral')
def get_ads():
    data = get_all_ads()
    return excel.make_response_from_array(data, 'csv')


@app.route('/geral/resumo')
def get_ads_summary():
    data = get_all_ads_summary()
    return excel.make_response_from_array(data, 'csv')
