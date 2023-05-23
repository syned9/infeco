from app import db, models, create_app
from functools import wraps
from flask import redirect, url_for, request
from flask_login import current_user
from instance.config import DevelopmentConfig, ProductionConfig, TestingConfig

app = create_app(DevelopmentConfig)

# @app.before_request
# def before_request():
#     if request.endpoint != 'user_bp.login' and not current_user.is_authenticated:
#         return redirect(url_for('user_bp.login'))

with app.app_context():
        db.create_all()


        
        # db.session.commit()
     

if __name__ == '__main__':
    app.run()