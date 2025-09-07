import os
from sqlalchemy import create_engine, MetaData
from api.models import Base  # Import your models

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)

# Create all tables
Base.metadata.create_all(engine)
print("Database tables created successfully!")
