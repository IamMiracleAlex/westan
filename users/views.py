from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum

from users.models import User, Subscribe
from utils.handlers import send_activation_email
from transactions.models import Transaction
from listings.models import Listing


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        next = request.POST.get('next')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

            user_type = request.POST.get('user_type')

            if user_type == 'client' and user.is_client:
                messages.success(request, 'You are now logged in, as a client')
                if next:
                    return redirect(next)
                return redirect(reverse('users:client_dashboard')) # client dashboard

            elif user_type == 'marketer' and user.is_marketer:
                messages.success(request, 'You are now logged in, as a marketer')
                if next:
                    return redirect(next)
                return redirect(reverse('users:marketer_dashboard')) # marketer dashboard

            else:
                auth.logout(request) #log user out
                messages.success(request, 'You are neither a client or a marketer')
                return redirect(reverse('listings:index')) # home

        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html', {'email': email})

    return render(request, 'users/login.html')


def signup(request, refer_code=None):

    if refer_code:
        request.session['refer_code'] = refer_code.lower()

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        referer = None

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is in use')
            return render(request, 'users/signup.html', {'email': email,
                                            'first_name': first_name,
                                            'last_name': last_name,
                                            'phone': phone })

        if request.session.get('refer_code'):
            try:
                referer = User.objects.get(refer_code=request.session['refer_code'])
            except:
                pass

        user_type = request.POST.get('user_type')

        if user_type == 'client': 

            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email, 
                                            phone=phone,
                                            referer=referer,
                                            is_client=True,
                                            password=password)

        elif user_type == 'marketer': 

            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email, 
                                            phone=phone,
                                            referer=referer,
                                            is_marketer=True,
                                            password=password)
        else:
            messages.error(request, 'Must be a client or marketer')
            return render(request, 'users/signup.html')

        send_activation_email(request, user)
        messages.success(request, 'Registeration successful! Kindly verify your email and login')
        return redirect(reverse('users:login'))

    return render(request, 'users/signup.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You're now logged out")
    return redirect('listings:index')


@login_required
def dashboard(request):
    if request.user.is_client:
        return redirect(reverse('users:client_dashboard'))

    elif request.user.is_marketer:    
        return redirect(reverse('users:marketer_dashboard'))
        
    else:
        return redirect(reverse('listings:index'))    


@login_required
def client_dashboard(request):
    if request.user.is_client:
        context = {}
        transactions = Transaction.objects.filter(user=request.user) #get user specific trans
        allocated_properties = transactions.filter(status=Transaction.ALLOCATED) # allocated ppties

        # incomplete transactions
        incomplete_transactions = transactions.exclude(status__in=[Transaction.ALLOCATED, Transaction.COMPLETED])
        # get last incomplete trans, and the it's listing
        last_incomplete_tran = incomplete_transactions.last() 

        if last_incomplete_tran:
            last_listing = last_incomplete_tran.listing

            # sum of all the amounts paid
            sum_paid = incomplete_transactions.filter(listing=last_listing).aggregate(Sum('amount_paid'))['amount_paid__sum']
            
            # listing price
            listing_price = last_incomplete_tran.listing.price        
            
            pending_payment = listing_price - sum_paid
            payment_progress = round(((sum_paid / listing_price) * 100), 2)

            context['pending_payment'] = pending_payment
            context['sum_paid'] = sum_paid
            context['payment_progress'] = payment_progress

        context['allocated_properties'] = allocated_properties
        context['transactions'] = transactions
        context['incomplete_trans'] = last_incomplete_tran

        return render(request, 'users/client.html', context)

    return redirect(reverse('listings:index'))    


@login_required
def marketer_dashboard(request):
    COMMISSION = 0.01  # 10% percent commission earned
    if request.user.is_marketer:
        referrals = request.user.referrals.all()
        trending_listings = Listing.objects.filter(status=Listing.PUBLISHED).order_by('-views')[:10]
        referred_users_ids = [user.id for user in referrals]
        # trans = Transaction.objects.filter(user_id__in=referred_users_ids).distinct("listing") # works only with postgres
        trans = Transaction.objects.filter(user_id__in=referred_users_ids)
        total_sales = trans.filter(status__in=[Transaction.ALLOCATED, Transaction.COMPLETED]).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.0
        commission_earned = total_sales * COMMISSION

        sales_data = []
        now = timezone.now()

        counter = 1
        while counter < 13:
            counter += 1

            month = now - timedelta(days=counter*30)

            sales_data.append(trans.filter(created_at__month=month.month).aggregate(Sum('amount_paid'))['amount_paid__sum'] or 0.0)


        context = {
            "referrals": referrals,
            "trending_listings": trending_listings,
            "num_properties": trans.count(),
            "total_sales": total_sales,
            "commission_earned": commission_earned,
            "sales_data": sales_data,
        }
        return render(request, 'users/marketer.html', context)
        
    return redirect(reverse('listings:index'))    



@login_required
def resend_activation_email(request):
    '''To resend activation email to a user'''
    
    send_activation_email(request, request.user)
    messages.info(request, f'Verification email sent to {request.user.email}')
    return redirect('listings:index')


def activate_email(request, uid, token):
    '''To activate the email address'''
    try:
        id = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(id=id)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    context = {}

    if user and user.email_verified:
        context['message'] = 'Your email has already been verified'
        # return render(request, 'account_activation.html', context)
        return HttpResponse('Your email has already been verified')

    if user and default_token_generator.check_token(user, token):

        user.email_verified = True
        user.save()

        context['message'] = 'Email verification successful'
        # return render(request, 'account_activation.html', context)
        return HttpResponse('Email verification successful')

    else:
        context['message'] = 'Email verification failed'
        # return render(request, 'account_activation.html', context)
        return HttpResponse('Email verification failed')



def profile(request):
    return render(request, 'users/profile.html')


def edit_profile(request, user_id):

    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)

        image = request.FILES.get('image')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone = request.POST.get('phone')
        user.address = request.POST.get('address')
        user.next_of_kin = request.POST.get('next_of_kin')
        user.send_notifications = True if request.POST.get('send_notifications') else False

        if image:
            fs = FileSystemStorage()
            fs.save(image.name, image)
            user.image = image

        user.save()

        messages.success(request, 'Profile has been updated successfully!')
        return redirect(reverse('users:profile'))


    return render(request,'users/edit_profile.html')



def subscribe(request):
    data = {}
    email = request.POST.get('email')

    if email:
        if Subscribe.objects.filter(email=email).exists():
            data['error'] = 'You are already subscribed!'

        else:
            Subscribe.objects.create(email=email, active=True)
            data['success'] = 'Your subscription was successful!'
    else:
        data['error'] = 'Please add an email address!'

    return JsonResponse(data)

   

def test(request):
    pass