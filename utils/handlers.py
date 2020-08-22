from django.contrib.auth.tokens import default_token_generator  
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from users.models import User



def send_activation_email(request, user):
	context = {
		'name': user.first_name,
		'domain': get_current_site(request).domain,
		'uid': urlsafe_base64_encode(force_bytes(user.id)),
		'token': default_token_generator.make_token(user),
	}
	email = user.email
	message = render_to_string('users/emails/activation_email.html', context)
	subject = 'Activate Your Account'
	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# bar.py

# def foo(data):
#     // process data
# # urls.py

# from multiprocessing import Process
# from .bar import foo

# @api_view(['POST'])
# def endpoint(request):
#     data = request.data.get('data')

#     p = Process(target=foo, args=(data,))
#     p.start()

#     return Response({})
