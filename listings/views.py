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

    listing = get_object_or_404(Listing, id=id)
    context = {
        'listing' : listing
    }
    return render(request, 'listings/single_listings.html', context)




def search(request):
    results = []

    query = request.GET['q'] if 'q' in request.GET else None
    type = request.GET['type'] if 'type' in request.GET else None
    bedrooms = request.GET['bedrooms'] if 'bedrooms' in request.GET else None
    bathrooms = request.GET['bathrooms'] if 'bathrooms' in request.GET else None
    reference = request.GET['reference'] if 'reference' in request.GET else None
    minprice = request.GET['minprice'] if 'minprice' in request.GET else None
    maxprice = request.GET['maxprice'] if 'maxprice' in request.GET else None


    queryset = Listing.objects.filter(status=Listing.PUBLISHED)

    if type:
        queryset = queryset.filter(type__iexact=type)

    if query:
        queryset = queryset.filter(title__icontains=query)

    if bedrooms:
        queryset = queryset.filter(bedrooms__lte=bedrooms)

    if bathrooms:
        queryset = queryset.filter(bathrooms__lte=bathrooms)

    if maxprice:
        queryset = queryset.filter(maxprice__lte=maxprice)    

    if minprice:
        queryset = queryset.filter(minprice__gte=minprice)    

    if reference:
        queryset = Listing.objects.filter(reference=reference)

    paginator = Paginator(queryset, 1) # 3 posts per page
    page = request.GET.get('page')
    try:
        results = paginator.page(page)
    except PageNotAnInteger:
        # if page is not an intger deliver the first page
        results = paginator.page(1)
    except EmptyPage:
        #  if page is out of range deliver last page of results
        results = paginator.page(paginator.num_pages)

    
    context = {
        'listings': results,
        'values': request.GET
    }
    return render(request, 'listings/search_listings.html', context) 
