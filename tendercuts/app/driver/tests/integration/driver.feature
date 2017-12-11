Feature: Driver completes the order

    Scenario: Driver sucessfully completes the order
        Given A customer places an order
        And Fetch related order by <store_id>
        And a driver is assigned to the order and the driver location for <latitude><longitude>
        When a update driver current locations for <latitude> and <longitude> <status> <message>

        Then the order should be completed and the driver location for <latitude><longitude>

        Examples: 
	    | store_id|latitude |longitude|status|message|
	    |	 7    |12.965365|80.246106|True  |driver location updated successfully|

	Scenario: Create the driver trip and completes it successfully
        Given A customer places an order
        And Fetch related order by <store_id>
        And a driver is assigned to the order and the driver location for <latitude><longitude>
        And create a driver trip
        Then complete a driver trip

        Examples:
	    | store_id|latitude |longitude|
	    |	 7    |12.965365|80.246106|


