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

                