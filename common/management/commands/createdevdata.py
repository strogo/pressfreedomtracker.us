import json
import random
import requests
import time
import wagtail_factories

from django.contrib.auth.models import User
from django.core import management
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.db import transaction
from wagtail.core.models import Site
from wagtail.core.rich_text import RichText
import factory
from faker import Faker

from blog.models import BlogIndexPage, BlogPage
from blog.tests.factories import BlogIndexPageFactory, BlogPageFactory
from common.models import (
    SimplePage, SimplePageWithSidebar,
    FooterSettings, SearchSettings,
    GeneralIncidentFilter, IncidentFilterSettings
)
from common.tests.factories import (
    PersonPageFactory, CustomImageFactory, OrganizationIndexPageFactory
)
from forms.models import FormPage
from home.models import HomePage, HomePageFeature
from incident.models import IncidentIndexPage, IncidentPage
from incident.tests.factories import IncidentIndexPageFactory, IncidentLinkFactory, MultimediaIncidentUpdateFactory
from menus.models import Menu, MenuItem

LIPSUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Ut in erat orci. Pellentesque eget scelerisque felis, ut iaculis erat. Nullam eget quam felis. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Vestibulum eu dictum ligula. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Praesent et mi tellus. Suspendisse bibendum mi vel ex ornare imperdiet. Morbi tincidunt ut nisl sit amet fringilla. Proin nibh nibh, venenatis nec nulla eget, cursus finibus lectus. Aenean nec tellus eget sem faucibus ultrices.'


fake = Faker()


