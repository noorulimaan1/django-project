from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginRequiredMiddleware(MiddlewareMixin):
    '''
    Middleware that redirects unauthenticated users to the login page
    when they try to access views that require authentication.
    '''

    def process_request(self, request):
        public_paths = [
            reverse('landing-page'),
            reverse('accounts:login'),
        ]

        dynamic_paths = [
            '/api/v1/leads/',
            '/api/v1/agents/',
            '/admin/',
            '/__debug__/'
        ]

        if request.path in public_paths:
            return None

        for path in dynamic_paths:
            if request.path.startswith(path):
                return None

        if not request.user.is_authenticated:
            return redirect(reverse('landing-page'))

        return None
