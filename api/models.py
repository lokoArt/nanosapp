from djongo import models


class FBInstaCreatives(models.Model):
    header = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    url = models.URLField()
    image = models.CharField(max_length=128)

    class Meta:
        abstract = True


class Insights(models.Model):
    impressions = models.IntegerField()
    clicks = models.IntegerField()
    website_visits = models.IntegerField()
    nanos_score = models.FloatField()
    cost_per_click = models.FloatField()
    click_through_rate = models.FloatField()
    advanced_kpi_1 = models.FloatField()
    advanced_kpi_2 = models.FloatField()

    class Meta:
        abstract = True


class FBInstaTargetAudience(models.Model):
    languages = models.ListField()
    genders = models.ListField()
    age_range = models.ListField()
    locations = models.ListField()
    interests = models.ListField()

    def __init__(self, languages=[], genders=[], age_range=[], locations=[], interests=[]):
        super().__init__()

        self.languages = languages
        self.genders = genders
        self.age_range = age_range
        self.locations = locations
        self.interests = interests

    class Meta:
        abstract = True


class FBInstaAdSet(models.Model):
    status = models.CharField(max_length=32)
    total_budget = models.IntegerField()
    remaining_budget = models.IntegerField()
    start_date = models.IntegerField()
    end_date = models.IntegerField()

    target_audience = models.EmbeddedModelField(
        model_container=FBInstaTargetAudience
    )

    creatives = models.EmbeddedModelField(
        model_container=FBInstaCreatives
    )

    insights = models.EmbeddedModelField(
        model_container=Insights
    )

    class Meta:
        abstract = True


class GoogleCreatives(models.Model):
    header_1 = models.CharField(max_length=128)
    header_2 = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    url = models.URLField()
    image = models.CharField(max_length=128)

    class Meta:
        abstract = True


class GoogleTargetAudience(models.Model):
    languages = models.ListField()
    genders = models.ListField()
    age_range = models.ListField()
    locations = models.ListField()
    keywords = models.ListField()

    # not the best solution... Need to rewrite EmbeddedModelField or model?
    def __init__(self, languages=[], genders=[], age_range=[], locations=[], keywords=[]):
        super().__init__()

        self.languages = languages
        self.genders = genders
        self.age_range = age_range
        self.locations = locations
        self.keywords = keywords

    class Meta:
        abstract = True


class GoogleAdSet(models.Model):
    status = models.CharField(max_length=32)
    total_budget = models.IntegerField()
    remaining_budget = models.IntegerField()
    start_date = models.IntegerField()
    end_date = models.IntegerField()

    target_audience = models.EmbeddedModelField(
        model_container=GoogleTargetAudience
    )

    creatives = models.EmbeddedModelField(
        model_container=GoogleCreatives
    )

    insights = models.EmbeddedModelField(
        model_container=Insights
    )

    class Meta:
        abstract = True


class Platforms(models.Model):
    facebook = models.EmbeddedModelField(
        model_container=FBInstaAdSet
    )

    instagram = models.EmbeddedModelField(
        model_container=FBInstaAdSet
    )

    google = models.EmbeddedModelField(
        model_container=GoogleAdSet
    )

    def __init__(self, facebook={}, instagram={}, google={}):
        super().__init__()

        self.instagram = instagram
        self.facebook = facebook
        self.google = google

    class Meta:
        abstract = True


class AdSet(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    goal = models.CharField(max_length=128)
    total_budget = models.IntegerField()
    status = models.CharField(max_length=32)
    platforms = models.EmbeddedModelField(
        model_container=Platforms
    )
    objects = models.DjongoManager()
