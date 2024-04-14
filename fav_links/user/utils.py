import bcrypt
import jwt
from datetime import datetime, timedelta
from .models import Token

def hash_password(password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_jwt_tokens(user_id):
    access_token_expiration = datetime.utcnow() + timedelta(minutes=15)
    refresh_token_expiration = datetime.utcnow() + timedelta(days=7)
    access_token_payload = {
        'user_id': user_id,
        'exp': access_token_expiration,
    }
    refresh_token_payload = {
        'user_id': user_id,
        'exp': refresh_token_expiration,
    }
    access_token = jwt.encode(access_token_payload, key='secret',algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, key='secret',algorithm="HS256")

    return {'access_token' : access_token, 'refresh_token' : refresh_token}

def refresh_jwt_token(refresh_token):
    refresh_token_payload = jwt.decode(refresh_token, 'secret', algorithms=['HS256'])
    user_id = refresh_token_payload.get('user_id')
    current_time = datetime.utcnow()
    current_time_stamp = int(current_time.timestamp())
    refresh_token_exp = refresh_token_payload.get('exp')
    if refresh_token_exp and refresh_token_exp < current_time_stamp:
        raise jwt.ExpiredSignatureError('Refresh token has expired')

    access_token_expiration = current_time + timedelta(minutes=15)
    refresh_token_expiration = current_time + timedelta(days=7)
    access_token_payload = {
        'user_id': user_id,
        'exp': access_token_expiration,
    }
    refresh_token_payload = {
        'user_id': user_id,
        'exp': refresh_token_expiration,
    }
    access_token = jwt.encode(access_token_payload, key='secret',algorithm="HS256")
    refresh_token = jwt.encode(refresh_token_payload, key='secret',algorithm="HS256")
    return {'user_id': user_id,'access_token': access_token, 'refresh_token': refresh_token}

def verify_jwt_token(request):
    if 'HTTP_AUTHORIZATION' in request.META:
        try:
            access_token = request.META['HTTP_AUTHORIZATION']
            payload = jwt.decode(access_token, key='secret',algorithms=["HS256"])
            token = Token.objects.get(user_id=payload["user_id"])
            if access_token == token.access_token:
                return {"status":True, "user_id": payload["user_id"]}
            else:
                return {"status":False}
        except:
            return {"status":False}
        
def strength_password(password):
    upperChars, lowerChars, specialChars, digits, length = 0, 0, 0, 0, 0
    length = len(password)
    if (length < 6):
        return {"status" : False, "message" : "Password must be at least 6 characters long"}
    else:
        for i in range(0, length):
            if (password[i].isupper()):
                upperChars += 1
            elif (password[i].islower()):
                lowerChars += 1
            elif (password[i].isdigit()):
                digits += 1
            else:
                specialChars += 1
    if (upperChars != 0 and lowerChars != 0 and digits != 0 and specialChars != 0):
        return {"status" : True, "message" : "The strength of password is strong"}
    else:
        return {"status" : False, "message" : "The strength of password is not strong"}