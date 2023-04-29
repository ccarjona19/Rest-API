from flask import Flask, jsonify, request, abort, redirect, url_for, render_template

app = Flask(__name__)

# Ejemplo de datos en memoria
products = [
    {'id': 1, 'name': 'Producto 1', 'price': 10.99},
    {'id': 2, 'name': 'Producto 2', 'price': 19.99},
    {'id': 3, 'name': 'Producto 3', 'price': 5.99},
]

@app.route('/')
def index():
    return render_template('index.html', products=products)



# Obtener una lista de todos los productos
@app.route('/products/show', methods=['GET'])
def get_products():
    return jsonify(products)

# Obtener un producto por ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = [product for product in products if product['id'] == product_id]
    if len(product) == 0:
        abort(404)
    return jsonify(product[0])

# Crear un nuevo producto
@app.route('/products/create', methods=['POST'])
def create_product():
    if not request.form or not 'name' in request.form:
        abort(400)
    product = {
        'id': products[-1]['id'] + 1,
        'name': request.form['name'],
        'price': request.form['price'],
    }
    products.append(product)
    return redirect(url_for("index"))

@app.route('/products/update/<int:product_id>', methods=['GET', 'POST'])
def update_product(product_id):
    product = [product for product in products if product['id'] == product_id]
    if len(product) == 0:
        abort(404)
    if request.method == 'POST':
        product[0]['name'] = request.form.get('name', product[0]['name'])
        product[0]['price'] = request.form.get('price', product[0]['price'])
        return redirect(url_for('index'))
    return render_template('update.html', product=product[0])

@app.route('/products/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = [product for product in products if product['id'] == product_id]
    if len(product) == 0:
        abort(404)
    if request.method == 'POST':
        products.remove(product[0])
        return redirect(url_for('index'))
    return render_template('delete.html', product=product[0])


if __name__ == '__main__':
    app.run(debug=True)
