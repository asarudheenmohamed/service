Feature: Driver completes the order

    Scenario: Driver sucessfully completes the order
        Given A customer places an order
        And Fetch related order by <store_id>
        And a driver is assigned to the order and the driver location for <latitude><longitude>
        When a update driver current locations for <latitude> <longitude> <status> <message>
        Then the order should be completed and the driver location for <latitude><longitude>

        Examples: 
	    | store_id|latitude |longitude|status|message|
	    |	 7    |12.965365|80.246106|True  |driver location updated successfully|