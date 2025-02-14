import requests
import json
from typing import List


BASE_URL = 'https://sidebar.stract.to/api'

with open('secrets.json', 'r') as f:
    token = json.load(f)['TOKEN']
headers = {f'Authorization': f'Bearer {token}'}


def get_accounts_by_platform(platform: str) -> List[dict]:
    accounts = []
    res = requests.get(f'{BASE_URL}/accounts?platform={platform}', headers=headers)
    res = res.json()

    for account in res['accounts']:
        accounts.append(account)

    last_page = res['pagination']['total']
    if last_page > 1:
        for page in range(2, last_page + 1):
            res = requests.get(f'{BASE_URL}/accounts?platform={platform}&page={page}', headers=headers)
            res = res.json()

            for account in res['accounts']:
                accounts.append(account)

    return accounts


def get_fields_by_platform(platform: str) -> List[tuple]:
    fields = []

    res = requests.get(f'{BASE_URL}/fields?platform={platform}', headers=headers)
    res = res.json()

    for field in res['fields']:
        fields.append((field['text'], field['value']))

    last_page = res['pagination']['total']
    if last_page > 1:
        for page in range(2, last_page + 1):
            res = requests.get(f'{BASE_URL}/fields?platform={platform}&page={page}', headers=headers)
            res = res.json()

            for field in res['fields']:
                fields.append((field['text'], field['value']))

    return fields


def get_ads_by_platform(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    insights = []

    for account in accounts:

        req_fields = ','.join([field[1] for field in fields])
        res = requests.get(
            f'{BASE_URL}/insights'
            f'?platform={platform}&account={account['id']}&token={account['token']}&fields={req_fields}',
            headers=headers
        )
        res = res.json()

        for insight in res['insights']:
            insights.append({
                'Platform': platform,
                'Name': account['name']
            })
            for field in fields:
                insights[-1][field[0]] = insight[field[1]]

    return insights
