from behave import given, use_step_matcher
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
use_step_matcher("re")


@given(u'I navigate to the kayak main page')
def visit_login(context):
    return context.browser.visit("")

@given('I open the main navigation menu')
def step_impl(context):
    menu_button = context.browser.find_element(By.CLASS_NAME, "ZGw-")
    menu_button.click()