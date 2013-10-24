"""This module will test the containers module"""
from nose.tools import raises
from veloview.analysis.containers import RootGraphic, Combiner
from veloview.analysis.score_manipulation import Score, Weight
from veloview.core.errors.exceptions import CombinerWeightAssignmentException

score1 = 65
score2 = 80
score3 = 99

weight1 = 0.4
weight2 = 0.5
weight3 = 0.1

r1 = RootGraphic(None, Score(score1), Weight(weight1))
r2 = RootGraphic(None, Score(score2), Weight(weight2))
r3 = RootGraphic(None, Score(score3), Weight(weight3))
c1 = Combiner(Weight(weight2), r1, r2)


def test_combainer_init():
    assert len(c1.elements) == 2
    assert c1.score == r1.score * r1.weight + r2.score * r2.weight

def test_combainer_append_calc():
    c3 = c1
    c3.append(r3)
    assert len(c3.elements) == 3
    assert c3.score == r1.score * r1.weight + r2.score * r2.weight + r3.score * r3.weight


@raises(CombinerWeightAssignmentException)
def test_combiner_weight_assignment():
    c1 = Combiner(weight2, r1)