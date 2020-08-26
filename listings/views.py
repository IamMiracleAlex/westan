from django.shortcuts import render


def index(request):
    return render(request, 'listings/index.html')


def listings(request):
    return render(request, 'listings/listings.html')


def single_listing(request):
    return render(request, 'listings/single_listing.html')