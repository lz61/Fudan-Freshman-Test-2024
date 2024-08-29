import json
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from cookie_engine import get_cookies, load_cookies, driver_get_with_cookies
from environment import driver_path, main_page, cookie_path, auth_url, if_load_cookie, question_path, \
    if_add_question
from operation_engine import take_exam, submit_exam, generate_answer
from question import Question
from question_engine import get_questions_answers, question_list_to_dict, question_list_merge, answer_question, \
    answer_all_questions, load_question_list, save_question_list

driver = driver_get_with_cookies(main_page, cookie_path)
try:
    question_list = load_question_list(question_path)
    question_dict = question_list_to_dict(question_list)

    print("-------------------开始答题------------------")
    take_exam(driver)
    answer_all_questions(driver, question_dict)

    time.sleep(10)
finally:
    driver.quit()
