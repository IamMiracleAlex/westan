import csv
import io
import sys

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator  
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

from PIL import Image


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
    # open the uploaded image
    img = Image.open(image_field)

    if img.height > 200 or img.width > 200:
        output_size = (200, 200)
        img.thumbnail(output_size)
        img = img.convert('RGB')

        output = io.BytesIO()
        img.save(output, format='JPEG')
        output.seek(0)

        # change the imagefield value to be the newley modifed image value
        image_field = InMemoryUploadedFile(
                                file=output, 
                                field_name='ImageField',
                                name=f'{image_field.name.split(".")[0]}.jpg',
                                content_type='image/jpeg',
                                size=sys.getsizeof(output),
                                charset=None)


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
