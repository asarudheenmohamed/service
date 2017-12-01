Feature: Inventory updated

	Scenario: Notify updated inventory
		Given Create notify object for store <store_id> and product <product_id>
		When Once the inventory updated customer will receive the SMS
		Then Notify customer object will set as notified

		Examples:
		| store_id | product_id |
		|    1     |    195     |
