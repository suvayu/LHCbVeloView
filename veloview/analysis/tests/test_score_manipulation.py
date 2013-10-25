"""This module will test the scores_manipulation module"""
from nose.tools import raises

from veloview.analysis.score_manipulation import Score
from veloview.core.errors.exceptions import ScoreAssignmentException, AddingScoreException

score_for_check = 93
score_for_check1 = 25
score_for_check2 = 70
weight_for_check = 0.3
weight_for_check1 = 1.0
score_for_check_exc = 101


def test_score_init():
    string_for_check = "{}%".format(score_for_check)

    tested_score = Score(score_for_check)

    assert tested_score.value == score_for_check
    assert str(tested_score) == string_for_check


def test_score_add():
    score_for_comparison = Score(score_for_check1 + score_for_check2)

    score1 = Score(score_for_check1)
    score2 = Score(score_for_check2)
    score3 = score1 + score2

    assert score3 == score_for_comparison


def test_score_iadd():
    score_for_comparison = Score(score_for_check1 + score_for_check2)
    score1 = Score(score_for_check1)
    score1 += Score(score_for_check2)

    assert score1 == score_for_comparison


def test_score_mul():
    score_for_comparison = Score(int(score_for_check * weight_for_check))
    score1 = Score(score_for_check)
    weight1 = weight_for_check
    score1 = score1 * weight1

    assert score1 == score_for_comparison


def test_score_imul():
    score_for_comparison = Score(int(score_for_check * weight_for_check))
    score1 = Score(score_for_check)
    weight1 = weight_for_check
    score1 *= weight1

    assert score1 == score_for_comparison


def test_score_div():
    score_for_comparison = Score(int(score_for_check / weight_for_check1))
    score1 = Score(score_for_check)
    weight1 = weight_for_check1
    score1 = score1 / weight1

    assert score1 == score_for_comparison


def test_score_idiv():
    score_for_comparison = Score(int(score_for_check / weight_for_check1))
    score1 = Score(score_for_check)
    weight1 = weight_for_check1
    score1 /= weight1

    assert score1 == score_for_comparison


def test_score_cmp():
    score1 = Score(score_for_check)

    score_thesame = Score(score_for_check)
    score_lower = Score(score_for_check - 1)
    score_higher = Score(score_for_check + 1)

    assert score1 == score_thesame
    assert score1 > score_lower
    assert score1 < score_higher


@raises(ScoreAssignmentException)
def test_score_assignment():
    score1 = Score(score_for_check_exc)


@raises(AddingScoreException)
def test_score_adding():
    score1 = Score(score_for_check) + Score(score_for_check1)