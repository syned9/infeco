from app import create_app
from instance.config import DevelopmentConfig, ProductionConfig, TestingConfig


app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    app.run()