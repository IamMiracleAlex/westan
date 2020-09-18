from django.shortcuts import render, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse

from listings.models import Listing, WishList
from listings.forms import ListingMapForm


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
    wish = None
    form = ListingMapForm()

    listing = get_object_or_404(Listing, id=id)
    listing.views += 1
    listing.save()

    if request.user.is_authenticated:
        try:
            wish = WishList.objects.get(user=request.user, listing=listing)
        except Exception as e:
            pass

    context = {
        'listing' : listing, 'wish': wish, 'form': form,
    }
    return render(request, 'listings/single_listings.html', context)


def add_wishlist(request):
    final_status, auth = None, None

    if request.user.is_authenticated:

        listing_id = request.GET.get('listing_id', None)
        listing = Listing.objects.get(pk=listing_id)

        try:
            wished = WishList.objects.get(
                listing=listing, user=request.user)
            wished.status = not wished.status
            wished.save()  
            final_status = wished.status 
        except:

            wish = WishList.objects.create(user=request.user, listing=listing, status=True)
            final_status = True

    else:
        auth = "Please login to add this listing to your wish list"

    data = {'final_status': final_status, 'auth': auth}

    return JsonResponse(data)



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


def sort(request, by=None):
    queryset = None

    if by == 'maxprice':
        queryset = Listing.objects.filter(status=Listing.PUBLISHED).order_by('-price')

    if by == 'minprice':
        queryset = Listing.objects.filter(status=Listing.PUBLISHED).order_by('price')

    if by == 'latest':
        queryset = Listing.objects.filter(status=Listing.PUBLISHED).order_by('-created_at')

    if by == 'popular':
        queryset = Listing.objects.filter(status=Listing.PUBLISHED).order_by('-views')

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




def dashboard_marketer_properties(request):
    return render(request, 'listings/dashboard_marketer_properties.html')

def dashboard_client_properties(request):
    return render(request, 'listings/dashboard_client_properties.html')

def dashboard_client_single_properties(request, id, slug=None):
    return render(request, 'listings/dashboard_client_single_properties.html')