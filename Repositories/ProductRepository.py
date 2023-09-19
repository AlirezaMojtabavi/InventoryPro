from Models.Product import Product, Category, TereaCategory, HeetsCategory, IqosCategory
from sqlalchemy.exc import DataError


class ProductRepository:
    def __init__(self):
        from database import engine
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_products_by_label(self, label):
        return self.session.query(Product).filter_by(label=label).all()

    def insert_items(self, names, codes, labels, prices):
        uniqueNames = list(set(names))
        uniqueCodes = list(set(codes))
        products = []
        for i in range(len(uniqueNames)):
            name = names[i].strip()
            code = str(codes[i]).strip()
            label = labels[i]
            price = prices[i]
            try:
                product = Product(name, code, label, price)

            except DataError:
                product = Product(name, code, price=0.0)

            products.append(product)
        self.session.add_all(products)
        self.session.commit()
        self.session.close()

    def insert_item(self, name, code, label=None, price=10.0):
        name = name.strip()
        code = code.strip()
        if label is not None:
            try:
                product = Product(name, code, price, label)
            except DataError:
                product = Product(name, code, price)  # Set default value for label

        else:
            product = Product(name, code, price)
        self.session.add(product)
        self.session.commit()
        self.session.close()

    def get_product_by_name(self, name):
        return self.session.query(Product).filter_by(name=name).first()

    def get_product_by_code(self, code):
        return self.session.query(Product).filter_by(code=code).first()

    def edit_product_label(self, code, _label):
        product_item = self.get_product_by_code(code)
        setattr(product_item, product_item.label, Category(_label))
        # product_item.label = _label
        self.session.commit()
        self.session.close()

    def edit_product_price(self, code, new_price):
        product_item = self.get_product_by_code(code)
        setattr(product_item, product_item.price, new_price)
        # product_item.price = new_price
        self.session.commit()
        self.session.close()

    def delete_product(self, code):
        product = self.get_product_by_code(code)
        if product:
            self.session.delete(product)
            self.session.commit()
            self.session.close()

    def get_category_length(self):
        return len(Category)

    def get_all_categories(self):
        return list(Category)

    def get_children_label(self, label_name):
        if label_name == Category.Terea:
            return list(TereaCategory)
        elif label_name == Category.Heets:
            return list(HeetsCategory)
        elif label_name == Category.Iqos:
            return list(IqosCategory)
        else:
            return False

    def get_product_by_id(self, p_id):
        return self.session.query(Product).filter_by(id=p_id).first()

    def get_products_by_sub_label(self, parent_label, sub_label):
        category_products = self.session.query(Product).filter_by(label=parent_label).all()
        return [product for product in category_products if sub_label in product.name]


