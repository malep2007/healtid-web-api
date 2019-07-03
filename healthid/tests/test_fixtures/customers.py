create_customer = '''
      mutation{{
        createCustomer(
            firstName:"{first_name}",
            lastName:"{last_name}",
            email: "{email}",
            cityId:{city_id},
            countryId:{country_id},
            primaryMobileNumber:"{primary_mobile_number}",
            secondaryMobileNumber:"{secondary_mobile_number}",
            loyaltyMember:{loyalty_member},
            localGovernmentArea:"Okene",
            addressLine1:"Oshodi 2",
            addressLine2:"Oshodi 1",
            emergencyContactName:"Moses",
            emergencyContactEmail:"{emergency_contact_email}",
            emergencyContactNumber:"+256788088831"
        ){{
            message
        customer{{
                id
                firstName
                lastName
                primaryMobileNumber
                secondaryMobileNumber
                email
                addressLine1
                addressLine2
                localGovernmentArea
                emergencyContactName
                emergencyContactNumber
                emergencyContactEmail
                loyaltyMember
                createdAt
        }}
        }}
        }}

'''

customer_query_all = '''
    query{
        customers{
            id
            firstName
            lastName
        }
    }
'''

customer_name_query = '''
    query{{customer(name: "{name}"){{
        id
        firstName
        lastName
        email
    }}
    }}
'''

customer_number_query = '''
    query{{customer(mobileNumber: "{mobile_number}"){{
        id
        firstName
        lastName
        email
    }}
    }}
'''

customer_id_query = '''
    query{{customer(customerId: "{customer_id}"){{
        id
        firstName
        lastName
        email
    }}
    }}
'''

customer_search_query = '''
    query{{
        filterCustomers({search_key}: "{search_term}"){{
            edges {{
                node {{
                id
                firstName
                lastName
                email
                }}
            }}
        }}
    }}
'''


def edit_customer_basic_profile(update_data):
    return f'''
      mutation{{
        editCustomerBasicProfile(
            id: {update_data["id"]},
            firstName:\"{update_data["first_name"]}\",
            lastName:\"{update_data["last_name"]}\",
            email: \"{update_data["email"]}\",
            cityId:{update_data["city_id"]},
            countryId:{update_data["country_id"]},
            primaryMobileNumber:\"{update_data["primary_mobile_number"]}\",
            secondaryMobileNumber:\"{update_data["secondary_mobile_number"]}\",
            loyaltyMember:{update_data["loyalty_member"]},
            localGovernmentArea:\"{update_data["local_government_area"]}\",
            addressLine1:\"{update_data["address_line_1"]}\",
            addressLine2:\"{update_data["address_line_2"]}\",
            emergencyContactName:\"{update_data["emergency_contact_name"]}\",
            emergencyContactEmail:\"{update_data["emergency_contact_email"]}\",
            emergencyContactNumber:\"{update_data["emergency_contact_number"]}\"
        ){{
            message
            customer {{
              firstName
              lastName
              primaryMobileNumber
              secondaryMobileNumber
              email
              addressLine1
              addressLine2
              localGovernmentArea
              city {{
                id
                name
              }}
              country {{
                id
                name
              }}
        }}
        }}
        }}
'''
