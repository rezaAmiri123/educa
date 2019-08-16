from .base import *

DEBUG = False

MIDDLEWARE += [
    'courses.middleware.subdomain_course_middleware',
]

ADMIN = (
    ('Admin', 'info@mysite.com'),
)

# ALLOWED_HOSTS = ['.mysite.com', '*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'database1',
        'USER': 'database1_role',
        'PASSWORD': 'database1_password',
        'HOST': 'database1', # <-- Important: same name as docker-compose service
        'PORT': 5432,
    }
}

# SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
