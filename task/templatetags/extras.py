from django import template
from django.utils.safestring import mark_safe

register = template.Library()

TEMPLATE = """<span class="badge badge-Light">
    <label for="{input_id}">{label_name}</label>
    {input}
</span>"""


@register.filter(name='change_format')
def print_all(value):
    output = TEMPLATE.format(label_name=value.label,
                             input_id=str(value.form.auto_id % value.html_name),
                             input=value)
    return mark_safe(output)
