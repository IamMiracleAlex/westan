from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from listings.models import Listing


def index(request):  #home page
    return render(request, 'listings/home.html')


def listings(request):

    queryset = Listing.objects.filter(status=Listing.PUBLISHED).order_by('-created_at')

    paginator = Paginator(queryset, 3) # 3 posts per page
    page = request.GET.get('page')
    try:
        listings = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an intger deliver the first page
        listings = paginator.page(1)
    except EmptyPage:
        #  if page is out of range deliver last page of results
        listings = paginator.page(paginator.num_pages)
   
    context = {
        'listings': listings
    }

    return render(request, 'listings/all_listings.html', context)


def single_listing(request, id, slug):

    # listing = get_object_or_404(Listing, id=id, slug=slug)
    context = {
        # 'listing' : listing
    }
    return render(request, 'listings/single_listing.html', context)




def search(request):
    # query_list = Listing.objects.order_by('-list_date') 

    # # keywords
    # if 'keywords' in request.GET:   # checks for keyword search
    #     keywords = request.GET['keywords']  
    #     if keywords:     # makes sure keyword is not an empty string
    #         # searches if the keyword is contained in the field description (case insensitive)
    #         query_list = query_list.filter(description__icontains=keywords) 

    # # city
    # if 'city' in request.GET:
    #     city = request.GET['city']
    #     if city:
    #         query_list = query_list.filter(city__iexact=city) # case insensitive exact search

    # # state
    # if 'state' in request.GET:
    #     state = request.GET['state']
    #     if state:
    #         query_list = query_list.filter(state__iexact=state)

    # # bedrooms
    # if 'bedrooms' in request.GET:
    #     bedrooms = request.GET['bedrooms']
    #     if bedrooms:
    #         query_list = query_list.filter(bedrooms__lte=bedrooms)  # less than or equal to search 

    # # price
    # if 'price' in request.GET:
    #     price = request.GET['price']
    #     if price:
    #         query_list = query_list.filter(price__lte=price)             

    context = {
        # 'state_choices': state_choices,
        # 'bedroom_choices': bedroom_choices,
        # 'price_choices': price_choices,
        # 'properties': query_list,
        # 'values': request.GET
    }
    return render(request, 'listings/search_listings.html', context) 


def test(request):

    # return render(request, 'listings/search_listings.html')
    return render(request, 'listings/single_listings.html')
