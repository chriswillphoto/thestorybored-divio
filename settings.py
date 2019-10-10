# -*- coding: utf-8 -*-

INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-wagtail',
    # </INSTALLED_ADDONS>
]

import aldryn_addons.settings
aldryn_addons.settings.load(locals())


# all django settings can be altered here

INSTALLED_APPS.extend([
    # add your project specific apps here
    'users',
    'blog',
    'images',
    'home',
    'about',
    'contact',
    'wagtail.api.v2',
    'rest_framework',
    'corsheaders'
])

AUTH_USER_MODEL = 'users.user'

WAGTAIL_USER_EDIT_FORM = 'users.forms.CustomUserEditForm'
WAGTAIL_USER_CREATION_FORM = 'users.forms.CustomUserCreationForm'
WAGTAIL_USER_CUSTOM_FIELDS = ['bio']

WAGTAILIMAGES_IMAGE_MODEL = 'images.CustomImage'

WAGTAILAPI_LIMIT_MAX = 30

CORS_ORIGIN_WHITELIST = (
    'https://tashtalevski.com',
    'http://localhost:3000',
    'https://friendly-poincare-58f75c.netlify.com'
)

MIDDLEWARE.insert(
    0,
    'corsheaders.middleware.CorsMiddleware'
)

MIDDLEWARE.insert(
    1,
    'django.middleware.common.CommonMiddleware'
)