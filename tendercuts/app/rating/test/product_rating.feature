Feature: Driver completes the order

    Scenario: Customer review and rating for a product purchased
        Given A customer placed an order
        And Add a rating Tag creation
        And Fetch all rating Tags
        And A customer shares feedback for the product purchased on rating <comments><rating>
        Then Cross check review rating <comments>
        
        Examples: 
	   |comments      | rating |
	   |product is bad|  2     |