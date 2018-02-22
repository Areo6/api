class BusinessModel():
    def __init__(self, business_name,business_type,business_description):
        # This method initialises the BusinessModel class
        # id will be automaticaly generated.
        self.id = 0
        self.business_name = business_name
        self.business_type = business_type
        self.business_description = business_description
