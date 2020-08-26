import string, random


def generate_random_number(len):
	return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(len))

def generate_unique_id(klass, field, len=6):
	new_field = generate_random_number(len)

	if klass.objects.filter(**{field: new_field}).exists():
		return generate_unique_id(klass, field)
	return new_field

