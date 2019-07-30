from .base import *

DEBUG = False

MIDDLEWARE += [
    'courses.middleware.subdomain_course_middleware',
]

ADMIN = (
    ('Admin', 'info@mysite.com'),
)

ALLOWED_HOSTS = ['.mysite.com']


SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
