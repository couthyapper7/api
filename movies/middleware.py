from django.http import JsonResponse
from django.core.exceptions import ValidationError
from django.forms.fields import URLField

def validate_url(url):
    url_form_field = URLField()
    try:
        url = url_form_field.clean(url)
    except ValidationError:
        return False
    return True

class Custom404Middleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if response.status_code == 404:
            try:
                url_segments = request.path.split('/')
                if len(url_segments) >= 2:
                    param = url_segments[-2]
                    try:
                        int_param = int(param)
                    except ValueError:
                        return JsonResponse({'result': False, 'data': 'Invalid number, please enter a valid number', 'url': request.path}, status=404)
                    if not validate_url(param):
                        return JsonResponse({'result': False, 'data': 'Invalid URL, please enter a valid path', 'url': request.path}, status=404)

                    return JsonResponse({'result': False, 'data': f'Invalid character, please enter a valid number: {int_param}', 'url': request.path}, status=404)
                else:
                    return JsonResponse({'result': False, 'data': 'Invalid URL, please enter a valid path', 'url': request.path}, status=404)
            except ValueError:

                return JsonResponse({'result': False, 'data': 'Invalid URL, please enter a valid path', 'url': request.path}, status=404)

        return response
