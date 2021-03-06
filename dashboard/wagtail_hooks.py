from django.template.loader import render_to_string
from wagtail.core import hooks

from common.models.settings import SearchSettings


class ShortcutsPanel:
    # This is an ordering number that is the minimum multiple of 10 to place
    # this panel underneath the built-in Wagtail panels.
    order = 100

    def __init__(self, request):
        self.request = request

    def render(self):
        search_page = SearchSettings.for_site(self.request.site).search_page
        return render_to_string('dashboard/shortcuts_panel.html', dict(
            incident_page=search_page,
        ))


@hooks.register('construct_homepage_panels')
def add_shortcuts_panel(request, panels):
    return panels.append(ShortcutsPanel(request))
