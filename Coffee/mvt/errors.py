from django.shortcuts import render


def not_found_404(request, exception):
    """
    Обработчик исключения not_found_404,
    возвращает кастомную страницу ошибки 404.
    """
    return render(request, 'pages/404.html', status=404)


def csrf_failure(request, reason=''):
    """
    Обработчик исключения csrf_failure,
    возвращает кастомную страницу ошибки 403."
    """
    return render(request, 'pages/403_csrf.html', status=404)
