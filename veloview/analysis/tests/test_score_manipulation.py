"""This module will test the scores_manipulation module"""
from nose.tools import raises

from veloview.analysis.score_manipulation import Weight, Score
from veloview.core.errors.exceptions import ScoreAssignmentException, AddingScoreException, MultiplyingScoreException, \
    WeightAssignmentException

score_for_check = 93
score_for_check1 = 25
score_for_check2 = 70
weight_for_check = 0.3
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
    weight1 = Weight(weight_for_check)
    score1 = score1 * weight1

    assert score1 == score_for_comparison


def test_score_cmp():
    score1 = Score(score_for_check)

    score_thesame = Score(score_for_check)
    score_lower = Score(score_for_check - 1)
    score_higher = Score(score_for_check + 1)

    assert score1 == score_thesame
    assert score1 > score_lower
    assert score1 < score_higher


def test_weight_init():
    weight1 = Weight(weight_for_check)
    string_for_check = "{}/1.0".format(weight_for_check)

    assert weight1.value == weight_for_check
    assert str(weight1) == string_for_check


@raises(ScoreAssignmentException)
def test_score_assignment():
    score1 = Score(score_for_check_exc)


@raises(AddingScoreException)
def test_score_adding():
    score1 = Score(score_for_check) + Score(score_for_check1)


@raises(MultiplyingScoreException)
def test_score_multiplying():
    score1 = Score(score_for_check) * 0.5


@raises(WeightAssignmentException)
def test_weight_assignment():
    weight1 = Weight(2)