import datetime
from sqlalchemy import Column, String, DateTime, Integer, text
from aedem.models import Base

class News(Base):
    
    __tablename__ = 'news'
    id              = Column(Integer,
                        nullable = False, 
                        primary_key = True)
    title           = Column(String, 
                        nullable = False)
    content         = Column(String, 
                        nullable = False)
    source          = Column(String, 
                        nullable = False)
    published_at    = Column(String, 
                        nullable = False)
    external_link   = Column(String, 
                        nullable = False)
    state_abbr      = Column(String, 
                        nullable = False)
    city_name       = Column(String, 
                        nullable = False)    
    created_at      = Column(DateTime, 
                        nullable = False, 
                        server_default = text('NOW()'))    
    last_updated    = Column(DateTime,
                        nullable = False, 
                        server_default = text('NOW()'), 
                        onupdate = datetime.datetime.now)
    def __init__(self, title, content, source, published_at, external_link, state_abbr, city_name)-> None:
        self.title = title
        self.content = content
        self.source = source
        self.published_at = published_at
        self.external_link = external_link
        self.state_abbr = state_abbr
        self.city_name = city_name

    def __repr__(self) -> str:
        return "<News '{id}'>".format(id = self.id)