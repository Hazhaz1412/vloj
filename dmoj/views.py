import secrets
import requests
from django.shortcuts import redirect
from django.contrib.auth import login, get_user_model
from django.conf import settings
import msal

def microsoft_login(request):
    # Generate state and save in session
    state = secrets.token_urlsafe(16)
    request.session['microsoft_auth_state'] = state
    
    msal_app = msal.ConfidentialClientApplication(
        settings.MICROSOFT_AUTH_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{settings.MICROSOFT_AUTH_TENANT_ID}",
        client_credential=settings.MICROSOFT_AUTH_CLIENT_SECRET,
    )
    
    auth_url = msal_app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
        state=state,
    )
    return redirect(auth_url)

def microsoft_callback(request):
    # Validate state to prevent CSRF
    state = request.GET.get('state')
    saved_state = request.session.pop('microsoft_auth_state', None)
    if state != saved_state:
        return redirect('login')  # Invalid state
    
    code = request.GET.get('code')
    if not code:
        return redirect('login')  # No code provided
    
    # Acquire token using MSAL
    msal_app = msal.ConfidentialClientApplication(
        settings.MICROSOFT_AUTH_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{settings.MICROSOFT_AUTH_TENANT_ID}",
        client_credential=settings.MICROSOFT_AUTH_CLIENT_SECRET,
    )
    
    result = msal_app.acquire_token_by_authorization_code(
        code,
        scopes=["openid", "profile", "email"],
        redirect_uri=settings.MICROSOFT_AUTH_REDIRECT_URI,
    )
    
    if 'error' in result:
        return redirect('login')  # Token acquisition failed
    
    # Fetch user details from Microsoft Graph
    access_token = result.get('access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    graph_response = requests.get('https://graph.microsoft.com/v1.0/me', headers=headers)
    if not graph_response.ok:
        return redirect('login')
    
    user_data = graph_response.json()
    email = user_data.get('mail') or user_data.get('userPrincipalName')
    
    # Get or create user
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            username=email,
            email=email,
            first_name=user_data.get('givenName', ''),
            last_name=user_data.get('surname', ''),
        )
    
    login(request, user)
    return redirect('user_page')  # Redirect to user profile