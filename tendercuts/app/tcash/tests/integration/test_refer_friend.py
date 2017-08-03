from pytest_bdd import given, when, then, scenario

@scenario(
    'refer_friend.feature',
    'Successfully creating a product',
)
def test_outlined():
    pass


@given('I am a backoffice admin')
def start_cucumbers():
    assert 1 == 1

@when('I go to the New product page')
def eat_cucumbers():
    assert 1 == 1


@then('I should see a success message')
def should_have_left_cucumbers():
    assert 1 == 1