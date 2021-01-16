from django.shortcuts import render


def home(request):
    return render(request, "staticpages/frontpage.html")


# Error Pages
def server_error(request):
    return render(request, 'errorpages/500.html')


def not_found(request, exception):
    data = {"name": "_"}
    return render(request, 'errorpages/404.html', data)


def permission_denied(request):
    return render(request, 'errorpages/403.html')


def bad_request(request):
    return render(request, 'errorpages/400.html')