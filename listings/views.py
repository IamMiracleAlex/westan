from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Listing


def index(request):  #home page
    return render(request, 'listings/home.html')


def listings(request):
    # listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    # paginator = Paginator(listings, 6)
    # page = request.GET.get('page')
    # paged_listings = paginator.get_page(page)

    # context = {
    #     'listings': paged_listings
    # }

    return render(request, 'listings/all_listings.html')


def single_listing(request, id, slug):

    # listing = get_object_or_404(Listing, id=id, slug=slug)
    # context = {
    #     'listing' : listing
    # }
    return render(request, 'listings/single_listing.html', context)




def search(request):
    query_list = Listing.objects.order_by('-list_date') 

    # keywords
    if 'keywords' in request.GET:   # checks for keyword search
        keywords = request.GET['keywords']  
        if keywords:     # makes sure keyword is not an empty string
            # searches if the keyword is contained in the field description (case insensitive)
            query_list = query_list.filter(description__icontains=keywords) 

    # city
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            query_list = query_list.filter(city__iexact=city) # case insensitive exact search

    # state
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            query_list = query_list.filter(state__iexact=state)

    # bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            query_list = query_list.filter(bedrooms__lte=bedrooms)  # less than or equal to search 

    # price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            query_list = query_list.filter(price__lte=price)             

    context = {
        # 'state_choices': state_choices,
        # 'bedroom_choices': bedroom_choices,
        # 'price_choices': price_choices,
        'properties': query_list,
        'values': request.GET
    }
    return render(request, 'listings/search.html', context) 


def test(request):

    return render(request, 'listings/single_listings.html')
