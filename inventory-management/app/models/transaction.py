from datetime import date


class Transaction:
    def __init__(self, id, product_id, type, quantity,  product_name=None, supplier_id=None, supplier_name=None, transaction_date=None):
        self.id = id
        self.product_id = product_id
        self.product_name = product_name
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.type = type  # "IN" or "OUT"
        self.quantity = quantity
        self.transaction_date = transaction_date or date.today()

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "supplier_id": self.supplier_id,
            "supplier_name": self.supplier_name,
            "type": self.type,
            "quantity": self.quantity,
            "transaction_date": self.transaction_date.isoformat(),
        }
