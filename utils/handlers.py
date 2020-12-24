import csv
import io

from django.core.files.storage import default_storage as storage
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator  
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from PIL import Image

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


class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(
            meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field)
                                   for field in field_names])
        return response


def image_resizer(image_field):

    img_read = storage.open(image_field.name, 'r')
    img = Image.open(img_read)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        in_mem_file = io.BytesIO()
        img.convert('RGB').save(in_mem_file, format='JPEG')
        img_write = storage.open(image_field.name, 'w+')
        img_write.write(in_mem_file.getvalue())
        img_write.close()

    img_read.close()   


def send_transaction_status_email(profile):
    context = {'first_name': profile.first_name }
    subject = 'Career Acceleration Program Status'
    message = render_to_string('transactions/emails/success.txt', context)
    email = profile.email_address
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
