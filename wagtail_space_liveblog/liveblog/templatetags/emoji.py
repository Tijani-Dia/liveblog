from django import template
from emoji_data_python import replace_colons

register = template.Library()


@register.filter
def emojify(block):
    if block.block_type == "text":
        block.value.source = replace_colons(block.value.source)
    return block
