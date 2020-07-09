import datetime
import uuid

from sqlalchemy import Column, String, Integer, Date, DateTime, text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from aedem.models import Base
# relation with User is not yet defined
class Attachment(Base):
	__tablename__ = 'attachments'

	id 				= Column(Integer, 
						primary_key = True)
	# user_id 		= Column(UUID(as_uuid = True), 
	# 					ForeignKey('users.id'))
	# user 			= relationship("User", 
	# 					back_populates="attachments")
	report_id 		= Column(Integer, 
						ForeignKey('reports.id'))
	report 			= relationship("Report", 
						back_populates="attachments")
	attachment_addr = Column(String, 
						nullable = False)
	last_updated 	= Column(DateTime, 
						server_default = text('NOW()'), 
						onupdate = datetime.datetime.now)
	created_at 		= Column(DateTime, 
						nullable = False, 
						server_default = text('NOW()'))

	def __init__(self, attachment_addr) -> None:
		self.attachment_addr = attachment_addr

	def __repr__(self) -> str:
		return "<Attachment '{id}'>".format(id = self.id)
