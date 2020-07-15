import datetime
import uuid

from sqlalchemy import Column, String, Integer, Date, DateTime, text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from aedem.models import Base
# relations with User and IPRecord are not yet defined
class Report(Base):
	__tablename__ = 'reports'

	id 				= Column(Integer, 
						primary_key = True)
	user_id 		= Column(UUID(as_uuid = True),
						ForeignKey('users.id'))
	user 			= relationship("User", 
						back_populates="reports")
	status 			= Column(Boolean,
						nullable = False,
						default = True)
	state_abbr 		= Column(String, 
						nullable = False)
	city_name 		= Column(String, 
						nullable = False)
	area 			= Column(String, 
						nullable = True)
	geolatitude 	= Column(String, 
						nullable = True)
	geolongitude 	= Column(String, 
						nullable = True)
	last_updated 	= Column(DateTime, 
						server_default = text('NOW()'), 
						onupdate = datetime.datetime.now)
	created_at 		= Column(DateTime, 
						nullable = False, 
						server_default = text('NOW()'))
	# id_ipaddr 	= Column(Integer, 
	# 					ForeignKey('ip_records.id'))
	# ipdarr 		= relationship("IPRecord", 
	# 					back_populates="reports")
	description 	= Column(String, 
						nullable = True)
	attachments 	= relationship('Attachment', 
						back_populates='report')

	def __init__(self, state_abbr, city_name, area, geolatitude, geolongitude, 
				description) -> None:
		self.state_abbr = state_abbr
		self.city_name = city_name
		self.area = area
		self.geolatitude = geolatitude
		self.geolongitude = geolongitude
		self.description = description

	def __repr__(self) -> str:
		return "<Report '{id}'>".format(id = self.id)
