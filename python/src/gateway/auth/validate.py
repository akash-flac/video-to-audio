import os
import requests

def token(request):
    if not "Authorization" in request.headers:
        return None, ("missing credentials", 401)
    
    token = request.headers["Authorization"]
    
    if not token:
        return None, ("missing credentials", 401)
    
    # the gateway service forwards the token to the auth service to validate
    response = requests.post(
        f"http://{os.environ.get('AUTH_SVC_ADDRESS')}/validate",
        headers={"Authorization": token},
    )
    
    # if the token is valid, the auth service will return the payload (claims) - username, exp, iat, admin (stuff that was initially encoded in the token using createJWT function)
    if response.status_code == 200:
        # response.text contains the payload (claims) - a JSON formatted string
        return response.text, None
    else:
        return None, (response.text, response.status_code)
