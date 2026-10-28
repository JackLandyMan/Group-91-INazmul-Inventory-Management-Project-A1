from flask import Blueprint, jsonify, request

from app import store
from app.models.transaction import Transaction

transactions_bp = Blueprint("transactions", __name__, url_prefix="/transactions")


@transactions_bp.route("", methods=["GET"])
def list_transactions():
    results = list(store.transactions.values())
    product_id = request.args.get("product_id", type=int)
    supplier_id = request.args.get("supplier_id", type=int)
    if product_id is not None:
        results = [t for t in results if t.product_id == product_id]
    if supplier_id is not None:
        results = [t for t in results if t.supplier_id == supplier_id]
    return jsonify([t.to_dict() for t in results])


@transactions_bp.route("", methods=["POST"])
def create_transaction():
    data = request.get_json()
    product = store.products.get(data["product_id"])

    # Check product ID first
    if product is None:
        return jsonify({"error": "Product not found"}), 404

    supplier_id = data.get("supplier_id")
    supplier = store.suppliers.get(supplier_id) if supplier_id is not None else None
    supplier_name = ""
    if supplier_id is not None:
        if supplier is None:
            return jsonify({"error": "Supplier not found"}), 404
        supplier_name = supplier.name

    quantity = data["quantity"]
    tx_type = data["type"]

    #this looks important for fixing quantity stuff
    if tx_type == "IN":
        product.quantity_on_hand += quantity
    elif tx_type == "OUT":
        if (quantity > product.quantity_on_hand):
            return jsonify({"error": "cannot remove into negative values"}), 400
        product.quantity_on_hand -= quantity
    #Added Sale option
    elif tx_type == "SALE":
        product.quantity_on_hand -= quantity
    else:
        return jsonify({"error": "type must be IN, SALE or OUT"}), 400

    transaction_id = store.next_id("transaction")
    transaction = Transaction(
        id=transaction_id,
        product_id=data.get("product_id"),
        product_name=product.name,
        supplier_id=data.get("supplier_id"),
        supplier_name=supplier_name,
        type=tx_type,
        quantity=quantity,
    )
    store.transactions[transaction_id] = transaction
    return jsonify(transaction.to_dict()), 201
