Feature: Start a transaction with juspay

    Scenario: User starts a transaction via a new card
        Given User places an order
        And   Customer starts the transaction
        When  Customer pays succesfully
        Then  Transaction is successfull
        And   Card is saved

#    Scenario: User starts a transaction via a saved card
#        Given Payment modes should atleast by 1
#        And places an order
#        When the customer successfully starts payment via a saved card
#        Then the transaction is initiated
