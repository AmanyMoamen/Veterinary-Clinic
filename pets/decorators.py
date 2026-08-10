from django.shortcuts import redirect
from functools import wraps


def role_required(*allowed_roles):
    """
    Allow access only to users who have one of the specified roles.
    """

    def decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # User must be logged in
            if not request.user.is_authenticated:
                return redirect("login")

            # Superuser has full access
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)

            # Check UserProfile
            try:
                role = request.user.profile.role
            except AttributeError:
                return redirect("login")

            # Check allowed roles
            if role in allowed_roles:
                return view_func(request, *args, **kwargs)

            # User doesn't have permission
            return redirect("unauthorized")

        return wrapper

    return decorator