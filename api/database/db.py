import json

from api.models import AdSet
from api.serializers import AdSetSerializer


def target_audience_mistypo_func(value):
    value['target_audience'] = value.pop('target_audiance')
    return value


def unify_database(adsets):
    for adset in adsets:
        platforms = adset['platforms']
        # target_audiance => target_audience
        dict(map(lambda p: (p[0], target_audience_mistypo_func(p[1])), adset['platforms'].items()))

        # KeyWords => keywords
        if 'google' in platforms:
            target_audience = platforms['google']['target_audience']
            target_audience['keywords'] = target_audience.pop('KeyWords')


def init_database():
    # remove old ones
    AdSet.objects.all().delete()

    str = open('api/database/data/data.json').read()
    adsets = json.loads(str)

    unify_database(adsets)

    ad_set = AdSetSerializer(data=adsets, many=True)
    ad_set.is_valid(raise_exception=True)

    ad_set.save()
