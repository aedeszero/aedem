import datetime
import uuid

from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from aedem.models import Base

class User(Base):
    __tablename__ = 'users'

    id              = Column(UUID(as_uuid = True),
                        unique = True,
                        primary_key = True,
                        default = uuid.uuid4)
    name            = Column(String,
                        nullable = False)
    passhash        = Column(String,
                        nullable = False)
    salt            = Column(String,
                        nullable = False)
    email           = Column(String,
                        unique = True,
                        nullable = False)
    status          = Column(Boolean,
                        nullable = False,
                        default = False)
    phone           = Column(String,
                        unique = True)
    birthday        = Column(Date)
    zip_code        = Column(String,
                        nullable = False)
    state_abbr      = Column(String(2),
                        nullable = False)
    city_name       = Column(String,
                        nullable = False)
    city_number     = Column(Integer)
    area            = Column(String,
                        nullable = False)
    flag_id         = Column(String,
                        ForeignKey('flags.identifier', ondelete = 'CASCADE'))
    flag            = relationship('Flag', backref = 'users')
    notifications   = relationship("Notification",
                        back_populates = "user")
    reports         = relationship('Report',
                        back_populates = 'user')
    attachments     = relationship('Attachment',
                        back_populates = 'user')
    replies         = relationship('Reply',
                        back_populates = 'user')
    last_updated    = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'), 
                        onupdate = datetime.datetime.now)
    created_at      = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'))

    def __init__(self, name, passhash, salt, email, phone, birthday, zip_code,
                state_abbr, city_name, city_number, area) -> None:
        self.name = name
        self.passhash = passhash
        self.salt = salt
        self.email = email
        self.phone = phone
        self.birthday = birthday
        self.zip_code = zip_code
        self.state_abbr = state_abbr
        self.city_name = city_name
        self.city_number = city_number
        self.area = area
    
    def __repr__(self) -> str:
        return "<User '{name}'>".format(name = self.name)