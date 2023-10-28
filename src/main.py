from portals.click_pay import ClickPayPortal
import sys

from utilities.database_util import DatabaseUtil
from utilities.logging_util import get_logger
from config import DB_URL

logger = get_logger(__name__)


def get_tenant_data_from_clickpay(username, password):
    click_pay_portal = ClickPayPortal()
    tenant_data = click_pay_portal.run(username, password)
    click_pay_portal.stop()

    tenant_data['property_managment_company'] = 'ClickPay'

    return tenant_data


def insert_tenant_to_db(tenant_data):
    db_util = DatabaseUtil(DB_URL)

    if tenant_data is None:
        logger.error('Failed to retrieve tenant data')

        return

    tenant_id = db_util.add_tenant_info(
        tenant_data['address'],
        tenant_data['property_managment_company'],
        tenant_data['email'],
        tenant_data['phone']
    )

    if tenant_id:
        logger.info(f'Inserted tenant with id: {tenant_id}')
    else:
        logger.error('Failed to insert tenant')


if __name__ == '__main__':
    poratl_handlers = {
        'click_pay': get_tenant_data_from_clickpay
    }

    if len(sys.argv) != 4:
        logger.debug(
            f'Number of arguments provided: {len(sys.argv), sys.argv}')
        logger.warning(
            'Invalid number of arguments provided. Usage: python main.py <portal> <username> <password>')
        sys.exit(1)

    # Get the tenant portal and user credentials from the command line
    portal = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]

    if portal not in poratl_handlers:
        logger.error(f'Invalid portal: {portal}')
        sys.exit(1)

    tenant_data = poratl_handlers[portal](username, password)
    insert_tenant_to_db(tenant_data)

 # to retrieve all tenants from the database and print them to the console, add the following code to the bottom of main.py:
# if __name__ == '__main__':
#     db_util = DatabaseUtil(DB_URL)
#     tenants = db_util.get_all_tenant_info()
#     for tenant in tenants:
#         print(tenant)
