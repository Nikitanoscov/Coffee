from django.shortcuts import render


def not_found_404(request, exception):
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    return render(request, 'pages/403_csrf.html', status=404)
