#! /usr/bin/python3
import sys
import ldap3 as ldap
import configparser

# Configparser
conf = configparser.ConfigParser()
conf.read('Config.ini')
ad_server = conf['ldap-config']['ad_server']
ad_user_basedn = conf['ldap-config']['ad_user_basedn']
ad_member_of = conf['ldap-config']['ad_member_of']
ad_bind_usr = conf['ldap-config']['ad_bind_usr']
ad_bind_pwd = conf['ldap-config']['ad_bind_pwd']

# Connect
def ldap_auth (usr = ad_bind_usr, pwd = ad_bind_pwd, address = ad_server):
    serv = ldap.Server('ldap://' + address)
    conn = ldap.Connection(serv, ad_bind_usr, ad_bind_pwd)

    result = True

    if not conn.bind():
        return  conn.result , False
    return conn, result

# get group members
def get_members(groupname, ldap_conn, basedn = ad_user_basedn):
    members = []
    members.append('[{0}]'.format(groupname))
    ad_filter = '(&(objectClass=USER)(sAMAccountName=*){0}(memberOf=cn=Alle,OU=Kopano,dc=chaos,dc=inmedias,dc=it))'.format(ad_member_of)
    if ldap_conn.search(search_base = basedn, search_scope= ldap.SUBTREE, search_filter=ad_filter, attributes=ldap.ALL_ATTRIBUTES ):
        result = ldap_conn.entries
    if result:
        print (result)
        for user in result:
            if 'mail' in user:
                attr_mail = str(user['mail'])
                attr_cn = str(user['cn'])
                members.append(attr_mail + "=" + attr_cn)
                
    return members


if __name__ == "__main__":
  groupname = sys.argv[1]
  ldap_conn, result = ldap_auth()
  if result:
    group_members = get_members(groupname, ldap_conn)
    for m in group_members:
        print(m)
