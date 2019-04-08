register_user_query = '''
            mutation {{
               createUser(
                   email:"{email}",
                   mobileNumber:"{mobileNumber}",
                   password:"{password}",
               ) {{
                 errors
                 success
               }}
            }}
            '''

login_user_query = '''
        mutation GetToken {{
            tokenAuth(
              email: "{email}",
              password: "{password}"
              ){{
              token
              }}
            }}
        '''

update_username_query = '''
          mutation {{
            updateUser(
              username: "{}"
            ){{
              error
              success
              user{{
              id
              username
              }}
            }}
          }}
        '''

update_email_query = '''
          mutation {{
            updateUser(
              email: "{}"
            ){{
              error
              success
              user{{
              id
              email
              }}
            }}
          }}
        '''

update_image_query = '''
          mutation {{
            updateUser(
              profileImage: "{}"
            ){{
              error
              success
              user{{
              id
              profileImage
              }}
            }}
          }}
        '''

add_user_query = '''
mutation {{
        addUser (
          email:"{email}",
          outletId: ["{outletId}"],
          roleId: "{roleId}",
          mobileNumber:"{mobileNumber}",
          firstName: "Firstname",
          lastName: "Lastname",
          username: "username",
          startingDate: "2019-12-04",
          birthday: "2019-11-15"
        ){{
          user{{
            email
          mobileNumber
          }}
        success
        errors
        }}
      }}
  '''
