Feature: Inventory updates from flock

  Scenario: The request is approved by controller w/w/o initial inventory
    Given setup initial inventory for <product1> and <product2> if flag <is_initial_set>
    Given create <type> request for <product1> and <product2>
    When the inventory requests are approved
    Then inventory <type> should become live with <qty1> and <qty2>
    And inventory <type> should have logs with <qty1> and <qty2> with <is_initial_set>
    And verify user approved is set

  Examples:
  | product1         | product2          | qty1     | qty2     | type | is_initial_set |
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,1.65 | 196,1.10 | today| False |
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,1.65 | 196,1.10 | tomo| False |
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,1.65 | 196,1.10 | today| True |
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,1.65 | 196,1.10 | tomo| True |


  Scenario: The request is rejected by controller
    Given setup initial inventory for <product1> and <product2> if flag <is_initial_set>
    And create <type> request for <product1> and <product2>
    When the inventory requests are rejected
    Then inventory <type> should become live with <qty1> and <qty2>

  Examples:
  | product1         | product2          | qty1     | qty2     | type | is_initial_set|
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,100 | 196,100 | today| True|
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,100 | 196,100 | tomo| True|

  Scenario: The request is auto approved
    Given setup initial inventory for <product1> and <product2> if flag <is_initial_set>
    And create <type> request for <product1> and <product2>
    When the inventory requests are auto approved
    Then inventory <type> should become live with <qty1> and <qty2>
    And inventory <type> should have logs with <qty1> and <qty2> with <is_initial_set>

  Examples:
  | product1         | product2          | qty1     | qty2     | type | is_initial_set|
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,1.65 | 196,1.10 | today| True|
  |   195,CHK_SKU,3  |   196,CHK_SKU2,2  | 195,1.65 | 196,1.10 | tomo| True|
