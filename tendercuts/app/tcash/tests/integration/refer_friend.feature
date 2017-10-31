Feature: Refer a friend

    Scenario: Refer a friend
        Given A new user signs up via referal link
        And logs into his account
        And is referred by an existing user
        And the new user get 100 in his account
        When the new user places an order
        Then the referee get 100 in his account
