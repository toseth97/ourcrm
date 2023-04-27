from django.shortcuts import redirect, render


def unauthenticated(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            return redirect("loginPage")

    return wrapper


def allowedUsers(allowed_role=[]):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            group = None
            userGroup = request.user.groups
            if userGroup.exists():
                group = userGroup.all()[0].name
                if group in allowed_role:
                    return view_func(request, *args, **kwargs)
                else:
                    return render(request, 'account/unauthorisedUser.html', {"title": "Unauthorized"})
            else:
                return render(request, 'account/unauthorisedUser.html', {"title": "Unauthorized"})
        return wrapper
    return decorator


def redirection(view_func):
    def wrapper(request, *args, **kwargs):
        group = None
        userGroup = request.user.groups
        if userGroup.exists():
            group = userGroup.all()[0].name

        if group == "customer":
            return redirect("userpage")

        elif group == 'admin':
            return view_func(request, *args, **kwargs)

    return wrapper
