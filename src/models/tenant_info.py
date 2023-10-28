from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base

from config import DB_URL

Base = declarative_base()


class TenantInfo(Base):
    __tablename__ = 'tenant_info'
    id = Column(Integer, Sequence('tenant_info_id_seq'), primary_key=True)
    address = Column(String(255))
    property_managment_company = Column(String(255))
    tenant_email = Column(String(255))
    tenant_phone = Column(String(20))

    def __str__(self):
        return f'TenantInfo(id={self.id}, address={self.address}, property_managment_company={self.property_managment_company}, tenant_email={self.tenant_email}, tenant_phone={self.tenant_phone})'


# Connect to the database
engine = create_engine(DB_URL)

# Create the tenant_info table
Base.metadata.create_all(engine)
