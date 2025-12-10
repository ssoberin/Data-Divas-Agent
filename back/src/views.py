# src/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            age = data.get('age')
            # Ваша логика предсказания...
            # Например: result = model.predict([[age]])
            return JsonResponse({'result': f"Predicted for age {age}"})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST requests allowed'}, status=405)
