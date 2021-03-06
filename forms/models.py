from django.db import models
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from modelcluster.fields import ParentalKey
from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.core.fields import RichTextField
from wagtail.contrib.forms.models import AbstractFormField
from wagtailcaptcha.models import WagtailCaptchaEmailForm

from forms.email import send_mail
from common.models import MetadataPageMixin
from common.edit_handlers import HelpPanel


class ReplyToValidatorForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super().clean()

        reply_to_fields = []
        reply_to_forms = []
        for form in self.formsets['form_fields'].forms:
            if form.is_valid():
                cleaned_form_data = form.clean()
                reply_to_field = cleaned_form_data.get('use_as_reply_to')

                if reply_to_field:
                    reply_to_fields.append(cleaned_form_data.get('label'))
                    reply_to_forms.append(form)

        if len(reply_to_fields) > 1:
            for form in reply_to_forms:
                form.add_error('use_as_reply_to', 'Only one field per form may have this option enabled.')
            raise ValidationError('Multiple fields with "Use as reply to" checked: {}'.format(', '.join(reply_to_fields)))

        return cleaned_data


class FormField(AbstractFormField):
    class Meta(AbstractFormField.Meta):
        constraints = [
            models.UniqueConstraint(
                fields=['page'],
                condition=models.Q(use_as_reply_to=True),
                name='only_one_reply_to_form_field',
            )
        ]

    page = ParentalKey('FormPage', related_name='form_fields')

    append_to_subject = models.BooleanField(
        default=False,
        help_text='Add the contents of this field to the subject of the email sent by this from.  All fields with this checked will be appended.',
    )
    use_as_reply_to = models.BooleanField(
        default=False,
        help_text='Use the contents of this field as the Reply-To header of the email sent by this from.  Only one field per form can have this checked.',
    )

    panels = AbstractFormField.panels + [
        FieldPanel('append_to_subject'),
        FieldPanel('use_as_reply_to'),
    ]


@method_decorator(cache_control(private=True), name='serve')
class FormPage(MetadataPageMixin, WagtailCaptchaEmailForm):
    intro = RichTextField(blank=True)
    thank_you_text = RichTextField(blank=True)
    button_text = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )

    content_panels = [
        HelpPanel(heading='Note', content='Forms can be embedded in an iframe by a third-party website. '
                  'Append <code>?embed=t</code> to any FormPage URL to request the embeddable version. '
                  'You can copy the code below and replace <code>[[URL TO FORM]]</code> with the full link to this form page.'
                  '<textarea style="font-size: 1em; color: black; font-family: monospace; border: 0; padding: 0.5em">'
                  '<iframe src="[[URL TO FORM]]?embed=t" width="100%" height="60vh"></iframe>'
                  '</textarea>'),
    ] + WagtailCaptchaEmailForm.content_panels + [
        FieldPanel('intro', classname="full"),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        FieldPanel('button_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
    ]
    base_form_class = ReplyToValidatorForm

    def get_context(self, request, *args, **kwargs):
        context = super(FormPage, self).get_context(request, *args, **kwargs)
        if request.GET.get('embed', None):
            context['template_name'] = 'base.chromeless.html'
        else:
            context['template_name'] = 'base.html'
        return context

    def serve(self, request, *args, **kwargs):
        response = super(FormPage, self).serve(request, *args, **kwargs)
        if 'embed' in request.GET:
            response.xframe_options_exempt = True
        return response

    def send_mail(self, form):
        fields = {x.clean_name: x for x in self.form_fields.all()}
        addresses = [x.strip() for x in self.to_address.split(',')]
        content = []
        reply_to = []
        subject = self.subject

        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))

            if fields.get(field.name):
                if fields.get(field.name).append_to_subject and value:
                    subject = '{0} - {1}'.format(subject, field.value())
                if fields.get(field.name).use_as_reply_to and value:
                    reply_to = [value]
        content = '\n'.join(content)
        send_mail(subject, content, addresses, self.from_address, reply_to=reply_to)
