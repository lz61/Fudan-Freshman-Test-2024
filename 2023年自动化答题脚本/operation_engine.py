from selenium.webdriver.remote.webdriver import WebDriver, WebElement


def take_exam(driver: WebDriver):
    driver.find_element_by_id("take_quiz_link").click()


def submit_exam(driver: WebDriver):
    driver.find_element_by_id("submit_quiz_button").click()
    alert = driver.switch_to.alert
    alert.accept()


def goto_next_question(driver: WebDriver):
    target = driver.find_elements_by_class_name("next-question")
    if len(target) == 0:
        return None
    target[0].click()
    return True


def generate_answer(driver: WebDriver):
    take_exam(driver)
    submit_exam(driver)
