import requests
from typing import List
from collections import namedtuple
from stract_api import Field, get_accounts_by_platform, get_fields_by_platform, get_platforms, get_account_insights


def get_ads_by_platform(platform: str) -> List[list]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]
    request_fields = ','.join([field.tag for field in fields])
    account_insights = []

    headers = ['Platform', 'Name'] + [field.name for field in fields]
    if platform == 'ga4':
        headers.append('Cost Per Click')

    for account in accounts:
        insights = get_account_insights(platform, account['id'], account['token'], request_fields)

        for insight in insights:
            account_insights.append([platform_name, account['name']])
            for field in fields:
                account_insights[-1].append(insight[field.tag])
            if platform == 'ga4':
                account_insights[-1].append(
                    round(account_insights[-1][headers.index('Spend')] /
                          account_insights[-1][headers.index('Clicks')], 3)
                )

    account_insights.insert(0, headers)
    return account_insights


def get_ads_by_platform_summary(platform: str) -> List[list]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]
    request_fields = ','.join([field.tag for field in fields])
    account_summaries = []

    headers = ['Platform', 'Name'] + [field.name for field in fields]
    if platform == 'ga4':
        headers.append('Cost Per Click')

    for account in accounts:
        account_summaries.append([platform_name, account['name']])
        insights = get_account_insights(platform, account['id'], account['token'], request_fields)

        if platform == 'ga4':
            fields.append(Field('Cost Per Click', 'cpc'))
            for insight in insights:
                insight['cpc'] = round(insight['cost'] / insight['clicks'], 3)
        fields_sum = {}
        for field in fields:
            try:
                float(insights[0][field.tag])
                fields_sum[field.name] = sum([ad[field.tag] for ad in insights])
            except ValueError:
                fields_sum[field.name] = ''

            account_summaries[-1].append(fields_sum[field.name])

    account_summaries.insert(0, headers)
        # fields_sum['id'] = ''
        # fields_sum['Name'] = account['name']
        # fields_sum['Platform'] = platform_name

        # account_summaries.append(fields_sum)



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
