from app import create_app
from app import db, models
from instance.config import DevelopmentConfig, ProductionConfig, TestingConfig


app = create_app(DevelopmentConfig)
with app.app_context():
        db.create_all()
        # db.session.commit()

if __name__ == '__main__':
    app.run()