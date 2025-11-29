from Models.Product import Product, Category, SubCat1, SubCat2, SubCat3
from sqlalchemy.exc import DataError


class ProductRepository:
    def __init__(self):
        from database import engine
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def get_products_by_label(self, label):
        if isinstance(label, str):
            try:
                label = Category[label]
            except KeyError:
                label = Category(label)

        return self.session.query(Product).filter_by(label=label).all()

    def insert_items(self, names, codes, labels, prices):
        uniqueNames = list(set(names))
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

    def insert_items(self, names, codes, labels, prices):
        products = []
        for name, code, label, price in zip(names, codes, labels, prices):
            name = str(name).strip()
            code = str(code).strip()
            try:
                product = Product(name, code, label, price)
            except DataError:
                product = Product(name, code, price=0.0)

            products.append(product)

        self.session.add_all(products)
        self.session.commit()
        self.session.close()

    def get_product_by_name(self, name):
        return self.session.query(Product).filter_by(name=name).first()

    def get_product_by_code(self, code):
        return self.session.query(Product).filter_by(code=code).first()

    def edit_product_label(self, code, new_label):
        product_item = self.get_product_by_code(code)
        if not product_item:
            return

        if isinstance(new_label, Category):
            label_enum = new_label

        elif isinstance(new_label, str):
            try:
                label_enum = Category[new_label]
            except KeyError:
                try:
                    label_enum = Category(new_label)
                except ValueError:
                    label_enum = Category.Cat5
        else:
            label_enum = Category.Cat5

        product_item.label = label_enum
        self.session.commit()
        self.session.close()

    def edit_product_price(self, code, new_price):
        product_item = self.get_product_by_code(code)
        if not product_item:
            return
        product_item.price = new_price
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

    def get_children_label(self, label):
        if isinstance(label, str):
            try:
                label = Category[label]
            except KeyError:
                label = Category(label)

        if label == Category.Cat1:
            return list(SubCat1)
        elif label == Category.Cat2:
            return list(SubCat2)
        elif label == Category.Cat3:
            return list(SubCat3)
        else:
            return []

    def get_product_by_id(self, p_id):
        return self.session.query(Product).filter_by(id=p_id).first()

    def get_products_by_sub_label(self, parent_label, sub_label):
        if isinstance(parent_label, Category):
            label_enum = parent_label
        elif isinstance(parent_label, str):
            try:
                label_enum = Category[parent_label]
            except KeyError:
                label_enum = Category(parent_label)
        else:
            raise TypeError(f"Unsupported parent_label type: {type(parent_label)}")

        category_products = (
            self.session.query(Product)
            .filter_by(label=label_enum.value).all())

        return [product for product in category_products if sub_label in product.name]
