## lambda function
from ldap3 import Server, Connection, ALL

import logging
from dotenv import dotenv_values

config = dotenv_values('.env')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def search_expired_password(config, tempo):
    """ 
    Procura por todos os usuarios com senha expirada!
    '(&
        (&
            (objectclass=User)
            (pwdLastSet=tempo)
        )
        (!(cn=guest))
    )'
    """

    logger.info(f"config: {config}")
    logger.info('called ldap search at active directory')
    server = Server(config['AD_SERVER'], get_info=ALL)
    conn = Connection(
            server=server,
            user=config['BIND_DN'], 
            password=config['AUTH_PASS'],
            auto_bind=True
            )
    conn.start_tls()
    s_filter = f'(&(&(objectclass=User)(pwdLastSet={tempo}))(!(cn=guest)))'
    attribs = ['cn', 'mail']

    conn.search(config['BASE_DN'], search_filter=s_filter, attributes=attribs)
    result = []
    for i in conn.entries:
        result.append(i.entry_to_json())
    return {'message' : f'{conn.entries[0].entry_to_json()}'}


def lambda_handler(event, context):
    logger.info('called lambda handler')
    return search_expired_password(config, 0)


