#models/users.py
from ..extensions import db,Column,Integer,String,TIMESTAMP,func


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    face_recognition_image_path = Column(String(500))
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.current_timestamp(), server_onupdate=func.current_timestamp())

    def serialize(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'face_recognition_image_path': self.face_recognition_image_path,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
        }
