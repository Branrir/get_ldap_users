#! /bin/env python3
import sys
import ldap

ad_server = "10.10.10.10"
ad_user_basedn = "dc=chaos,dc=inmedias,dc=it"
ad_user_filter = '(&(objectClass=USER)(sAMAccountName={username}))'
ad_userdn_filter = '(&(objectClass=USER)(dn={userdn}))'
ad_group_filter = '(&(objectClass=GROUP)(cn={group_name}))'
ad_bind_usr = 'Kopano Agent'
ad_bind_pwd = '10027a8a6637cae33a933535e2dad2cd'

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
    #ad_filter = ad_group_filter.replace('{group_name}', groupname)
    ad_filter = '(&(objectClass=USER)(sAMAccountName=*)(memberOf=cn=Alle,OU=Kopano,dc=chaos,dc=inmedias,dc=it))'
    result = ldap_conn.search_s(basedn, ldap.SCOPE_SUBTREE, ad_filter )
    if result:
        #print (result[0])
        for user, attrb in result:
            if 'mail' in attrb:
                members.append(str(attrb['mail'][0]))
                
    return members


if __name__ == "__main__":
  group_name = sys.argv[1]
  ldap_conn, result = ldap_auth()
  if result:
    group_members = get_members(group_name, ldap_conn)
    for m in group_members:
        print(m)
