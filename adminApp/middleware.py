import time
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

class SessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            last_activity = request.session.get('last_activity')
            current_time = time.time()

            if last_activity:
                idle_duration = current_time - last_activity
                if idle_duration > settings.SESSION_COOKIE_AGE:
                    logout(request)
                    return HttpResponseRedirect(settings.LOGOUT_REDIRECT_URL)

            request.session['last_activity'] = current_time

        response = self.get_response(request)
        return response