from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator  

from django.http import HttpResponse

from .models import User
from utils.handlers import send_activation_email



def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']


        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)

            user_type = request.POST.get('user_type', None)

            if user_type == 'client' and user.is_client:
                messages.success(request, 'You are now logged in, as a client')
                # return redirect('dashboard') # client dashboard
                return HttpResponse('You are now logged in, as a client')

            elif user_type == 'marketer' and user.is_marketer:
                messages.success(request, 'You are now logged in, as a marketer')
                # return redirect('dashboard') # marketer dashboard
                return HttpResponse('You are now logged in, as a marketer')
            else:
                messages.success(request, 'You are neither a client or a marketer')
                # return redirect('index') # home
                return HttpResponse('You are neither a client or a marketer')
        else:
            messages.error(request, 'Invalid credentials')
            # return redirect('login')
            return HttpResponse('Invalid credentials')

    return render(request, 'users/login.html')


def signup(request, refer_code=None):

    if refer_code:
        request.session['refer_code'] = refer_code.lower()

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        referer = None

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is in use')
            # return redirect('signup')
            return HttpResponse('This email is in use')

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
                                            # is_active=False,
                                            referer=referer,
                                            is_client=True,
                                            password=password)

        elif user_type == 'marketer': 

            user = User.objects.create_user(first_name=first_name,
                                            last_name=last_name,
                                            email=email, 
                                            phone=phone,
                                            # is_active=False,
                                            referer=referer,
                                            is_marketer=True,
                                            password=password)
        else:
            messages.success(request, 'Must be a client or marketer')
            # return redirect('signup')
            return HttpResponse('Must be a client or marketer')

        send_activation_email(request, user)
        messages.success(request, 'Registeration successful! Kindly login')
        # return redirect('login')
        return HttpResponse('Registration was successful, Verify your email')

    return render(request, 'users/signup.html')


def logout(request):
    auth.logout(request)
    messages.info(request, "You're now logged out")
    # return redirect('index')
    return HttpResponse('You are now logged out')



# @login_required
# def dashboard(request):
#     # pylint: disable = no-member
#     user_contacts = Contact.objects.order_by(
#         '-contact_date').filter(user_id=request.user.id)
#     context = {
#         'contacts': user_contacts
#     }
#     return render(request, 'users/dashboard.html', context)




def resend_activation_email(request):
    '''To resend activation email to a user'''

    return send_activation_email(request, request.user)


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






def test(request):
    return render(request, 'registration/password_reset_email.html')
    # return render(request, 'users/emails/activation_email.html')