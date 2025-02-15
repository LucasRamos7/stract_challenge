import json
import requests
from collections import namedtuple
from typing import List

BASE_URL = 'https://sidebar.stract.to/api'

with open('secrets.json', 'r') as f:
    token = json.load(f)['TOKEN']
headers = {f'Authorization': f'Bearer {token}'}


Field = namedtuple('Field', ['field_name', 'field_tag'])


def get_accounts_by_platform(platform: str) -> List[dict]:
    accounts = []
    res = requests.get(f'{BASE_URL}/accounts?platform={platform}', headers=headers)
    res = res.json()

    for account in res['accounts']:
        accounts.append(account)

    if 'pagination' in res:
        last_page = res['pagination']['total']
        if last_page > 1:
            for page in range(2, last_page + 1):
                res = requests.get(f'{BASE_URL}/accounts?platform={platform}&page={page}', headers=headers)
                res = res.json()

                for account in res['accounts']:
                    accounts.append(account)

    return accounts


def get_fields_by_platform(platform: str) -> List[namedtuple]:
    fields = []

    res = requests.get(f'{BASE_URL}/fields?platform={platform}', headers=headers)
    res = res.json()

    for field in res['fields']:
        fields.append(Field(field['text'], field['value']))
    if 'pagination' in res:
        last_page = res['pagination']['total']
        if last_page > 1:
            for page in range(2, last_page + 1):
                res = requests.get(f'{BASE_URL}/fields?platform={platform}&page={page}', headers=headers)
                res = res.json()

                for field in res['fields']:
                    fields.append(Field(field['text'], field['value']))

    return fields


def get_platforms():
    res = requests.get(f'{BASE_URL}/platforms', headers=headers)
    res = res.json()
    platforms = {platform['value']: platform['text'] for platform in res['platforms']}

    return platforms


def get_account_insights(platform: str, account: int, token: str, fields='str') -> List[dict]:
    res = requests.get(
        f'{BASE_URL}/insights'
        f'?platform={platform}&account={account}&token={token}&fields={fields}',
        headers=headers
    )
    res = res.json()

    return res['insights']