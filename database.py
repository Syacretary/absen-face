import os
import datetime
import numpy as np # Import numpy to handle face_recognition encodings
from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_PATH

# Ensure the instance directory exists
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

# Database setup
engine = create_engine(f'sqlite:///{DATABASE_PATH}')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    nis = Column(String, nullable=False) # Nomor Induk Siswa
    name = Column(String, nullable=False)
    class_name = Column(String, nullable=False)
    absent_number = Column(String, nullable=False)
    face_encoding = Column(LargeBinary, nullable=False) # Store face encodings as binary

    def __repr__(self):
        return f"<User(id={self.id}, name='{self.name}', class_name='{self.class_name}')>"

    def get_face_encoding_array(self):
        return np.frombuffer(self.face_encoding, dtype=np.float64)

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    activity = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return f"<Visit(id={self.id}, user_id={self.user_id}, activity='{self.activity}', timestamp='{self.timestamp}')>"

def init_db():
    Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
# session = Session() # Do not create a global session, create per-request or per-task
