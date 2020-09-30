from django import template

from taggit.models import Tag
from listings.models import Listing



register = template.Library()



# get tags
@register.simple_tag
def get_tags(count=7):
    # Gets all tags
    return Tag.objects.all()[:count]


@register.simple_tag
def featured_listings(count=10):
    # retrieves featured listings
    listings = Listing.objects.filter(featured=True).filter(
                    status=Listing.PUBLISHED).order_by('-created_at')[:count]
    return listings


@register.filter
def shrink(value, num_decimals=2):
    # """
    # Django template filter to convert regular numbers to a
    # cool format (ie: 2K, 434.4K, 33M...)
    # :param value: number
    # :param num_decimals: Number of decimal digits
    # """

    # int_value = int(value)
    # formatted_number = '{{:.{}f}}'.format(num_decimals)
    # if int_value < 1000:
    #     return str(int_value)
    # elif int_value < 1000000:
    #     return formatted_number.format(int_value/1000.0).rstrip('0.') + 'K'
    # else:
    #     return formatted_number.format(int_value/1000000.0).rstrip('0.') + 'M'
    

    int_value = int(value)
    formatted_number = '{{:.{}f}}'.format(num_decimals)
    if int_value < 1000:
        return str(int_value)
    elif int_value < 1000000:
        return formatted_number.format(int_value/1000.0).rstrip('0').rstrip('.')+ 'K'
    else:
        return formatted_number.format(int_value/1000000.0).rstrip('0').rstrip('.') + 'M'
    