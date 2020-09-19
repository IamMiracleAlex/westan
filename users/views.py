from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  
from django.http import HttpResponse, JsonResponse
from django.urls import reverse

from users.models import User, Subscribe
from utils.handlers import send_activation_email




def login(request):
    if request.method == 'POST':
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)


        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

            user_type = request.POST.get('user_type', None)

            if user_type == 'client' and user.is_client:
                messages.success(request, 'You are now logged in, as a client')
                return redirect(reverse('users:client_dashboard')) # client dashboard

            elif user_type == 'marketer' and user.is_marketer:
                messages.success(request, 'You are now logged in, as a marketer')
                return redirect(reverse('users:marketer_dashboard')) # marketer dashboard

            else:
                auth.logout(request) #log user out
                messages.success(request, 'You are neither a client or a marketer')
                return redirect('index') # home

        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'users/login.html', {'email': email})

    return render(request, 'users/login.html')


def signup(request, refer_code=None):

    if refer_code:
        request.session['refer_code'] = refer_code.lower()

    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        referer = None

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is in use')
            return render(request, 'users/signup.html', {'email': email,
                                            'first_name': first_name,
                                            'last_name': last_name,
                                            'phone': phone })

        if request.session.get('refer_code', None):
            try:
                referer = User.objects.get(refer_code=request.session['refer_code'])
            except:
                pass

        user_type = request.POST.get('user_type', None)

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
def client_dashboard(request):
    # user_contacts = Contact.objects.order_by(
    #     '-contact_date').filter(user_id=request.user.id)
    context = {
        # 'contacts': user_contacts
    }
    return render(request, 'users/client.html', context)


@login_required
def marketer_dashboard(request):
    return render(request, 'users/marketer.html',)



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
        is_active = True,
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



def subscribe(request):
    data = {}
    email = request.POST['email'] if 'email' in request.POST else None

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