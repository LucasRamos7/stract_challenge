from typing import List
from stract_api import Field, get_accounts_by_platform, get_fields_by_platform, get_platforms, get_account_insights


def get_ads_by_platform(platform: str) -> List[list]:
    accounts = get_accounts_by_platform(platform)
    fields = get_fields_by_platform(platform)
    platform_name = get_platforms()[platform]

    # Joining field names to add to request URL
    request_fields = ','.join([field.tag for field in fields])

    account_insights = []
    headers = ['Platform', 'Name'] + [field.name for field in fields]

    if platform == 'ga4':
        headers.append('Cost Per Click')

    for account in accounts:
        insights = get_account_insights(platform, account['id'], account['token'], request_fields)

        for insight in insights:
            # Each line starts with platform and account names
            account_insights.append([platform_name, account['name']])

            for field in fields:
                # Appending the value of each insight to the line
                account_insights[-1].append(insight[field.tag])
            if platform == 'ga4':
                # Calculating Cost Per Click for the Google Analytics platform
                account_insights[-1].append(round(
                    account_insights[-1][headers.index('Spend')] / account_insights[-1][headers.index('Clicks')], 3
                ))

    # Adding csv headers at the start
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
                # Testing whether it's a numeric field
                float(insights[0][field.tag])
                fields_sum[field.name] = sum([ad[field.tag] for ad in insights])
            except ValueError:
                # If it's a text field, return an empty string
                fields_sum[field.name] = ''

            account_summaries[-1].append(fields_sum[field.name])

    account_summaries.insert(0, headers)

    return account_summaries


def get_all_ads() -> List[dict]:
    platforms = get_platforms()
    all_ads = []

    for platform in platforms.keys():
        all_ads += get_ads_by_platform(platform)

    return all_ads


def get_all_ads_summary() -> List[list]:
    platforms = get_platforms()
    platform_summaries = []

    # Getting fields from meta_ads because it has all the fields from the two other platforms, plus a few extra
    headers = ['Platform'] + [field.name for field in get_fields_by_platform('meta_ads')]

    for platform in platforms.keys():
        # Platform name at the start of the line
        platform_summaries.append([platforms[platform]])
        ads = get_ads_by_platform_summary(platform)
        fields_sum = {}

        for field in headers[1:]:
            try:
                float(ads[1][ads[0].index(field)])
                fields_sum[field] = sum([ad[ads[0].index(field)] for ad in ads[1:]])

                # Rounding Cost Per Click to 3 decimal places
                if field == 'Cost Per Click':
                    fields_sum[field] = round(fields_sum[field], 3)
            except (ValueError, KeyError):
                fields_sum[field] = ''

            platform_summaries[-1].append(fields_sum[field])

    platform_summaries.insert(0, headers)

    return platform_summaries
