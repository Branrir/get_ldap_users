#! /bin/env python3
import sys
import ldap
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
    conn = ldap.initialize('ldap://' + address)
    conn.protocol_version = 3
    conn.set_option(ldap.OPT_REFERRALS, 0)

    result = True

    try:
        conn.simple_bind_s(usr, pwd)
        print ("connection siccesful")
    except ldap.INVALID_CREDENTIALS:
        return "credentils wrong", False
    except ldap.SERVER_DOWN:
        return "server down", False
    except ldap.LDAPError as e:
        return e, False
    
    return conn, result

# get group members
def get_members(groupname, ldap_conn, basedn = ad_user_basedn):
    members = []
    members.append(f'[{groupname}]')
    ad_filter = f'(&(objectClass=USER)(sAMAccountName=*){ad_member_of}(memberOf=cn=Alle,OU=Kopano,dc=chaos,dc=inmedias,dc=it))'
    result = ldap_conn.search_s(basedn, ldap.SCOPE_SUBTREE, ad_filter )
    if result:
        #print (result[0])
        for user, attrb in result:
            if 'mail' in attrb:
                tmp_mail = ""
                tmp_cn = ""
                attr_mail = str(attrb['mail'][0])
                attr_cn = str(attrb['cn'][0])
                for i in range(0, len(attr_mail)):
                    if i != 0:
                        tmp_mail = tmp_mail + attr_mail[i]
                for i in range(0, len(attr_cn)):
                    if i !=0:
                        tmp_cn = tmp_cn + attr_cn[i]
                members.append(tmp_mail + "=" + tmp_cn)
                
    return members


if __name__ == "__main__":
  groupname = sys.argv[1]
  ldap_conn, result = ldap_auth()
  if result:
    group_members = get_members(groupname, ldap_conn)
    for m in group_members:
        print(m)
