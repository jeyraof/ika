from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import PasswordType

from ika.conf import settings


Base = declarative_base()


class Nick(Base):
    __tablename__ = 'nick'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)
    last_use = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True)
    name = relationship('Nick', uselist=False, backref='user')
    aliases = relationship('Nick', backref='user_alias')
    password = Column(PasswordType(max_length=128,
        schemes=['bcrypt_sha256', 'md5_crypt'], deprecated=['md5_crypt']))
    last_login = Column(DateTime)

    @validates('email')
    def validate_email(self, key, value):
        assert '@' in value
        return value


engine = create_engine(settings.database)
Session = sessionmaker(bind=engine)
