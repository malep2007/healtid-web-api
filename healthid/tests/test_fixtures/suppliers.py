supplier_mutation = '''
        mutation{
            addSupplier(input:{
                name: "shadik.",
                email: "email@ntale.com",
                mobileNumber:"+256702260027",
                addressLine1:"address",
                addressLine2:"addressline2",
                lga: "lga",
                tierId: 1,
                cityId: 1
                rating:5,
                creditDays:4,
                logo:"logo",
                paymentTermsId: 1,
                commentary: "no comment"

            }){
                supplier{
                id
                supplierId
                city{
                    name
                }
                supplierId
                }
            }
            }
'''

suppliers_query = '''
        query{
            allSuppliers{
                id
                name
            }
        }

'''

approved_suppliers = '''
        query{
            approvedSuppliers{
                id
                name
            }
        }

'''

approve_supplier = '''
        mutation{{
          approveSupplier(id:"{supplier_id}"){{
            success
          }}
        }}

'''
delete_supplier = '''
        mutation{{
          deleteSupplier(id:"{supplier_id}"){{
            success
          }}
        }}

'''

edit_request = '''
        mutation{{
          editSupplier(
            id: "{supplier_id}"
            email: "email9@email.com"
            name: "shack",
            mobileNumber:"+256702260027",
            addressLine1:"address",
            addressLine2:"addressline2",
            lga: "lga",
            tierId:1,
            cityId: 1
            rating:5,
            creditDays:4,
            logo:"logo",
            paymentTermsId:1,
            commentary: "no comment"
          ){{
            message,
            editRequest{{
              id
              name
              mobileNumber
            }}
          }}
        }}

'''

edit_proposal = '''
        mutation{{
          editProposal(
            id: "{proposal_id}"
            name: "sean2",
            mobileNumber:"+256702260027",
            addressLine1:"DreamVille",
            addressLine2:"addressline2",
            lga: "lga",
            rating:5,
            creditDays:4,
            logo:"logo",
            commentary: "no comment"
          ){{
            message,
            editRequest{{
              name
              mobileNumber
            }}
          }}
        }}

'''

edit_requests = '''
        query{
            editRequests{
            id
            name
            isApproved
          }
        }
'''
approve_request = '''
        mutation{{
          approveEditRequest(id:"{request_id}"){{
            message
          }}
        }}
'''
decline_request = '''
        mutation{{
          declineEditRequest(
          id:"{request_id}"
          comment: "No way!"){{
            message
          }}
        }}
'''
filter_suppliers = '''
        query{
          filterSuppliers(rating: 5){
            edges{
              node{
                id
                name
              }
            }
          }
        }
'''

empty_search = '''
        query{
          filterSuppliers(rating: 9){
            edges{
              node{
                id
                name
              }
            }
          }
        }
'''
invalid_search = '''
        query{
          filterSuppliers(tier_Name_Icontains: ""){
            edges{
              node{
                id
                name
              }
            }
          }
        }
'''

user_requests = '''
        query{
            userRequests{
            id
            name
            adminComment
          }
        }
'''

create_suppliers_note = '''
      mutation{{
        createSuppliernote(
          supplierId:"{supplier_id}",
          note:"{note}",
          outletIds:[{outlet_id}]
        ){{
          message
          supplierNote{{
            id
            note
            user{{
              id
              email
            }}
          }}
          supplier{{
            id
            name
            email
          }}

        }}
      }}

'''

update_suppliers_note = '''
      mutation{{
        updateSuppliernote(
          id:{supplier_note},
          note:"{note}",
          outletIds:[{outlet_id}]
        ){{
          success
          supplierNote{{
                id
                note
                user{{
                  id
                  email
                  }}
            supplier{{
              id
              name
              email
            }}
          }}
        }}
      }}

'''


all_suppliers_note = '''
    query{
      allSuppliersNote{
        id
        note
        user{
          id
          email
        }
        supplier{
          id
          name
        }
      }
    }

'''


def supplier_notes(supplier_id):
    return (f'''query{{suppliersNote(id: "{supplier_id}"){{id}}}}''')


def delete_supplier_note(supplier_note):
    return f'''mutation{{
                deleteSuppliernote(id: {supplier_note}){{success}}
                    }}'''
