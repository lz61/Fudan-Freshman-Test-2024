from typing import List
import json


class Question(object):
    def __init__(self, stem: str = "", answers=None, correct_answers=None):
        if correct_answers is None:
            correct_answers = []
        if answers is None:
            answers = []
        self.stem = stem
        self.answers = answers
        self.correct_answers = correct_answers
        self.answers_set = {answer for answer in answers}
        self.correct_answers_set = {correct for correct in correct_answers}

    def set_stem(self, stem):
        self.stem = stem

    def set_answers(self, answers):
        self.answers = answers
        self.answers_set = {answer for answer in answers}

    def set_correct_answers(self, correct_answers):
        self.correct_answers = correct_answers
        self.correct_answers_set = {correct for correct in correct_answers}

    def to_dict(self):
        return {"stem": self.stem, "answers": self.answers, "correct_answers": self.correct_answers}

    def equal(self, other):
        if self.stem != other.stem:
            return False
        # if len(self.answers) != len(other.answers) or len(self.correct_answers) != len(other.correct_answers):
        if len(self.answers) != len(other.answers):
            return False
        for item in other.answers:
            if item not in self.answers_set:
                return False
        # for item in other.correct_answers:
        #     if item not in self.correct_answers:
        #         return False
        return True

    @classmethod
    def from_dict(cls, dic):
        return cls(dic["stem"], dic["answers"], dic["correct_answers"])
