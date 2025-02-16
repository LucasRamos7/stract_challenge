# Stract Challenge


# Descrição do Projeto

A meta do projeto é consumir a API da Stract e retornar os dados organizados em formato .csv

# Requisitos

## **Python**

A versão utilizada do Python foi a 3.12, disponível para [download](https://www.python.org/downloads/).

## **Dependências / Bibliotecas**

As dependências do projeto estão listadas no arquivo requirements.txt 

É recomendado o uso de um ambiente virtual para a instalação das dependências, que pode ser criado com o comando **`python -m venv ./venv`**.

Após criado, o ambiente virtual deve ser ativado, com o comando **`venv\Scripts\activate`** (Windows) ou **`source venv/bin/activate`** (Linux).

Com o ambiente virtual criado e ativado, o comando **`pip install -r requirements.txt`** instalará as dependências do projeto.


# Executando o projeto
## 1. Clonar o repositório
    
No diretório definido para armazenar os arquivos do projeto, executar o comando `git clone <link do repositório>`.

## 2. Arquivo secrets.json

O arquivo secrets.json contém o token de acesso da API da Stract, e deve se localizar na raiz do projeto. Sua formatação é a seguinte:

`{

  "TOKEN": "<API TOKEN>"

}`

## 3. Flask

O projeto foi desenvolvido a partir do framework Flask. Para executá-lo, basta executar o comando **`flask run`** no diretório raiz do projeto.


# Endpoints
Todos os endpoints retornam uma tabela em formato .csv

### Recuperar todos os anúncios de uma plataforma

```
GET localhost:5000/<platform>
```

Valores aceitos para platform: **meta_ads** (Meta Ads), **ga4** (Google Analytics), **tiktok_insights** (TikTok).

### Recuperar todos os anúncios de uma plataforma, resumido por conta

```
GET localhost:5000/<platform>/resumo
```

Valores aceitos para platform: **meta_ads** (Meta Ads), **ga4** (Google Analytics), **tiktok_insights** (TikTok).

### Recuperar todos os anúncios

```
GET localhost:5000/geral
```

### Recuperar todos os anúncios, resumido por plataforma

```
GET localhost:5000/geral/resumo
```