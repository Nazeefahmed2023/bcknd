from locust import HttpUser, task, between, tag
import random


# Replace these with real product IDs or fetch dynamically in on_start
PRODUCT_IDS = [1,2,3,4,5]


class Shopper(HttpUser):
    wait_time = between(0.5, 2)


def on_start(self):
# optional: attach a pre-created JWT
    token = None
    if token:
        self.client.headers.update({"Authorization": f"Bearer {token}"})


@task(4)
@tag("browse")
def browse_products(self):
    self.client.get("/api/products/?page=1")


@task(2)
@tag("search")
def search(self):
    q = random.choice(["rice","milk","oil","dal","sugar"])
    self.client.get(f"/api/search/?q={q}")


@task(2)
@tag("cart")
def add_to_cart(self):
    pid = random.choice(PRODUCT_IDS)
    self.client.post("/api/cart/add/", json={"product_id": pid, "quantity": 1})


@task(1)
@tag("checkout")
def checkout(self):
    resp = self.client.post("/api/checkout/", json={"address_id": 1}, catch_response=True)
    if resp.status_code == 200:
        order_id = resp.json().get("order_id")
    if order_id:
        self.client.post("/api/payments/create/", json={"order_id": order_id})