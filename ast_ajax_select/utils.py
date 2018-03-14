import json
from django.core.serializers.json import DjangoJSONEncoder
try:
    from django.urls import reverse
except ImportError:
    # < django 1.10
    from django.core.urlresolvers import reverse
from django.template.defaultfilters import force_escape


def make_plugin_options(lookup, channel_name, field_name, widget_plugin_options, initial, dock_id, multiple):
    """ Make a JSON dumped dict of all options for the jQuery ui plugin."""
    po = {
        'field_name': field_name,
        'deck_id': dock_id,
        'multiple': multiple,
    }

    if initial:
        po['initial'] = initial
    po.update(getattr(lookup, 'plugin_options', {}))
    po.update(widget_plugin_options)
    if not po.get('source'):
        po['source'] = reverse('ajax_lookup', kwargs={'channel': channel_name})

    # allow html unless explicitly set
    if po.get('html') is None:
        po['html'] = True

    return {
        'plugin_options': force_escape(json.dumps(po, cls=DjangoJSONEncoder)),
    }


last_uid = {
    "uid": 0
}


def get_uid():
    last_uid['uid'] += 1
    return last_uid['uid']
