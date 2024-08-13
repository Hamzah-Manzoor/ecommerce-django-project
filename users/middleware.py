import time
from django.utils.deprecation import MiddlewareMixin
from users.models import RequestLog


class RequestLoggingMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        duration = time.time() - request.start_time
        RequestLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            method=request.method,
            path=request.path,
            status_code=response.status_code,
            duration=duration,
            ip_address=self.get_client_ip(request),
        )
        return response

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
