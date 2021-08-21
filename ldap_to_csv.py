#Author Iqbal, Honnur
import os, sys, subprocess
import csv
import fnmatch

ldap_attributes = []



okta_to_ldap_mapping = {
    "login": None,
    "firstName": "givenName",
    "lastName": "sn",
    "middleName": None,
    "email": "mail",
    "mobilePhone": "businessPhone",
    "city": "city",
    "state": "st",
    "zipCode": "postalCode",
    "employeeNumber": None,
    "uid": "uid",
    "accountCreationSource": "accountCreationSource",
    "address1": "address1",
    "address2": "address2",
    "address3": "address3",
    "address4": None,
    "ApplicationEmail": None,
    "authenticationType": "authenticationType",
    "companyName": "companyName",
    "companySize": None,
    "co": "co",
    "countryId": "countryId",
    "cpoe_country": None,
    "poe_market_segment": None,
    "cpoe_site_section": None,
    "enableFlag": "enableFlag",
    "iscustomer": "iscustomer",
    "ispartner": "ispartner",
    "isemployee": "isemployee",
    "languagePreferenceId": "languagePreferenceId",
    "otherState": None,
    "primaryPhone": None,
    "primaryPhoneExt": None,
    "salutation": None,
    "secondayPhoneExt": None,
    "stateId":None,
    "timeZone":None,
    "titleId":None,
    "otherTitle":None,
    "userNameSameAsEmailFlag": "userNameSameAsEmailFlag",
    "accountCreationSourceId": "accountCreationSource",
    "commonName": "cn",
    "employeeType": None,
    "dn": "dn",
}



csv_headings= []
for keys in okta_to_ldap_mapping.keys():
    csv_headings.append(keys)



def get_attributes(ldap_output_sample):
    ldap_attributes = ldap_output_sample.splitlines()
    okta_attributes = []
    for key, value in okta_to_ldap_mapping.items():
        if value is None:
            okta_attributes.append("")
        else: 
            value = value + ":*"
            matching = fnmatch.filter(ldap_attributes, value)
            if matching:
                okta_attributes.append(matching[0].split(":")[1])
            else:
                okta_attributes.append("")  
    return okta_attributes



if __name__ == '__main__':
    output_csv = open('ldap_users.csv', 'w') 
    wr = csv.writer(output_csv, quoting=csv.QUOTE_ALL)
    wr.writerow(csv_headings)
    with open("ldap_users_list.txt", 'r') as emails: 
        for mailid in emails:
            ldap_output = subprocess.check_output(['ldapsearch',  '-h', 'extldap-stage.community.veritas.com' , '-p' , '389' ,'-D' , 'uid=authsymaccount,ou=serviceuser,dc=veritas,dc=com' , '-w' , 'cCt9mD#8', '-b', 'dc=veritas,dc=com', 'mail={}'.format(mailid)])  
            output = get_attributes(ldap_output)
            wr.writerow(output)








