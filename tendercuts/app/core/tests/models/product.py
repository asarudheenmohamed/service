import app.tcuts.models as models

def test_product_fetch():
    store = models.ProductStore()
    categries = store.get_store_product()

    assert categries is not None
    assert len(categries) == 7
