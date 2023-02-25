#!/bin/bash
set -xe

tmpfile=$(mktemp /tmp/usertmp.ldif.XXXXXXXXXX) || exit 1;
padc_script_dir="$HOME/git_hub/padc"
HOST_NAME='etv4-mint0x86-64'

for i in {1..5}; do
    # create ldif for new user
    echo "dn: cn=Pingu${i} pythonico${i},cn=Users,dc=rts,dc=local
cn: Pingu${i} pythonico${i}
sn: pythonico${i}
objectClass: top
objectClass: person
objectClass: organizationalPerson
objectClass: user
sAMAccountName: Pingu${i}
givenName: Pingu${i}
userPrincipalName: Pingu${i}
displayName: Pingu${i}
unicodePwd: PythonicPasswd@1${i}
mail: pingu${i}@${HOST_NAME}
pwdLastSet: 0
userAccountControl: 512" > "$tmpfile"

    # call padc to create user
    env VIRTUAL_ENV="$padc_script_dir/.venv" "$padc_script_dir/.venv/bin/padc" users create-ldif -f "$padc_script_dir/.env" -l "$tmpfile"

done


rm "$tmpfile"
