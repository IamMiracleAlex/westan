from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.urls import reverse

from listings.models import Listing, WishList
from transactions.models import Transaction
from listings.forms import ListingMapForm
from utils.handlers import send_contact_us_mail


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
    wish = False
    form = ListingMapForm()

    listing = get_object_or_404(Listing, id=id)
    listing.views += 1
    listing.save()

    if request.user.is_authenticated:
        try:
            wish = WishList.objects.get(user=request.user, listing=listing)
            wish = True 
        except Exception as e:
            pass

    context = {
        'listing' : listing, 'wish': wish, 'form': form,
    }
    return render(request, 'listings/single_listings.html', context)


def add_wishlist(request):
    final_status, auth = None, None

    if request.user.is_authenticated:

        listing_id = request.GET.get('listing_id')

        wish = WishList.objects.filter(listing_id=listing_id, user=request.user)

        if wish.exists():
            wish.delete()
            final_status = False

        else:
            WishList.objects.create(user=request.user, listing_id=listing_id)
            final_status = True

    else:
        auth = """
        Please login to add this listing to your wish list: <br/> <br/> <a href='/login/'> Click to Login </a>  
        """

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
        queryset = queryset.filter(price__lte=maxprice)    

    if minprice:
        queryset = queryset.filter(price__gte=minprice)    

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
    referred_users_ids = [user.id for user in request.user.referrals.all()]
    trans = Transaction.objects.filter(user_id__in=referred_users_ids)

    return render(request, 'listings/dashboard_marketer_properties.html', {"trans": trans})


def dashboard_client_properties(request):
    trans = Transaction.objects.filter(user=request.user, status__in=[Transaction.ALLOCATED, Transaction.COMPLETED])
    context = {
        'trans': trans 
        }
    return render(request, 'listings/dashboard_client_properties.html', context)


def dashboard_wishlist(request):
    wishes = WishList.objects.filter(user=request.user)
    return render(request, 'listings/dashboard_wishlist.html', {'wishes': wishes}) 


def contact(request):
    if request.method == "POST":
        send_contact_us_mail(request.POST)

        data = {'success': 'Hang on! We will get back to you!'}
        return JsonResponse(data)    
    return render(request, 'listings/contact.html')


def privacy(request):
    return render(request, 'listings/privacy.html') 


def faqs(request):
    return render(request, 'listings/faqs.html')    