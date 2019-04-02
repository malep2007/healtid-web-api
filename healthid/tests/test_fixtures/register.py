def create_register_query(outlet_id,receipt_id):
    return (f'''
                mutation{{
                createRegister(
                 name: "liver moore"
                 outletId:{outlet_id},
                 receiptId:\"{receipt_id}\",)
                   {{
                    register{{id name}}
                }}
            }}
            ''')


def update_register_query(register_id):
    return (f'''
            mutation{{
                updateRegister {{
               updateRegister (id:{register_id}, input:{{
                  name: "ever moore"
              }}) {{
                success
                  register {{
                    name
                  }}

              }}
              }}
            }}

           ''')


def delete_register_query(register_id):
    return f'''mutation{{
                deleteRegister(id: {register_id}){{success}}
                    }}'''


def query_register(register_id):
    return (f'''query{{register(id: {register_id}){{id}}}}''')
