Feature: Driver completes the order

    Scenario: Driver sucessfully completes the order
        Given A customer places an order
        And Fetch related order by <store_id>
        And a driver is assigned to the order at <latitude><longitude>
        And a update driver current locations for <latitude> and <longitude> <status> <message>
        And check the driver's current location
        When the order should be completed and the driver location for <latitude><longitude>
        Then find the no of driver stat objects

        Examples: 
	    | store_id|latitude |longitude|status|message|
	    |	 7    |12.965365|80.246106|True  |driver location updated successfully|

    Scenario: Driver Update a order sequence number
        Given A customer places an order
        And Fetch related order by <store_id>
        And a driver is assigned to the order at <latitude><longitude>
        And B customer generate a new order and driver assigned the order at <latitude><longitude>
        Then driver update the sequence number for the B customer order

        Examples:
        |latitude |longitude|store_id |
        |12.965365|80.246106|7        |

    Scenario: Auto generated driver Trip
        Given A customer places an order
        And a store manager <assign> order for the driver
        And a driver get a current trip details <driver_order>
        And Fetch related order by <store_id>
        And a driver is assigned to the order at <latitude><longitude>
        And a driver start a trip
        And a update driver current locations for <latitude> and <longitude> <status> <message>
        And check the driver's current location
        When the order should be completed and the driver location for <latitude><longitude>
        Then find the no of driver stat objects

        Examples:
        | store_id|latitude |longitude|status|message                             |assign|driver_order|
        |    7    |12.965365|80.246106|True  |driver location updated successfully|True  |     1      |

    Scenario: Driver generate a trip
        Given A customer places an order
        And a driver create a driver trip <driver_order>
        And Fetch related order by <store_id>
        And a driver is assigned to the order at <latitude><longitude>
        Then check the driver current trip <assign> details

        Examples:
        | store_id|latitude |longitude|assign| driver_order |
        |    7    |12.965365|80.246106|False |     0        |