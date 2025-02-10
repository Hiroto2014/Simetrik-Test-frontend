@regression_tests

Feature: Validate element created dropdown column

  @navigate_home
  Scenario: Navigate to the Kayak home page and validate principal elements
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    And The page "should" contain the next elements
      | name                   | type   |
      | name_tag               | input  |
      | name_dropdown_column   | input  |
      | search_tag             | input  |
      | cancel                 | button |
      | create_column_disabled | button |

  @validate_url
  Scenario: Validate URL of Home page
    Given I navigate to the kayak main page
    Then I should be in the "home" page
    And The url page should be equal to the next "https://www.kayak.com" url

    Scenario Outline: Navigate between countries and validate the URL
      Given I navigate to the kayak main page
      Then I should be in the "home" page
      When I navigate to the "<url>" URL
      Then The url page should be equal to the next "<url>" url

    Examples:
      | url                       |
      | https://www.kayak.com.my/ |
      | https://www.kayak.com.pr/ |
      | https://www.kayak.com.br/ |

  @navigate_menu
  Scenario: Validate navigation menu functionality
    Given I navigate to the kayak main page
    When I open the main navigation menu
    Then The menu "should" contain the next options
      | name         | type   | url                  |
      | Flights      | link   | /flights             |
      | Hotels       | link   | /hotels              |
      | Cars         | link   | /cars                |
    Then The url page should be equal to the expected menu options
      | name         | type   | url                  |
      | Flights      | link   | /flights             |
      | Hotels       | link   | /hotels              |
      | Cars         | link   | /cars                |

