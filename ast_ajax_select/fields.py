from django.forms import fields, widgets
from django.http import QueryDict
from django.db.models import Model
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from ajax_select.registry import registry
from .utils import make_plugin_options, get_uid

# TODO: Полностью пересмотреть работу. В вид


class AutoCompleteSelectWidget(widgets.Widget):
    channel = None
    multiple = False

    def __init__(self, *args, channel=None, multiple=False, **kwargs):
        super(AutoCompleteSelectWidget, self).__init__(*args, **kwargs)
        self.channel = channel
        self.multiple = multiple

    def render(self, name, value, attrs=None, renderer=None):

        if value is None:
            value = []

        final_attrs = self.build_attrs(self.attrs)
        final_attrs.update(attrs or {})
        final_attrs.pop('required', None)
        html_id = final_attrs.pop('id', name)
        deck_id = "%s_%s_on_deck" % (html_id, get_uid())

        lookup = registry.get(self.channel)

        if value:
            values = self.multiple and list(value) or [value]

            if all([isinstance(v, Model) for v in values]):
                objects = values
            else:
                objects = lookup.get_objects(values)

            initial = [
                [lookup.format_item_display(obj), obj.pk]
                for obj in objects
            ]
        else:
            initial = []

        context = {
            "name": name,
            'html_id': html_id,
            'deck_id': deck_id
        }
        # self.widget_plugin_options
        context.update(make_plugin_options(lookup, self.channel, name, {}, initial, deck_id, self.multiple))

        templates = ('ast_ajax_select/input_select_%s.html' % self.channel,
                     'ast_ajax_select/input_select.html')
        out = render_to_string(templates, context)
        return mark_safe(out)

    def value_from_datadict(self, data, files, name):
        if self.multiple:
            if isinstance(data, QueryDict):
                return data.getlist(name)
            else:
                return name in data and [data[name], ] or []
        else:
            if isinstance(data, QueryDict):
                return data.get(name)
            else:
                return name in data and data[name] or None


class AutoCompleteSelectMultipleField(fields.Field):
    widget = AutoCompleteSelectWidget
    channel = None

    def __init__(self, channel, *args, **kwargs):
        widget_kwargs = {
            'channel': channel,
            'multiple': True,
        }
        kwargs['widget'] = self.widget(**widget_kwargs)
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)
        self.channel = channel


class AutoCompleteSelectField(fields.Field):
    widget = AutoCompleteSelectWidget
    channel = None

    def __init__(self, channel, *args, empty_label="For compatibility with ModelChoiceField", **kwargs):
        widget_kwargs = {
            'channel': channel,
            'multiple': False,
        }
        kwargs['widget'] = self.widget(**widget_kwargs)
        super(AutoCompleteSelectField, self).__init__(*args, **kwargs)
        self.channel = channel
