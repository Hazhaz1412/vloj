import requests
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from judge.models.checkers import get_custom_checkers

@csrf_exempt
def proxy_delete_checker(request, filename):
    """Proxy endpoint để xóa checker từ máy chấm"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied'}, status=403)
        
    try:
        response = requests.delete(f'http://127.0.0.1:5001/list_checkers/{filename}')
        return JsonResponse(response.json(), status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
        
@csrf_exempt
def proxy_upload_checker(request):
    """Proxy endpoint để tải lên checker tới máy chấm"""
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    if request.method != 'POST' or 'file' not in request.FILES:
        return JsonResponse({'error': 'Invalid request'}, status=400)
        
    try:
        files = {'file': request.FILES['file']}
        response = requests.post('http://127.0.0.1:5001/upload_checker', files=files)
        return JsonResponse(response.json(), status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@never_cache
def refresh_checkers(request):
    """Endpoint để làm mới danh sách checkers"""
    checkers = get_custom_checkers(use_cache=False)  # Buộc lấy dữ liệu mới
    
    # Format dữ liệu đúng: Trả về danh sách tên file thay vì objects
    checker_files = [c[0] + '.py' for c in checkers]
    
    response = JsonResponse({
        'success': True, 
        'checkers': checker_files,  # Danh sách chuỗi thay vì objects
        'select2_data': [{'id': c[0], 'text': c[1]} for c in checkers]  # Dữ liệu cho Select2
    })
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    
    return response