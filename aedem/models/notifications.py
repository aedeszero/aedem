import datetime

from sqlalchemy import Column, String, DateTime, text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from aedem.models import Base

class Notification(Base):
    __tablename__ = 'notifications'
    
    id              = Column(Integer,
                        primary_key = True)
    user_id         = Column(UUID(as_uuid = True),
                        ForeignKey('users.id'))
    user            = relationship("User",
                        back_populates = "notifications")
    content         = Column(String,
                        nullable = False)
    notiftype       = Column(String,
                        nullable = False)
    last_updated    = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'),
                        onupdate = datetime.datetime.now)
    created_at      = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'))

    def __init__(self, notiftype, content) -> None:
        self.notiftype = notiftype
        self.content = content
    
    def __repr__(self) -> str:
        return "<Notification '{id}'>".format(name = self.id)