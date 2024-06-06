from django.shortcuts import redirect

class RestrictAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path.startswith('/media/uploads/'):
            return redirect('home')
        
        return self.get_response(request)