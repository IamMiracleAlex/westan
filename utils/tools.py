import string, random
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six


def generate_random_number(len):
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(len))

def generate_unique_id(klass, field, len=6):
	new_field = generate_random_number(len)

	if klass.objects.filter(**{field: new_field}).exists():
		return generate_unique_id(klass, field)
	return new_field



# class ActivationTokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             six.text_type(user.id) + six.text_type(timestamp) +
#             six.text_type(user.email_verified)
#         )

