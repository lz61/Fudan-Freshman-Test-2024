import os

from cookie_engine import driver_get_with_cookies
from environment import if_add_question, question_path, main_page, cookie_path
from operation_engine import generate_answer
from question_engine import load_question_list, get_questions_answers, question_list_merge, save_question_list

if __name__ == "__main__":
    driver = driver_get_with_cookies(main_page, cookie_path)
    try:
        print("-------------------开始获得答案信息------------------")
        question_list_old = []
        if os.path.exists(question_path) and if_add_question:
            question_list_old = load_question_list(question_path)

        generate_answer(driver)
        question_list = get_questions_answers(driver)
        question_list_merge(question_list, question_list_old)
        save_question_list(question_list, question_path)
    finally:
        driver.quit()
