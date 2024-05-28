from Models.Customer import Customer


class CustomerRepository:
    def __init__(self):
        from database import engine
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.customer = None

    def get_all_customers(self):
        return self.session.query(Customer).all()

    def get_customer_by_id(self, customer_id):
        return self.session.query(Customer).filter_by(id=customer_id).first()

    def get_customer_by_name(self, name):
        return self.session.query(Customer).filter_by(name=name).first()

    def create_customer(self, name, phone, address=None):
        customer = Customer(name=name, phone=phone, address=address)
        self.customer = customer
        self.session.add(customer)
        self.session.commit()
        return customer

    def update_customer(self, customer_id, updates):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            for key, value in updates.items():
                setattr(customer, key, value)
            self.session.commit()
        return customer

    def delete_customer(self, customer_id):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            self.session.delete(customer)
            self.session.commit()

    def check_phone_number(self, phone_number):
        customer = self.session.query(Customer).filter_by(phone=phone_number).first()
        if customer is not None:
            self.set_customer(customer)
            return True
        else:
            return False

    def get_customer_by_phone(self, phone_number):
        return self.session.query(Customer).filter_by(phone=phone_number).first()

    def get_customer_name(self):
        return self.customer.name

    def get_customer_id(self):
        return self.customer.id

    def set_customer(self, customer):
        self.customer = customer

    def get_current_customer(self):
        return self.customer

    def edit_customer(self, phone_number, customer_name):
        customer = self.session.query(Customer).filter_by(phone=phone_number).first()
        setattr(customer, "name", customer_name)
        self.session.commit()
        self.session.close()