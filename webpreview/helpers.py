try:
    from urlparse import urlparse, urlunparse  # Python2
except ImportError:
    from urllib.parse import urlparse, urlunparse  # Python3


def process_image_url(request_url, image_url, force_absolute_url):
    if not force_absolute_url:
        return image_url

    parsed_image_url = urlparse(image_url)

    if not parsed_image_url.netloc and force_absolute_url:
        scheme, netloc, path, params, query, fragment = urlparse(request_url)
        path = image_url if image_url.startswith('/') else '{}{}'.format(path, image_url)
        url_components = [scheme, netloc, path, None, None, None]
        return urlunparse(url_components)