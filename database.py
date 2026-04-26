from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL="postgresql://postgres:1111@localhost/BD_Strahovanie"
#DATABASE_URL = "postgresql://username:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



