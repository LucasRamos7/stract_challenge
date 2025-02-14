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


def get_platform_name(platform: str) -> str:
    res = requests.get(f'{BASE_URL}/platforms', headers=headers)
    res = res.json()
    platforms = {platform['value']: platform['text'] for platform in res['platforms']}

    return platforms[platform]


def get_ads_by_platform(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platform_name(platform)
    request_fields = ','.join([field[1] for field in fields])
    insights = []

    for account in accounts:
        res = requests.get(
            f'{BASE_URL}/insights'
            f'?platform={platform}&account={account['id']}&token={account['token']}&fields={request_fields}',
            headers=headers
        )
        res = res.json()

        for insight in res['insights']:
            insights.append({
                'Platform': platform_name,
                'Name': account['name']
            })
            for field in fields:
                insights[-1][field[0]] = insight[field[1]]

    return insights


def get_ads_by_platform_summary(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platform_name(platform)
    request_fields = ','.join([field[1] for field in fields])
    account_summaries = []

    for account in accounts:
        res = requests.get(
            f'{BASE_URL}/insights'
            f'?platform={platform}&account={account['id']}&token={account['token']}&fields={request_fields}',
            headers=headers
        )
        res = res.json()

        insights = res['insights']
        fields_sum = {}
        for field in fields:
            try:
                float(insights[0][field[1]])
                fields_sum[field[0]] = sum([ad[field[1]] for ad in insights])
            except ValueError:
                fields_sum[field[0]] = ''

        fields_sum['id'] = ''
        fields_sum['Name'] = account['name']
        fields_sum['Platform'] = platform_name

        account_summaries.append(fields_sum)

    return account_summaries
