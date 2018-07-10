Feature: Driver completes the order

    Scenario: Driver sucessfully completes the order
        Given A customer places an order
        And Rating Tag creation
        And Fetch all rating Tags
        And a customer create a rating <comments>
        Then find the no of driver stat objects
        
        Examples: 
	   |comments |
	   |product is bad|