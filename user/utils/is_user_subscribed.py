import time
from functools import wraps
from django.shortcuts import redirect
from django.conf import settings

def is_user_subscribed(function=None, *, time_limit=600):
    if function is None:
        return lambda func: is_user_subscribed(func, time_limit=time_limit)

    @wraps(function)
    def inner(request, *args, **kwargs):
        if settings.DEBUG:
            return function(request, *args, **kwargs)
        
        # Django auth user'dan sizin User modelinizdeki karşılığı buluyoruz
        from user.models import User  # your_app yerine kendi app adınızı yazın
        
        try:
            # Auth user'ın username'i ile sizin User modelinizdeki kullanıcıyı buluyoruz
            user = User.objects.get(username=request.user.username)
            
            if not user.is_subscribed:
                if 'subscription_start_time' not in request.session:
                    request.session['subscription_start_time'] = time.time()

                remaining_time = time_limit - (time.time() - request.session['subscription_start_time'])

                if remaining_time <= 0:
                    return redirect('subscription_page')

                request.session.modified = True
                kwargs['remaining_time'] = remaining_time
                return function(request, *args, **kwargs)
            
        except User.DoesNotExist:
            return redirect('login')
        except AttributeError as e:
            print(f"Error: {e}")
            return redirect('subscription_page')

        return function(request, *args, **kwargs)

    return inner