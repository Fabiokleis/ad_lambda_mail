## lambda function
from ldap3 import Server, Connection, ALL

import logging
import json
from dotenv import dotenv_values

from .user import parse_entry
from .send_smtp import send_mail

config = dotenv_values('.env')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def create_user(attr):
    cn = attr['attributes']['cn']
    mail = attr['attributes']['mail']
    dn = attr['dn']
    return parse_entry({ "cn": cn, "mail": mail, "dn": dn })


def search_expired_password(config, tempo):
    """ 
    Procura por todos os usuarios com senha expirada ou até um número de dias estipulado!
    '
    (&
        (objectclass=User)
        (pwdLastSet<=tempo)
        (!(cn=guest))
    )
    '
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
    tempo_nano_sec = 0
    s_filter = f'(&(objectclass=User)(pwdLastSet<={tempo_nano_sec})(!(cn=guest)))'
    attribs = ['cn', 'mail']

    status = conn.search(config['BASE_DN'], search_filter=s_filter, attributes=attribs)
    json_response = conn.response_to_json()
    json_entries = json.loads(json_response)['entries']
    users = []
    for t in json_entries:
        user = create_user(t)
        if bool(user.mail):
            users.append(user)

    return {'status': status, 'entries': users}

def lambda_handler(event, context):
    logger.info('called lambda handler')
    result = search_expired_password(config, 0)
    status = result['status']
    entries = result['entries']
    if not status:
        return {
                'status': False,
                'event': event,
                'context': context
        }
    else:
        for entry in entries:
            send_mail(config, entry)
        #return {'status': status, 'entries': entries}
        
    
