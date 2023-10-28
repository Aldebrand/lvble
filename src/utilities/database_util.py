from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from src.models.tenant_info import TenantInfo, Base
from utilities.logging_util import get_logger

logger = get_logger(__name__)


class DatabaseUtil:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        Base.metadata.bind = self.engine
        self.DBSession = sessionmaker(bind=self.engine)

    def add_tenant_info(self, address, property_managment_company, tenant_email, tenant_phone):
            """
            Adds a new tenant to the database with the given information.

            Args:
                address (str): The address of the tenant.
                property_managment_company (str): The name of the property management company.
                tenant_email (str): The email address of the tenant.
                tenant_phone (str): The phone number of the tenant.

            Returns:
                None
            """
            session = self.DBSession()
            try:
                new_tenant = TenantInfo(
                    address=address,
                    property_managment_company=property_managment_company,
                    tenant_email=tenant_email,
                    tenant_phone=tenant_phone
                )

                session.add(new_tenant)
                session.commit()
                logger.info(f'Added tenant info: {str(new_tenant)}')

                return new_tenant.id
            except (SQLAlchemyError, Exception) as e:
                session.rollback()
                logger.error(f'Error adding tenant info: {e}')
                
                return None
            finally:
                session.close()

    def get_all_tenant_info(self):
        session = self.DBSession()
        tenants = session.query(TenantInfo).all()
        session.close()

        return tenants
    
if __name__ == '__main__':
    from config import DB_URL
    db_util = DatabaseUtil(DB_URL)
    db_util.get_all_tenant_info()


