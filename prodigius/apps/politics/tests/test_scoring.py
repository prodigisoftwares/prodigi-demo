from django.test import TestCase

# If your module path differs, update the import below.
from ..utils import Q_AXIS, compute_coords, score_answer


class ScoreAnswerTests(TestCase):
    def test_x_axis_rules(self):
        # X-axis standard rule: A -> -weight, B -> +weight, other -> 0
        w1 = Q_AXIS[1][1]
        self.assertAlmostEqual(score_answer(1, "A"), -1.0 * w1)
        self.assertAlmostEqual(score_answer(1, "B"), 1.0 * w1)
        self.assertAlmostEqual(score_answer(1, "C"), 0.0)

        w5 = Q_AXIS[5][1]
        self.assertAlmostEqual(score_answer(5, "A"), -1.0 * w5)
        self.assertAlmostEqual(score_answer(5, "B"), 1.0 * w5)
        self.assertAlmostEqual(score_answer(5, "Both"), 0.0)

    def test_y_axis_special_q3_q6(self):
        # q3 & q6: A=+1, B=-1, Both=0.3, other=0 (times weight)
        for qnum in (3, 6):
            _, w = Q_AXIS[qnum]
            self.assertAlmostEqual(score_answer(qnum, "A"), 1.0 * w)
            self.assertAlmostEqual(score_answer(qnum, "B"), -1.0 * w)
            self.assertAlmostEqual(score_answer(qnum, "Both"), 0.3 * w)
            self.assertAlmostEqual(score_answer(qnum, "C"), 0.0)

    def test_y_axis_special_q8(self):
        # q8: A=0.6, B=0.6, Both=1.0, other=0 (times weight)
        qnum = 8
        _, w = Q_AXIS[qnum]
        self.assertAlmostEqual(score_answer(qnum, "A"), 0.6 * w)
        self.assertAlmostEqual(score_answer(qnum, "B"), 0.6 * w)
        self.assertAlmostEqual(score_answer(qnum, "Both"), 1.0 * w)
        self.assertAlmostEqual(score_answer(qnum, "C"), 0.0)


class ScoreAnswerDefaultYTests(TestCase):
    def test_y_axis_default_branch(self):
        # Create a fake Y-axis entry not in (3, 6, 8)
        Q_AXIS[99] = ("y", 2.0)  # test-only injection
        try:
            self.assertAlmostEqual(score_answer(99, "A"), 2.0)
            self.assertAlmostEqual(score_answer(99, "B"), -2.0)
            self.assertAlmostEqual(score_answer(99, "Both"), 0.6)
            self.assertAlmostEqual(score_answer(99, "C"), 0.0)
        finally:
            # Clean up to avoid side effects on other tests
            Q_AXIS.pop(99, None)


class ComputeCoordsTests(TestCase):
    def test_all_A(self):
        """
        X-axis (q1,2,4,5,7): each A => -weight => average -1.0
        Y-axis:
          q3 A -> +1.0*1.0 = 1.0
          q6 A -> +1.0*0.8 = 0.8
          q8 A -> 0.6*0.8  = 0.48
        y_total = 2.28, y_weight = 2.6 -> y ≈ 0.8769230769
        """
        answers = {f"q{i}": "A" for i in range(1, 9)}
        x, y = compute_coords(answers)
        self.assertAlmostEqual(x, -1.0)
        self.assertAlmostEqual(y, 2.28 / 2.6)

    def test_all_B(self):
        """
        X-axis average +1.0
        Y-axis:
          q3 B -> -1.0*1.0 = -1.0
          q6 B -> -1.0*0.8 = -0.8
          q8 B -> 0.6*0.8  = +0.48
        y_total = -1.32, y_weight = 2.6 -> y ≈ -0.5076923077
        """
        answers = {f"q{i}": "B" for i in range(1, 9)}
        x, y = compute_coords(answers)
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, -1.32 / 2.6)

    def test_partial_and_unknown_choices(self):
        """
        Only q5='B' (X, w=0.8): x_total=+0.8, x_weight=0.8
        q3='Both' (Y, w=1.0): y_total=0.3, y_weight=1.0
        q1='C' (unknown on X): delta=0.0 but weight 1.0 still counted.
        Final X = (0.8 + 0.0) / (0.8 + 1.0) = 0.8 / 1.8 ≈ 0.444444...
        """
        answers = {"q5": "B", "q3": "Both", "q1": "C"}
        x, y = compute_coords(answers)
        self.assertAlmostEqual(x, 0.8 / (0.8 + 1.0))
        self.assertAlmostEqual(y, 0.3)  # 0.3 / 1.0

    def test_skips_unanswered(self):
        """
        Only q6='A' answered on Y.
          y_total = 0.8, y_weight = 0.8 -> y = 1.0
          x = 0.0 (no X answers)
        """
        answers = {"q6": "A"}
        x, y = compute_coords(answers)
        self.assertAlmostEqual(x, 0.0)
        self.assertAlmostEqual(y, 1.0)

    def test_clamped_to_unit_interval(self):
        """
        Averages are clamped to [-1.0, 1.0].
        """
        answers = {
            "q1": "B",
            "q2": "B",
            "q4": "B",
            "q5": "B",
            "q7": "B",  # push X high
            "q3": "A",
            "q6": "A",
            "q8": "Both",  # push Y high
        }
        x, y = compute_coords(answers)
        self.assertGreaterEqual(x, -1.0)
        self.assertLessEqual(x, 1.0)
        self.assertGreaterEqual(y, -1.0)
        self.assertLessEqual(y, 1.0)
        # Specifically:
        self.assertAlmostEqual(x, 1.0)
        self.assertAlmostEqual(y, 1.0)  # 2.6 / 2.6 == 1.0
