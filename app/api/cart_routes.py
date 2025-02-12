from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from ..models import db, Cart, Product, User

cart_routes = Blueprint('cart',__name__)

@cart_routes.route('/')
@login_required
def get_cart():
    cart_items = Cart.query.filter(Cart.userId == current_user.id) \
                          .join(Product) \
                          .join(User, Product.owner_id == User.id) \
                          .all()
                          
    if not cart_items:
        return jsonify({'message': 'Shopping cart is empty.'}), 400
        
    return jsonify({
        'cart': [{
            'id': item.id,
            'userId': item.userId,
            'productId': item.productId,
            'quantity': item.quantity,
            'product': {
                'id': item.product.id,
                'name': item.product.name,
                'price': item.product.price,
                'description': item.product.description,
                'previewImage': item.product.previewImage,
                'owner': {
                    'id': item.product.owner.id,
                    'first_name': item.product.owner.first_name,
                    'last_name': item.product.owner.last_name
                }
            }
        } for item in cart_items]
    }), 200

@cart_routes.route('/', methods=["POST"])
@login_required
def add_to_cart():

    data = request.get_json()

    product_id = data.get('productId')
    quantity = data.get('quantity')

    if not product_id or not isinstance(quantity, int) or quantity <= 0:
        return jsonify({"message": "Invalid input data"}), 400
    
    existing_cart_item = Cart.query.filter_by(
        userId = current_user.id,
        productId = product_id
    ).first()

    if existing_cart_item:
        existing_cart_item.quantity += quantity
    else: 
        new_item_cart= Cart(
            userId = current_user.id,
            productId = product_id,
            quantity= quantity
        )
        db.session.add(new_item_cart)

    db.session.commit()

    return jsonify({"message": "Item added to cart successfully"}), 201

@cart_routes.route('/<int:cart_id>/', methods=['PUT'])
@login_required
def update_cart(cart_id):
    print(f"Received PUT request for cart_id: {cart_id}")
    cart_item = Cart.query.get(cart_id)

    if not cart_item:
        print("Cart item not found")
        return jsonify({"message": "Item not found"}), 404

    data = request.get_json()
    print(f"Request data: {data}")
    new_quantity = int(data.get("quantity"))

    if new_quantity <= 0:
        print("Invalid quantityyyyyyyyyyyyyyyyyyyyyy")
        return jsonify({"message": "Quantity must be greater than 0"}), 400

    cart_item.quantity = new_quantity
    db.session.commit()
    print("Cart item updated successfully")

    return jsonify({"item": cart_item.to_dict()}), 200
    


@cart_routes.route('/<int:cart_id>', methods=["DELETE"])
@login_required
def delete_cart(cart_id):
    cart_item = Cart.query.get(cart_id)

    if not cart_item:
        return jsonify({"message": "Item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()

    return jsonify({"message": "Item removed from cart"}), 200


@cart_routes.route('/checkout/', methods=["POST"])
@login_required
def checkout():
    cart = Cart.query.filter(Cart.userId == current_user.id).all()
    if not cart:
        return jsonify({'message': 'Shopping cart is empty.'}), 400
    
    for item in cart:
        db.session.delete(item)

    db.session.commit()

    return jsonify({"message": "Transaction completed successfully"})


