Feature: otp
	
	Examples: 
	    | phone    |resend_type|status|    message        |
	    |9080804360|  text     |True  |Successfully verified|
	    |9080804360|  voice    |False |Your OTP is Invalid|

	Scenario Outline: Login via OTP
	    Given Generating OTP for the given mobile number: <phone> <otp_type>
	    And the customer requests a resend via <resend_type>
	    When the user enter the OTP <status> then the message should be <message>
	    Then LogIn the user

	    Examples: 
	    | otp_type|
	    |	LOGIN |
	    

	Scenario Outline: forgot password
	    Given Generating OTP for the given mobile number: <phone> <otp_type>
	    And the customer requests a resend via <resend_type>
	    When the user enter the OTP <status> then the message should be <message>
	    Then forgot a password

	    Examples: 
	    | otp_type |
	    |	FORGOT |

