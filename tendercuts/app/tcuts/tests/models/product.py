import app.tcuts.models as models

def test_product_fetch():
    store = models.ProductStore()
    product = store.get_store_product()

    assert product[0] is not None
