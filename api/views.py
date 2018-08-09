# Create your views here.

from bson import json_util
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import AdSet


@api_view(['GET'])
def get_adsets(request):
    query = AdSet.objects.mongo_find({}, {'_id': False})

    # TODO Only for testing purposes!
    str = json_util.dumps(query)
    campaigns = json_util.loads(str)
    return Response(campaigns)

@api_view(['GET'])
def get_adset(request, id):
    campaign = AdSet.objects.mongo_find_one({'id': id}, {'_id': False})
    if campaign is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # TODO Only for testing purposes!
    str = json_util.dumps(campaign)
    return Response(json_util.loads(str))
