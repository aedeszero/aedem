import datetime

from sqlalchemy import Column, String, DateTime, Boolean, text

from aedem.models import Base

class Privilege(Base):
    __tablename__ = 'privileges'
    
    identifier      = Column(String,
                        unique = True,
                        nullable = False,
                        primary_key = True)
    assignable      = Column(Boolean,
                        nullable = False,
                        default = True)
    last_updated    = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'),
                        onupdate = datetime.datetime.now)
    created_at      = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'))

    def __init__(self, identifier, assignable = True) -> None:
        self.identifier = identifier
        self.assignable = assignable
    
    def __repr__(self) -> str:
        return "<Privilege '{name}'>".format(name = self.identifier)