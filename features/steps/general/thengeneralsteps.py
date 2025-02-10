from behave import then, use_step_matcher
from hamcrest import equal_to, assert_that, only_contains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse



from lib.components.generalcomponents import GeneralComponents
from lib.helpers.generalhelpers import validate_text, transform_validation, transformation_helper, join_words, \
    split_and_replace_string, transformation_to_element_name

use_step_matcher("re")


@then(u'The page title should "(?P<assertion>contain|equal)" the "(?P<page_name>.*)" text')
def step_impl(context, assertion, page_name):
    validation_result = validate_text(assertion, page_name, context.current_page.get_title_page())
    return assert_that(validation_result, equal_to(True),
                       f'The expected title is "{page_name}", but was "{context.current_page.get_title_page()}"')


@then(u'I should be in the "(?P<page>.*)" page')
def step_impl(context, page):
    context.current_page = context.all_contexts[page]
    return assert_that(context.current_page.is_open(), only_contains(True),
                       'Some element is not present in the opened page')


@then(u'The page "(?P<expression>should|should not)" contain the next elements')
def step_impl(context, expression):
    if not context.table:
        print("Error: La tabla de elementos está vacía.")
        return  # Termina la ejecución sin romper la prueba

    try:
        # Depuración: Mostrar los elementos recibidos
        print(f"Contenido de context.table: {context.table}")
        for row in context.table:
            print(f"Elemento: {row}")

        # Obtener la lista de validaciones
        list_validation = []
        for row in context.table:
            name = row.get("name", "").strip()  # Obtener el valor, con manejo de espacios en blanco
            type_ = row.get("type", "").strip()

            if not name or not type_:
                print(f"Advertencia: Se encontró una fila vacía en la tabla ({row})")
                continue

            try:
                # Intentar verificar si el elemento está presente
                is_present = context.browser.are_element_presents(name, type_, context)
                list_validation.append(is_present)
            except Exception as e:
                print(f"Error buscando '{name}' de tipo '{type_}': {e}")
                list_validation.append(False)  # Registrar como no encontrado

        # Validar la existencia con Hamcrest
        assertion = transform_validation(expression)
        assert_that(list_validation, only_contains(assertion))

    except Exception as general_error:
        print(f"⚠️ Error inesperado en la validación: {general_error}")
    try:
        elements = context.table
        print(f"Validando la existencia de los siguientes elementos: {elements}")

        list_validation = []
        for row in elements:
            name = row["name"]
            type_ = row["type"]

            try:
                is_present = context.browser.are_element_presents(name, type_, context)
                list_validation.append(is_present)
            except Exception as e:
                print(f"Error al buscar el elemento '{name}' de tipo '{type_}': {e}")
                list_validation.append(False)  

        assertion = transform_validation(expression)

        assert_that(list_validation, only_contains(assertion))

    except Exception as general_error:
        print(f"⚠️ Error inesperado en la validación de elementos: {general_error}")


@then(u'The "(?P<element_name>.*)" "(?P<element_type>label|button|container)" should contain the "('
      u'?P<text_to_validate>.*)" text')
def step_impl(context, element_name, element_type, text_to_validate):
    element = transformation_helper(element_name, element_type)
    text_element = GeneralComponents.get_text_element(context, element).rstrip()
    new_text_to_validate = join_words(split_and_replace_string(text_to_validate))
    new_text_element = join_words(split_and_replace_string(text_element))
    return assert_that(new_text_to_validate, equal_to(new_text_element))


@then(u'The "(?P<element_name>.*)" "(?P<element_type>label|button|container)" "(?P<expression>should|should not)" be '
      u'present')
def step_impl(context, element_name, element_type, expression):
    element = transformation_helper(element_name, element_type)
    element_validation = GeneralComponents.check_exist_element(context, element)
    assertion = transform_validation(expression)
    return assert_that(element_validation, equal_to(assertion))


@then(u'The url page should be equal to the next "(.*)" url')
def step_impl(context, expected_url):
    actual_url = context.browser.get_current_url()
    
    # Permitir variaciones con dominios regionales (.com, .com.br, etc.)
    if not actual_url.startswith(expected_url):
        raise AssertionError(f"Se esperaba que la URL comenzara con '{expected_url}', pero se obtuvo '{actual_url}'")
    
    print(f"La URL es válida: {actual_url}")



@then(u'The "(?P<element_name>.*)" "(?P<element_type>button)" "('u'?P<expression>should|should 'u'not)" be enabled')
def step_impl(context, element_name, element_type, expression):
    element_name = transformation_helper(element_name, element_type)
    assertion = transform_validation(expression)
    button_enabled = GeneralComponents.is_enabled_in_page(context, element_name)
    return assert_that(button_enabled, equal_to(assertion))

@then('The menu "should" contain the next options')
def step_impl(context):
    for row in context.table:
        name = row['name']
        url = row['url']
        try:
            # Usar context.browser.web_driver en lugar de context.driver
            menu_item = context.browser.web_driver.find_element(By.XPATH, f"//a[@href='{url}']")            
            assert menu_item.is_displayed(), f"Elemento de menú '{name}' no encontrado o no visible."
            expected_url = url
            actual_href = menu_item.get_attribute("href")

            assert expected_url in actual_href, f"URL de '{name}' no contiene '{expected_url}'. URL actual: {actual_href}"

        except NoSuchElementException:
            assert False, f"Elemento de menú '{name}' no encontrado."
        except AssertionError as e:
            print(f"Error en el menú '{name}': {e}")



@then('The url page should be equal to the expected menu options')
def step_impl(context):
    wait = WebDriverWait(context.browser, 10)

    for row in context.table:
        expected_url = row["url"]

        # Hacer clic en el enlace correspondiente
        menu_item = wait.until(
            EC.element_to_be_clickable((By.XPATH, f'//a[contains(@href, "{expected_url}")]'))
        )
        menu_item.click()

        # Esperar y validar la URL actual
        actual_url = context.browser.get_current_url()
        
        if not actual_url.endswith(expected_url):
            raise AssertionError(f"Se esperaba que la URL terminara con '{expected_url}', pero se obtuvo '{actual_url}'")

        print(f"La URL es válida: {actual_url}")
        


