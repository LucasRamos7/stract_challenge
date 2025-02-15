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

    if 'pagination' in res:
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
    if 'pagination' in res:
        last_page = res['pagination']['total']
        if last_page > 1:
            for page in range(2, last_page + 1):
                res = requests.get(f'{BASE_URL}/fields?platform={platform}&page={page}', headers=headers)
                res = res.json()

                for field in res['fields']:
                    fields.append((field['text'], field['value']))

    return fields


def get_platforms():
    res = requests.get(f'{BASE_URL}/platforms', headers=headers)
    res = res.json()
    platforms = {platform['value']: platform['text'] for platform in res['platforms']}

    return platforms


def get_ads_by_platform(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]
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

            if platform == 'ga4':
                insights[-1]['Costs Per Click'] = round(insights[-1]['Spend'] / insights[-1]['Clicks'], 3)

    return insights


def get_ads_by_platform_summary(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]
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
        if platform == 'ga4':
            fields.append(('Cost Per Click', 'cpc'))
            for insight in insights:
                insight['cpc'] = round(insight['cost'] / insight['clicks'], 3)
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


def get_all_ads() -> List[dict]:
    platforms = get_platforms()
    all_ads = []
    for platform in platforms.keys():
        all_ads += get_ads_by_platform(platform)

    return all_ads


def get_all_ads_summary() -> List[dict]:
    platforms = get_platforms()
    all_ads = []
    for platform in platforms.keys():
        ads = get_ads_by_platform_summary(platform)
        fields_sum = {}
        for field in ads[0].keys():
            try:
                float(ads[0][field])
                fields_sum[field] = sum([ad[field] for ad in ads])
            except ValueError:
                fields_sum[field] = ''

        fields_sum['Platform'] = platforms[platform]
        fields_sum['id'] = ''
        fields_sum['Cost Per Click'] = round(fields_sum['Cost Per Click'], 3)

        all_ads.append(fields_sum)

    return all_ads
