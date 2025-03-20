import requests

JUDGE_SERVER_URL = "http://127.0.0.1:5001/list_checkers"  # Đảm bảo đúng địa chỉ API máy chấm

def get_custom_checkers(use_cache=False):
    """Lấy danh sách checkers từ máy chấm với tùy chọn không sử dụng cache"""
    try:
        response = requests.get(JUDGE_SERVER_URL, timeout=5, 
                               headers={'Cache-Control': 'no-cache'} if not use_cache else {})
        if response.status_code == 200:
            checkers = response.json().get("checkers", [])
            return [(checker[:-3], checker[:-3]) for checker in checkers if checker.endswith(".py")]  # Cắt ".py"
        else:
            print(f"Error: Received status code {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []