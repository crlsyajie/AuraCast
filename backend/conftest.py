import os

if os.getenv('DATABASE_URL') is None:
    os.environ['DATABASE_URL'] = 'sqlite:///./weather.db'
