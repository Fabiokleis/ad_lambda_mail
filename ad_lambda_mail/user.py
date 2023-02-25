from dataclasses import dataclass
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass
class User:
    cn: str
    name: str
    sn: str
    mail: str
    host: str

def parse_cn(cn):
    full_name = [n.capitalize() for n in cn.split()]
    first_name = full_name[0]
    sn = " ".join(full_name[1:])
    full_name = " ".join(full_name)
    return {
        'name': f'{first_name}',
        'sn': f'{sn}',
        'cn': f'{full_name}'
    }

def parse_entry(entry):
    """Simply returns a new instancy of User."""
    name = ''
    sn = ''
    full_name = ''
    mail = entry['mail'] if bool(entry['mail']) else ''

    host = str(entry['mail']).split("@")[1] if bool(entry['mail']) else ''

    if bool(entry['cn']):
        result = parse_cn(entry["cn"])
        full_name = result['cn']
        name = result['name']
        sn = result['sn']

    return User(
            cn=full_name,
            name=name,
            sn=sn,
            mail=mail,
            host=host
        )

