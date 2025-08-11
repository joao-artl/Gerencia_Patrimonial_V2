from django.http import JsonResponse
from django.db import connection

def keep_alive_view(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            
        return JsonResponse({"status": "ok"}, status=200)

    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)