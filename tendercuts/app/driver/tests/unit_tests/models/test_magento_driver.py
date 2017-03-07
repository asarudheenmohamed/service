import app.driver.models as models

def test_fetch_driver():
    magento_user = models.DriverManagement.objects.filter(phone="9908765678")
    assert len(magento_user) == 1
    assert magento_user[0].name == "Tester1"
