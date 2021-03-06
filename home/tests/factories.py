import factory
import wagtail_factories
from wagtail.core.rich_text import RichText

from home.models import HomePage, StatBox
from common.choices import CATEGORY_COLOR_CHOICES
from common.tests.utils import StreamfieldProvider


factory.Faker.add_provider(StreamfieldProvider)


class HomePageFactory(wagtail_factories.PageFactory):
    class Meta:
        model = HomePage
        django_get_or_create = ('slug',)
        exclude = ('about_text')

    about_text = factory.Faker('paragraph', nb_sentences=10)

    title = 'Home'
    about = factory.LazyAttribute(lambda o: RichText(o.about_text))
    content = factory.Faker(
        'streamfield',
        fields=['heading2', 'rich_text_paragraph', 'raw_html', 'tweet', 'tabs']
    )


class StatBoxFactory(factory.DjangoModelFactory):
    class Meta:
        model = StatBox

    class Params:
        # By default, no category, but you may supply one to
        # auto-populate other fields below.
        category = None

    sort_order = factory.Sequence(lambda n: n)
    value = factory.LazyAttribute(
        lambda o: '{{% num_incidents categories={} %}}'.format(o.category.pk) if o.category else '{% num_incidents %}'
    )
    label = factory.LazyAttribute(
        lambda o: 'Total {}'.format(o.category.plural_name) if o.category else '{% num_incidents %}'
    )

    color = factory.Iterator(CATEGORY_COLOR_CHOICES, getter=lambda c: c[0])
    internal_link = factory.LazyAttribute(
        lambda o: o.category if o.category else None
    )
    querystring = ''
    external_link = factory.Faker('url', schemes=['https'])
