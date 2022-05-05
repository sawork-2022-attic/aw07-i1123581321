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

    product1 = random.choice(products)
    product2 = random.choice(products)

    pprint.pprint(product1)

    pprint.pprint(product2)

    cart = {
        "id": 42,
        "items": [
            {
                "id": 1,
                "amount": 1,
                "product": product1
            }
        ]
    }

    # create a cart
    response = requests.post("http://localhost:8080/carts/api/carts", headers=headers, data=json.dumps(cart))

    assert response.status_code == 200, f"{response.content}"

    cart = response.json()

    response = requests.get(f"http://localhost:8080/carts/api/carts/{cart['id']}")

    assert response.status_code == 200, f"{response.content}"

    cart2 = response.json()

    assert str(cart) == str(cart2), f"{cart}, {cart2}"

    # add some item
    item = {
        "id": 2,
        "amount": 2,
        "product": product2
    }

    response = requests.post(f"http://localhost:8080/carts/api/carts/{cart['id']}",
                             headers=headers, data=json.dumps(item))

    assert response.status_code == 200, f"{response.content}"

    total = product1['price'] + product2['price'] * 2

    response = requests.get(f"http://localhost:8080/carts/api/carts/{cart['id']}/total")

    assert response.status_code == 200, f"{response.content}"

    assert total == float(response.text), f"{total}, {response.text}"
