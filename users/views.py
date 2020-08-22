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
            messages.success(request, 'You are now logged in')
            # return redirect('dashboard')
            return HttpResponse('You are now logged in')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    return render(request, 'users/login.html')


def signup(request, refer_code=None):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']
        refer_code = request.POST['refer_code']
        referer = None

        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is in use')
            # return redirect('signup')
            return HttpResponse('This email is in use')

        if refer_code:
            try:
                referer = User.objects.get(refer_code=refer_code.lower())
            except:
                pass
        user = User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        email=email, 
                                        phone=phone,
                                        is_active=False,
                                        referer=referer,
                                        is_client=True,
                                        password=password)
        send_activation_email(request, user)
        messages.success(request, 'Registeration successful! Kindly login')
        # return redirect('login')
        return HttpResponse('Registration was successful, Verify your email')

    return render(request, 'users/signup.html', {'refer_code':refer_code})


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



def activate_email(request, uid, token):
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
    return render(request, 'users/emails/activation_email.html')