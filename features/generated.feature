Feature: Functional Testing of https://www.amazon.in/

  @happy_path
  Scenario: Successful Login Flow
    Given the user navigates to "https://www.amazon.in/"
    When the user enters "standard_user" into the "user-name" field
    And the user enters "secret_sauce" into the "password" field
    And clicks the "login-button" button
    Then the user should see "Products"

  @negative_path
  Scenario: Invalid Login Flow
    Given the user navigates to "https://www.amazon.in/"
    When the user enters "wrong_user" into the "user-name" field
    And clicks the "login-button" button
    Then the user should see "Epic sadface: Username and password do not match any user in this service"
