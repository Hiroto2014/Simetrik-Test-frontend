from behave import when, use_step_matcher
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from lib.components.generalcomponents import GeneralComponents
from lib.helpers.generalhelpers import transformation_helper

use_step_matcher("re")


@when(u'I click on the "(?P<element_name>.*)" "(?P<element_type>button|dropdown|option)"')
def step_impl(context, element_name, element_type):
    element_name = transformation_helper(element_name, element_type)
    if GeneralComponents.wait_until_element_is_clickable(
            context, context.current_page.webElements.__dict__.get(element_name)
    ):
        return context.browser.find_element(context.current_page.webElements.__dict__.get(element_name)).click()


@when(u'I navigate to the "(?P<url>.*)" URL')
def step_impl(context, url):
    return context.browser.visit(url)


@when('I select "(?P<option>.*)" in the dropdown')
def step_impl(context, option):
    return context.current_page.text_value_in_the_select(option)


@when(u'I search "(?P<option>.*)" in the input')
def step_impl(context, option):
    return context.current_page.text_value_in_the_filter(option)


@when('I open the main navigation menu')
def step_impl(context):
    
    driver = context.browser.web_driver  # Usa 'web_driver' en lugar de 'driver'

    wait = WebDriverWait(driver, 10)  # Espera hasta 10s
    menu_button = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//div[@role='button' and contains(@class, 'ZGw-')]"))
    )
    menu_button.click()

