from ward import test
from dotenv import dotenv_values
from ad_lambda_mail import search_expired_password
from ad_lambda_mail.send_smtp import send_mail
from ad_lambda_mail.user import User

config = dotenv_values('.env')

#@test("test ldap search on local ad server")
#def search_test():
#    assert search_expired_password(config, 0) == {}
@test("test send mail to smtp local server")
def send_mail_test():
    assert send_mail(config, User(cn="urameshi surname", name="urameshi", sn='surname', mail="urameshi@etv4-mint0x86-64", host="etv4-mint0x86-64")) == {}
