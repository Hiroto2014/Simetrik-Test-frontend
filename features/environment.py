from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from lib.pages.basepage import BasePage
from lib.pages.homepage import HomePage


def before_all(context):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")

    driver = set_selenium_driver(context)
    driver.set_page_load_timeout(30)
    driver.maximize_window()

    context.web_driver = driver
    context.browser = BasePage(context)
    context.home = HomePage(context)

    context.all_contexts = {
        'home': context.home,
    }


def after_scenario(context, scenario):
    steps = [str(step).replace('<', '').replace('>', '').capitalize() for step in scenario.steps]
    
    if test_rail_report(context) == 'True':
        validate_scenario(scenario, context, "\n".join(steps))


def after_all(context):
    if hasattr(context, "browser") and context.browser:
        context.web_driver.quit()
    print("===== That's all folks =====")


def after_step(context, step):
    if step.exception is not None:
        context.step_error = step.exception
        context.failed_step = step.name
    if step.status == 'failed':
        context.failed_step = step.name


def validate_scenario(scenario, context, steps):
    if scenario.status.name == 'failed':
        print('Failed Step: ' + context.failed_step + '\n' + str(context.step_error))


def set_selenium_driver(context):
    env = context.config.userdata["driver"]
    if env == 'aws':
        return set_docker_driver()
    return set_local_driver()


def set_local_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument("--lang=en-US")
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())  # ✅ Se usa Service correctamente
    return webdriver.Chrome(service=service, options=chrome_options)


def set_docker_driver() -> webdriver:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.set_capability('--lang', 'en-GB')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option('useAutomationExtension', False)

    return webdriver.Remote(
        command_executor='http://0.0.0.0:4444/wd/hub',
        options=chrome_options
    )


def test_rail_report(context):
    return context.config.userdata["testrail"]
