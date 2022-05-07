import pprint

import requests
import random
import json

headers = {"Content-type": "application/json"}

if __name__ == '__main__':
    # get products
    response = requests.get("http://localhost:8080/products/api/products")
    products = response.json()

    assert response.status_code == 200, f"{response.content}"

    assert len(products) > 0

    print(f"get {len(products)} products")

    product1 = random.choice(products)
    product2 = random.choice(products)

    pprint.pprint(product1)

    pprint.pprint(product2)

    cart = {
        "items": [
            {
                "amount": 1,
                "product": product1
            }
        ]
    }

    # create a cart
    response = requests.post("http://localhost:8080/carts/api/carts", headers=headers, data=json.dumps(cart))

    assert response.status_code == 200, f"{response.content}"

    print("create a cart")

    cart = response.json()

    pprint.pprint(cart)

    response = requests.get(f"http://localhost:8080/carts/api/carts/{cart['id']}")

    assert response.status_code == 200, f"{response.content}"

    print("query the created cart")

    cart2 = response.json()

    pprint.pprint(cart2)

    assert str(cart) == str(cart2), f"{cart}, {cart2}"

    cart = cart2

    # add some item
    item = {
        "amount": 2,
        "product": product2
    }

    response = requests.post(f"http://localhost:8080/carts/api/carts/{cart['id']}",
                             headers=headers, data=json.dumps(item))

    assert response.status_code == 200, f"{response.content}"

    print("add some items")

    cart = response.json()

    pprint.pprint(cart)

    total = product1['price'] + product2['price'] * 2

    response = requests.get(f"http://localhost:8080/carts/api/carts/{cart['id']}/total")

    assert response.status_code == 200, f"{response.content}"

    assert total == float(response.text), f"{total}, {response.text}"

    print(f"total: {total}")

    response = requests.post("http://localhost:8080/orders/api/orders", headers=headers, data=json.dumps(cart))

    assert response.status_code == 200, f"{response.content}"

    order = response.json()

    print("create a order")

    pprint.pprint(order)

    # check waybill

    response = requests.get("http://localhost:8080/waybills/api/waybills")

    assert response.status_code == 200, f"{response.content}"

    waybills = response.json()

    pprint.pprint(waybills)

    assert any(waybill['order_id'] == order['id'] for waybill in waybills), waybills