class Command(BaseCommand):
    help = 'Creates data appropriate for development'

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-download',
            action='store_false',
            dest='download_images',
            help='Download external images',
        )

    def fetch_image(self, width, height, collection):
        url = 'https://picsum.photos/{width}/{height}'.format(
            width=width, height=height,
        )
        response = requests.get(url)
        if response and response.content:
            CustomImageFactory(
                file__from_file=ContentFile(response.content),
                file_size=len(response.content),
                width=width,
                height=height,
                collection=collection,
            )
        else:
            return False
        time.sleep(0.2)
        return True

    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Creating development data')
        self.stdout.flush()

        # createcategories will handle creating homepage.
        management.call_command('createcategories')
        home_page = HomePage.objects.get(slug='home')

        if not Site.objects.filter(is_default_site=True):
            site = Site.objects.create(
                site_name='Press Freedom Incidents (Dev)',
                hostname='localhost',
                port='8000',
                root_page=home_page,
                is_default_site=True
            )
        else:
            site = Site.objects.get(
                is_default_site=True,
            )

        # IMAGES
        photo_collection = wagtail_factories.CollectionFactory(name='Photos')

        if options.get('download_images', True):
            self.stdout.write('Fetching images')
            self.stdout.flush()

            image_fail = False
            for i in range(5):
                if not self.fetch_image(800, 600, photo_collection):
                    image_fail = True
            for i in range(5):
                if not self.fetch_image(1280, 720, photo_collection):
                    image_fail = True
            for i in range(5):
                if not self.fetch_image(600, 800, photo_collection):
                    image_fail = True

            self.stdout.write('')
            if image_fail:
                self.stdout.write(self.style.NOTICE('NOTICE: Some images failed to save'))
            else:
                self.stdout.write(self.style.SUCCESS('OK'))
        else:
            faker = factory.faker.Faker._get_faker(locale='en-US')
            for i in range(20):
                CustomImageFactory.create(
                    file__width=800,
                    file__height=600,
                    file__color=faker.safe_color_name(),
                    collection=photo_collection,
                )
                CustomImageFactory.create(
                    file__width=1280,
                    file__height=720,
                    file__color=faker.safe_color_name(),
                    collection=photo_collection,
                )
                CustomImageFactory.create(
                    file__width=600,
                    file__height=800,
                    file__color=faker.safe_color_name(),
                    collection=photo_collection,
                )

        # ABOUT PAGE
        if not SimplePage.objects.filter(slug='about').exists():
            about_page = SimplePage(
                title='About',
                slug='about',
                body=json.dumps([
                    dict(
                        type='text',
                        value=dict(
                            text=LIPSUM,
                            background_color='white',
                            text_align='left',
                            font_size='large',
                            font_family='sans-serif',
                        ),
                    ),
                ])
            )
            home_page.add_child(instance=about_page)
            home_page.about_page = about_page
        else:
            about_page = SimplePage.objects.get(slug='about')

        # RESOURCES PAGE
        if not Menu.objects.filter(slug='resources').exists():
            resources_menu = Menu.objects.create(name='Resources Sidebar', slug='resources')
            MenuItem.objects.bulk_create([
                MenuItem(
                    text='About',
                    link_page=about_page,
                    menu=resources_menu,
                    sort_order=1
                ),
                MenuItem(
                    text='A menu item',
                    link_url='#',
                    menu=resources_menu,
                    sort_order=2
                ),
            ])
            resources_page = SimplePageWithSidebar(
                title='Resources',
                slug='resources',
                sidebar_menu=resources_menu,
                body=json.dumps([
                    dict(
                        type='text',
                        value=dict(
                            text=LIPSUM,
                            background_color='white',
                            text_align='left',
                            font_size='large',
                            font_family='sans-serif',
                        ),
                    ),
                ])
            )

            home_page.add_child(instance=resources_page)

        # SUBMIT INCIDENT FORM
        if not FormPage.objects.filter(slug='submit-incident'):
            incident_form = FormPage(title='Submit an incident', slug='submit-incident')
            home_page.add_child(instance=incident_form)
        else:
            FormPage.objects.get(slug='submit-incident')

        # CREATE MENUS
        # delete any the existing main menu
        if not Menu.objects.filter(slug='main').exists():
            main = Menu.objects.create(name='Main Menu', slug='main')
            MenuItem.objects.bulk_create([
                MenuItem(
                    text='About',
                    link_page=about_page,
                    menu=main,
                    sort_order=1
                ),
                MenuItem(
                    text='Resources',
                    link_page=resources_page,
                    menu=main,
                    sort_order=2
                ),
                MenuItem(
                    text='Contact',
                    link_url='#',
                    menu=main,
                    sort_order=3
                ),
                MenuItem(
                    text='Submit an Incident',
                    link_page=incident_form,
                    menu=main,
                    sort_order=99,
                    html_classes='header__nav-link--highlighted'
                ),
            ])

        footer_menu, created = Menu.objects.get_or_create(
            name='Footer Menu', slug='footer')
        if created:
            MenuItem.objects.bulk_create([
                MenuItem(
                    text='About',
                    link_page=about_page,
                    menu=footer_menu,
                    sort_order=1,
                ),
                MenuItem(
                    text='Our Partners',
                    link_url='#',
                    menu=footer_menu,
                    sort_order=2,
                ),
                MenuItem(
                    text='Privacy Policy',
                    link_url='#',
                    menu=footer_menu,
                    sort_order=3,
                ),
                MenuItem(
                    text='Contact',
                    link_url='#',
                    menu=footer_menu,
                    sort_order=4,
                ),
            ])

        # FOOTER
        footer_settings = FooterSettings.for_site(site)
        footer_settings.body = RichText('U.S. Press Freedom Tracker is a project of <a href="https://freedom.press">Freedom of the Press Foundation</a> and the <a href="https://www.cpj.org/">Committee to Protect Journalists</a>.')
        if footer_menu:
            footer_settings.menu = footer_menu
        footer_settings.save()

        # BLOG RELATED PAGES
        if not BlogIndexPage.objects.filter(slug='fpf-blog').exists():
            blog_index_page = BlogIndexPageFactory(parent=home_page, main_menu=True, with_image=True)
            org_index_page = OrganizationIndexPageFactory(parent=home_page)
            home_page.blog_index_page = blog_index_page

            author1, author2, author3 = PersonPageFactory.create_batch(3, parent=home_page)

            BlogPageFactory.create_batch(
                10,
                parent=blog_index_page,
                organization__parent=org_index_page,
                author=author1,
                with_image=True,
            )
            BlogPageFactory.create_batch(
                10,
                parent=blog_index_page,
                organization__parent=org_index_page,
                author=author2,
                with_image=True,
            )
            BlogPageFactory.create_batch(
                10,
                parent=blog_index_page,
                organization__parent=org_index_page,
                author=author3,
                with_image=True,
            )

            for i, page in zip((2, 4, 6), random.sample(list(BlogPage.objects.all()), 3)):
                HomePageFeature.objects.create(
                    sort_order=i,
                    home_page=home_page,
                    page=page,
                )
        else:
            blog_index_page = BlogIndexPage.objects.get(slug='fpf-blog')

        # INCIDENT RELATED PAGES
        search_settings = SearchSettings.for_site(site)
        incident_filter_settings = IncidentFilterSettings.for_site(site)
        GeneralIncidentFilter.objects.create(
            incident_filter_settings=incident_filter_settings,
            incident_filter='date',
        )

        if not IncidentIndexPage.objects.filter(slug='all-incidents'):
            incident_index_page = IncidentIndexPageFactory(
                parent=home_page,
                main_menu=True,
                title='All Incidents',
            )
            management.call_command('createincidents')
        else:
            incident_index_page = IncidentIndexPage.objects.get(slug='all-incidents')

        search_settings.search_page = incident_index_page
        search_settings.save()

        for i, incident in zip((1, 3, 5), random.sample(list(IncidentPage.objects.all()), 3)):
            HomePageFeature.objects.create(
                sort_order=i,
                home_page=home_page,
                page=incident,
            )
            MultimediaIncidentUpdateFactory(page=incident)
            IncidentLinkFactory.create_batch(3, page=incident)
        home_page.save()

        # Create superuser
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                'test',
                'test@pressfreedom',
                'test',
            )
            self.stdout.write(
                'Superuser created:\n'
                '\tname: test\n'
                '\temail: test@pressfreedom\n'
                '\tpassword: test'
            )

        self.stdout.write('Done.')
