Feature: Driver completes the order

    Scenario: Driver sucessfully completes the order
        Given A customer places an order
        And Fetch related order by <store_id>
        And a driver is assigned to the order
        When the driver completes the order
        Then the order should be completed

        Examples: 
	    | store_id|
	    |	 7    |