class BusinessModel:
    '''Defines the business Model for BUsiness operations'''

    def __init__(self, business_name, business_type, business_desc):
        # Id will be automatically generated
        self.id = 0
        self.business_name = business_name
        self.business_type = business_type
        self.business_desc = business_desc

class UserModel:
    '''Defines all the user operations'''

    def __init__(self, name,email,password):
        self.id = 0
        self.name = name
        self.email = email
        self.password = password