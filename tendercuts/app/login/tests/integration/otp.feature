Feature: otp
	
	Examples: 
	    | phone    |resend_type|status|    message        |
	    |8973111017|  text     |True  |succesfuly verified|
	    |8973111017|  voice    |False |Your OTP is Invalid|

	Scenario Outline: Login via OTP
	    Given Generating OTP for the given otp type and mobile number <otp_type><phone>
	    And Resend otp for text and voice method <otp_type><phone><resend_type>
	    When Validating the user entered OTP <otp_type><phone><status><message>
	    Then LogIn the user

	    Examples: 
	    | otp_type|
	    |	LOGIN |
	    

	Scenario Outline: forgot password
	    Given Generating OTP for the given otp type and mobile number <otp_type><phone>
	    And Resend otp for text and voice method <otp_type><phone><resend_type>
	    When Validating the user entered OTP <otp_type><phone><status><message>
	    Then forgot a password <phone><otp_type>

	    Examples: 
	    | otp_type |
	    |	FORGOT |


