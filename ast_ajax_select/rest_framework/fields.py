import json
from django.template.defaultfilters import force_escape
from django.core.serializers.json import DjangoJSONEncoder
try:
    from django.urls import reverse
except ImportError:
    # < django 1.10
    from django.core.urlresolvers import reverse
from rest_framework import serializers
from ajax_select.registry import registry
from ..utils import get_uid


class AjaxSelectFieldMixin(object):
    multiple = False
    data_url = None
    key_name = "key"

    def get_initial_data(self, field_name, parent):
        initial = None
        if hasattr(parent, "initial_data"):
            initial = parent.initial_data.get(field_name)
        elif hasattr(parent, "instance") and parent.instance:
            initial = getattr(parent.instance, field_name)

        return [initial, initial] if initial else None

    def init(self, field_name, parent):
        html_id = "id_%s" % field_name  # id для поля ввода
        deck_id = "%s_%s_on_deck" % (html_id, get_uid())  # id контейнера для результатов

        initial = self.get_initial_data(field_name, parent)

        po = {
            'deck_id': deck_id,
            "field_name": field_name,
            "key_name": self.key_name,
            "multiple": self.multiple,
            "initial": initial,
            "source": self.data_url,
        }

        style = {
            'base_template': 'input_select.html',
            'html_id': html_id,
            'deck_id': deck_id,
            'plugin_options': force_escape(json.dumps(po, cls=DjangoJSONEncoder)),
        }

        self.style.update(style)


class AjaxSelectM2MField(serializers.ManyRelatedField, AjaxSelectFieldMixin):
    data_url = None
    multiple = True
    queryset = None
    channel_name = None
    key_name = "pk"

    def __init__(self, queryset, channel_name, *args, **kwargs):
        self.queryset = queryset
        self.channel_name = channel_name
        child_relation = serializers.PrimaryKeyRelatedField(queryset=self.queryset)
        super(AjaxSelectM2MField, self).__init__(child_relation=child_relation, *args, **kwargs)

    def get_initial_data(self, field_name, parent):
        lookup = registry.get(self.channel_name)
        initial = None

        qs = None
        if hasattr(parent, "initial_data"):
            pks = parent.initial_data.getlist(field_name)
            if pks:
                qs = self.queryset.filter(pk__in=pks)
        elif hasattr(parent, "instance") and parent.instance:
            qs = getattr(parent.instance, field_name).all()
        initial = qs and [[lookup.format_item_display(obj), obj.pk] for obj in qs] or []

        return initial

    def bind(self, field_name, parent):
        self.data_url = reverse('ajax_lookup', kwargs={'channel': self.channel_name})
        self.init(field_name, parent)
        super(AjaxSelectM2MField, self).bind(field_name, parent)


# PrimaryKeyRelatedField(queryset=CompanyPublication.objects.all())
class AjaxSelectFKField(serializers.PrimaryKeyRelatedField, AjaxSelectFieldMixin):
    data_url = None
    multiple = False
    channel_name = None
    key_name = "pk"

    def __init__(self, channel_name, *args, **kwargs):
        # many -- для совместимости, когда serializer генерирует автоматом параметры
        self.channel_name = channel_name
        super(AjaxSelectFKField, self).__init__(*args, **kwargs)

    def get_initial_data(self, field_name, parent):
        lookup = registry.get(self.channel_name)
        initial = None

        obj = None
        if hasattr(parent, "initial_data"):
            pk = parent.initial_data.get(field_name)
            if pk:
                try:
                    obj = self.related_model.objects.get(pk=pk)
                except self.related_model.DoesNotExist:
                    pass
        elif hasattr(parent, "instance") and parent.instance:
            obj = getattr(parent.instance, field_name)
        initial = obj and [[lookup.format_item_display(obj), obj.pk]] or None

        return initial

    def bind(self, field_name, parent):
        self.data_url = reverse('ajax_lookup', kwargs={'channel': self.channel_name})
        self.init(field_name, parent)
        super(AjaxSelectFKField, self).bind(field_name, parent)
