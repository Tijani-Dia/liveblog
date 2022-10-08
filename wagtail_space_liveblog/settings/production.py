from .base import *

# Compress static files offline and minify CSS
# http://django-compressor.readthedocs.org/en/latest/settings/#django.conf.settings.COMPRESS_OFFLINE
COMPRESS_OFFLINE = True

# Use local cache for Django compressor so we can build it in Docker
CACHES["compressor_cache"] = {  # noqa
    "BACKEND": "django.core.cache.backends.locmem.LocMemCache"
}
COMPRESS_CACHE_BACKEND = "compressor_cache"

COMPRESS_FILTERS = {
    "css": [
        "compressor.filters.css_default.CssAbsoluteFilter",
        "compressor.filters.cssmin.CSSMinFilter",
    ]
}

# Ensure that the session cookie is only sent by browsers under an HTTPS connection.
# https://docs.djangoproject.com/en/stable/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# Ensure that the CSRF cookie is only sent by browsers under an HTTPS connection.
# https://docs.djangoproject.com/en/stable/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

WAGTAIL_LIVE_USE_SECURE_WS_CONNECTION = True

try:
    from .local import *
except ImportError:
    pass
