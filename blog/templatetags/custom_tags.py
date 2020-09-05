from django import template
from taggit.models import Tag



register = template.Library()

# filters for adding css classes and html attributes
# @register.filter(name='add_attr')
# def add_attr(field, css):
#     attrs = {}
#     definition = css.split(',')

#     for d in definition:
#         if ':' not in d:
#             attrs['class'] = d
#         else:
#             key, val = d.split(':')
#             attrs[key] = val

#     return field.as_widget(attrs=attrs)




# get tags
@register.simple_tag
def get_tags(count=7):

    return Tag.objects.all()[:count]


                