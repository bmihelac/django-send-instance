from django import template

register = template.Library()


@register.inclusion_tag('send_instance/email/_render_fields.html')
def render_fields(obj, include=None, exclude=None):
    if include:
        field_names = include.split(',')
    else:
        field_names = [f.name for f in obj._meta.fields]
        if exclude:
            exclude_fields = exclude.split(',')
            field_names = [f for f in field_names if f not in exclude_fields]

    fields = []
    for field_name in field_names:
        name = obj._meta.get_field_by_name(field_name)[0].verbose_name
        display_method = 'get_%s_display' % field_name
        if hasattr(obj, display_method):
            value = getattr(obj, display_method)()
        else:
            value = getattr(obj, field_name)
        value = getattr(obj, field_name)
        fields.append({
            'name': name,
            'value': value,
            })
    return {'fields': fields}
