"""This module will test the containers module"""
from nose.tools import raises
from veloview.analysis.containers import RootGraphic, Combiner
from veloview.analysis.score_manipulation import Score
from veloview.core.errors.exceptions import RootGraphicListArgumentException

score1 = 65
score2 = 80
score3 = 99

weight1 = 0.4
weight2 = 0.5
weight3 = 0.1

r1 = RootGraphic("r1", None, Score(score1), [], [])
r2 = RootGraphic("r2", None, Score(score2), [], [])
r3 = RootGraphic("r3", None, Score(score3), [], [])
c1 = Combiner("c1", r1, r2)
c2 = Combiner("c2", r1)


def test_combainer_init():
    assert len(c1.elements) == 2
    #assert c1.score == r1.score * r1.weight + r2.score * r2.weight  # TODO move to calculate test


def test_combainer_append_calc():
    c3 = c1
    c3.append(r3)
    assert len(c3.elements) == 3
    #assert c3.score == r1.score * r1.weight + r2.score * r2.weight + r3.score * r3.weight  # TODO move to calculate test


@raises(RootGraphicListArgumentException)
def test_combiner_list_arg_assignment():
    r1 = RootGraphic("r1", None, Score(score1), "warning", "error")