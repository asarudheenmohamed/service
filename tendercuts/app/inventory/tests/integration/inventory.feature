Feature: Inventory updated

	Scenario: Notify updated inventory
		Given Create notify object for <product1> and <product2>
		When The inventory is updated for <product1>, <product2>
		Then Notify customer object will set as notified

		Examples:
		| product1 | product2 |
		|    1,195 |  1,196   |
