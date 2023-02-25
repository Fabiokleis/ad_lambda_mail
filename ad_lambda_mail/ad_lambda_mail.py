## lambda function
from ldap3 import Server, Connection, ALL

import logging
import json
from datetime import datetime, timedelta


from dotenv import dotenv_values

from .user import parse_entry
from .send_smtp import send_mail
from .filetime import from_datetime 

config = dotenv_values('.env')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def create_user(attr):
    cn = attr['attributes']['cn']
    mail = attr['attributes']['mail']
    dn = attr['dn']
    return parse_entry({ "cn": cn, "mail": mail, "dn": dn })



def search_expired_password(config, dias, range_de_dias):
    """ 
    Procura por todos os usuarios com senha expirada ou até um número de dias estipulado!
    '
    (&
        (objectCategory=Person)
        (objectClass=inetOrgPerson)
        (objectclass=User)
        (|
            (pwdLastSet<=(hoje - dias - range_de_dias))
            (pwdLastSet=0)
        )
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

    # (hoje - dias) = senha mais velha possivel = max_age
    # (max_age - range_de_dias) = senha faltando pouco tempo para expirar = expiration_range
    tempo_nano_sec = from_datetime(datetime.now() - timedelta(days=dias) - timedelta(days=range_de_dias))
    s_filter = f'(&(objectCategory=Person)(objectClass=inetOrgPerson)(objectclass=User)(|(pwdLastSet<={tempo_nano_sec})(pwdLastSet=0)))'
    attribs = ['cn', 'mail', 'pwdlastset']

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

    # default: max_age = 47 dias, range = 7 dias
    result = search_expired_password(
            config, 
            int(config['MAX_AGE']),
            int(config['DAYS_RANGE'])
    ) 
    status = result['status']
    entries = result['entries']
    if not status:
        result = {
            'status': status,
            'event': event,
            'context': context
        }
        logger.error(f'result: {result}')
        return result
    else:
        for entry in entries:
            send_mail(config, entry)
            logger.info(f"send mail: from {config['SMTP_USER']}@{config['HOST_NAME']} to {entry.mail}")

        entries_parsed = []
        for entry in entries:
            entries_parsed.append(entry.to_json())

        return {'status': status, 'entries': entries_parsed}
