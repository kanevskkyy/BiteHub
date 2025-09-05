from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy_utils import EmailType, URLType

from backend.extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = db.Column(EmailType,
                      unique=True,
                      nullable=False,
                      index=True)

    password_hash = db.Column(db.Text, nullable=False)
    username = db.Column(db.String(100),
                         nullable=False,
                         unique=True,
                         index=True)
    avatar_url = db.Column(URLType, nullable=False,
                           default='https://res.cloudinary.com/dkdljnfja/image/upload/v1757081419/Profile_Avatar_hsthfe.png')

    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('roles.id'), nullable=False)
    role = db.relationship('Role', backref='users')

    def set_password(self, password: str) -> None:
        self.password_hash = hashpw(password.encode('utf-8'), gensalt()).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))


    __table_args__ = (
        db.CheckConstraint('length(trim(username)) > 0', name='ck_users_username_required'),
    )