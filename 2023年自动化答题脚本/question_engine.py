import json
import time
from typing import List

from selenium.webdriver.remote.webdriver import WebDriver, WebElement

from operation_engine import goto_next_question, submit_exam
from question import Question


def get_questions_answers(browser: WebDriver) -> List[Question]:
    result = browser.find_elements_by_class_name("question_holder")
    question_list = []
    for question in result:
        question_text = question.find_elements_by_class_name("question_text")[0].text
        answers = []
        for answer in question.find_elements_by_class_name("answer_text"):
            answers.append(answer.text)
        correct_answers = question.find_elements_by_class_name("info")
        correct_ids = [correct.get_attribute("id").split("_")[1] for correct in correct_answers]
        correct_texts = [question.find_elements_by_xpath(f'//label[@for="answer-{correct_id}"]')[0].text for correct_id
                         in
                         correct_ids]
        # dic = {"stem": question_text, "answers": answers, "correct_answers": correct_texts}
        question_list.append(Question(question_text, answers, correct_texts))
        # question_list.append(Question.from_dict(dic))
        # print(f"question_text: {question_text}")
        # print(f"answers: {answers}")
        # print(f"correct_text: {correct_texts}")
    return question_list


def question_list_to_dict(question_list: List[Question]) -> dict:
    result = {}
    for question in question_list:
        if question.stem not in result:
            result[question.stem] = [question]
        else:
            result[question.stem].append(question)
    return result


def question_list_merge(a: List[Question], b: List[Question]):
    # merge to a
    a_set = question_list_to_dict(a)
    for question in b:
        flag = True
        if question.stem in a_set:
            for a_question in a_set[question.stem]:
                if question.equal(a_question):
                    flag = False
        if flag:
            a.append(question)


def answer_question(browser: WebDriver, question_dict: dict):
    stem = browser.find_elements_by_class_name("question_text")[0].text
    answers_element = browser.find_elements_by_class_name("answer_label")
    answers = [answer.text for answer in answers_element]
    cur_question = Question(stem=stem, answers=answers)
    find_question = None
    if cur_question.stem in question_dict:
        for question in question_dict[cur_question.stem]:
            if cur_question.equal(question):
                find_question = question
                break
    if find_question is None:
        return
    correct_answers_set = find_question.correct_answers_set
    for ele in answers_element:
        if ele.text in correct_answers_set:
            ele.click()


def answer_all_questions(browser: WebDriver, question_dict: dict):
    answer_question(browser, question_dict)
    while goto_next_question(browser) is not None:
        answer_question(browser, question_dict)
    time.sleep(5)
    submit_exam(browser)


def save_question_list(question_list: List[Question], path):
    with open(path, 'w') as f:
        f.write(json.dumps([question.to_dict() for question in question_list]))


def load_question_list(path):
    with open(path, 'r', encoding='utf8') as f:
        question_list_json = json.loads(f.read())
    return [Question.from_dict(question) for question in question_list_json]
