import jwt

def generate_token( id  , username , email , role):
    token = jwt.encode({ "id" : id , "username" : username, "email" : email , "role" : role} , "hi3hri3ho" , algorithm="HS256")
    return token
    
    
def decode_token(token):
  
        payload = jwt.decode(token, "hi3hri3ho", algorithms="HS256")
         
        return payload
   