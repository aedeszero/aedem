import datetime

from sqlalchemy import Column, String, DateTime, text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from aedem.models import Base

class Reply(Base):
    __tablename__ = 'replies'
    
    id              = Column(Integer,
                        primary_key = True)
    user_id         = Column(UUID(as_uuid = True),
                        ForeignKey('users.id'))
    user            = relationship("User",
                        back_populates = "replies")
    report_id       = Column(Integer,
                        ForeignKey('reports.id'))
    report          = relationship("Report",
                        back_populates = "replies")
    content         = Column(String,
                        nullable = False)
    last_updated    = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'),
                        onupdate = datetime.datetime.now)
    created_at      = Column(DateTime,
                        nullable = False,
                        server_default = text('NOW()'))

    def __init__(self, content) -> None:
        self.content = content
    
    def __repr__(self) -> str:
        return "<Reply '{id}'>".format(id = self.id)