import datetime

from sqlalchemy import Column, String, DateTime, text, Table, ForeignKey
from sqlalchemy.orm import relationship

from aedem.models import Base

flags_privileges_association = Table(
    'flags_privileges', Base.metadata,
    Column('flag_identifier', String, ForeignKey('flags.identifier')),
    Column('privilege_identifier', String, ForeignKey('privileges.identifier'))
)

class Flag(Base):
    __tablename__ = 'flags'
    
    identifier      = Column(String,
                        nullable = False,
                        unique = True,
                        primary_key = True)
    title           = Column(String,
                        nullable = False)
    description     = Column(String)
    privileges      = relationship("Privilege",
                        secondary = flags_privileges_association)
    last_updated    = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'),
                        onupdate = datetime.datetime.now)
    created_at      = Column(DateTime, 
                        nullable = False,
                        server_default = text('NOW()'))

    def __init__(self, identifier, title, description = None) -> None:
        self.identifier = identifier
        self.title = title
        self.description = description
    
    def __repr__(self) -> str:
        return "<Flag '{name}'>".format(name = self.identifier)