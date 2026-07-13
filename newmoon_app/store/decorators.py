"""دکوراتورهای دسترسی پنل مدیریت."""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden


def staff_required(view_func):
    @login_required
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        user = request.user
        if user.is_staff or user.is_superuser:
            return view_func(request, *args, **kwargs)
        if not user.is_authenticated:
            return redirect_to_login(request.get_full_path())
        return HttpResponseForbidden("اجازه دسترسی ندارید")
    return _wrapped
