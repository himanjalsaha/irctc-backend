from flask import Flask
from utils.db import db
from utils.db import create_db
from flask_migrate import Migrate
from routes.users import user_routes
from routes.Trains import train_routes
from models.User import Role
from utils.decorators import require_admin
from flask_cors import CORS
from flask import jsonify
app = Flask(__name__)
CORS(app)
# PostgreSQL Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://irctc_sgwa_user:v51yFXYmfdefCkGC7bdTVbaQcBVg9qgg@dpg-cu0d36pu0jms73cvclfg-a.singapore-postgres.render.com/irctc_sgwa'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)

def add_default_roles():
    roles = ['user', 'admin']  

    for role_name in roles:
        role = Role.query.filter_by(name=role_name).first()
        if not role:
            new_role = Role(name=role_name)
            db.session.add(new_role)
            db.session.commit()
            
    
 
     

with app.app_context():
    create_db()
    add_default_roles()
    
    


# Call this function at the start of your application (e.g., in an init or setup function).
 

app.register_blueprint(user_routes)
app.register_blueprint(train_routes)

    
    
if __name__ == "__main__"  :
    app.run(debug=True)  
