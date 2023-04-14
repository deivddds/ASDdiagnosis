import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


package_dir = os.path.abspath(os.path.dirname(__file__))
db_dir = os.path.join(package_dir, 'teadb.db')

DATABASE_URL = ''.join(['sqlite:///', db_dir])

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
