import requests
from typing import List
from collections import namedtuple
from stract_api import Field, get_accounts_by_platform, get_fields_by_platform, get_platforms, get_account_insights


def get_ads_by_platform(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]
    request_fields = ','.join([field.field_tag for field in fields])
    account_insights = []

    for account in accounts:
        insights = get_account_insights(platform, account['id'], account['token'], request_fields)

        for insight in insights:
            account_insights.append({
                'Platform': platform_name,
                'Name': account['name']
            })
            for field in fields:
                account_insights[-1][field.field_name] = insight[field.field_tag]

            if platform == 'ga4':
                account_insights[-1]['Costs Per Click'] = round(account_insights[-1]['Spend'] / account_insights[-1]['Clicks'], 3)

    return account_insights


def get_ads_by_platform_summary(platform: str) -> List[dict]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]
    request_fields = ','.join([field.field_tag for field in fields])
    account_summaries = []

    for account in accounts:
        insights = get_account_insights(platform, account['id'], account['token'], request_fields)

        if platform == 'ga4':
            fields.append(Field('Cost Per Click', 'cpc'))
            for insight in insights:
                insight['cpc'] = round(insight['cost'] / insight['clicks'], 3)
        fields_sum = {}
        for field in fields:
            try:
                float(insights[0][field.field_tag])
                fields_sum[field.field_name] = sum([ad[field.field_tag] for ad in insights])
            except ValueError:
                fields_sum[field.field_name] = ''

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
