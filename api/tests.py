import json

from django.test import TestCase, Client

# Create your tests here.
from django.utils import timezone

from api.models import AdSet, FBInstaAdSet, FBInstaTargetAudience, Platforms, FBInstaCreatives, Insights
from api.serializers import AdSetSerializer


class ApiTest(TestCase):
    def test_create_adset_programmatically(self):
        api_client = Client()

        facebook = FBInstaAdSet(status='Delivering',
                                total_budget=40,
                                remaining_budget=12,
                                start_date=timezone.now().timestamp(),
                                end_date=timezone.now().timestamp(),
                                target_audience=FBInstaTargetAudience(
                                    languages=['RU', 'EN'],
                                    genders=['M', 'F'],
                                    age_range=[20, 66],
                                    locations=[
                                        "France",
                                        "Germany",
                                        "Switzerland"],
                                    interests=[
                                        "Docker",
                                        "Kubernates",
                                        "DevOps",
                                        "AWS",
                                        "Google Cloud Platform",
                                        "Ubuntu"]
                                ),
                                creatives=FBInstaCreatives(
                                    header='DevOps Made Easy, We Take care of the heavy lifting for you',
                                    description='DOP SuperHero is where all DevOps is going to happen in '
                                                'the future, join the revolution today!',
                                    url='https://example.io',
                                    image='img1.jpg'),
                                insights=Insights(
                                    impressions=4503,
                                    clicks=328,
                                    nanos_score=5.7,
                                    cost_per_click=0.88,
                                    click_through_rate=0.09,
                                    advanced_kpi_1=44.5,
                                    advanced_kpi_2=0.0023))

        AdSet.objects.create(id=777,
                             name='Test Ad 1',
                             goal='Increase Reach',
                             total_budget=120,
                             status='Delivering',
                             platforms=Platforms(facebook=facebook))

        response = api_client.get('/campaigns/777/')
        self.assertEqual(response.data['id'], 777)

    def test_adset_serialization(self):
        api_client = Client()

        str = open('api/test-resources/test-ad-set.json').read()
        adset_data = json.loads(str)

        ad_set = AdSetSerializer(data=adset_data)
        ad_set.is_valid(raise_exception=True)
        ad_set.save()

        response = api_client.get('/campaigns/')
        self.assertEqual(len(response.data), 4)

        response = api_client.get('/campaigns/{}/'.format(adset_data['id']))
        self.assertEqual(response.data['id'], adset_data['id'])
