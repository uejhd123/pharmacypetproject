from django.urls import resolve


def current_path(request):
    return {
        'current_path': resolve(request.path_info).url_name
    }
