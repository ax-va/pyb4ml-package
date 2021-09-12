from pyb4ml.modeling.factor_graph.factor import Factor
from pyb4ml.modeling.factor_graph.variable import Variable
from pyb4ml.models.factor_graphs.model import Model


class Student(Model):
    """
    The Student model [1, page 53]. See also "student.pdf" or "student.odp".

    [1] Daphne Koller and Nir Friedman, "Probabilistic Graphical Models:
    Principles and Techniques", MIT Press, 2009
    """
    def __init__(self):
        # Random variables
        self._difficulty = Variable(domain={'d0', 'd1'}, name='Difficulty')
        self._intelligence = Variable(domain={'i0', 'i1'}, name='Intelligence')
        self._grade = Variable(domain={'g0', 'g1', 'g2'}, name='Grade')
        self._sat = Variable(domain={'s0', 's1'}, name='SAT')
        self._letter = Variable(domain={'l0', 'l1'}, name='Letter')
        variables = (
            self._difficulty,
            self._intelligence,
            self._grade,
            self._sat,
            self._letter
        )

        # Conditional probability distributions (CPDs)
        self._cpd_difficulty = {
            'd0': 0.6,
            'd1': 0.4
        }
        self._cpd_intelligence = {
            'i0': 0.7,
            'i1': 0.3
        }
        self._cpd_grade = {
            ('d0', 'i0'): {'g0': 0.30, 'g1': 0.40, 'g2': 0.30},
            ('d0', 'i1'): {'g0': 0.90, 'g1': 0.08, 'g2': 0.02},
            ('d1', 'i0'): {'g0': 0.05, 'g1': 0.25, 'g2': 0.70},
            ('d1', 'i1'): {'g0': 0.50, 'g1': 0.30, 'g2': 0.20}
        }
        self._cpd_sat = {
            'i0': {'s0': 0.95, 's1': 0.05},
            'i1': {'s0': 0.20, 's1': 0.80}
        }
        self._cpd_letter = {
            'g0': {'l0': 0.10, 'l1': 0.90},
            'g1': {'l0': 0.40, 'l1': 0.60},
            'g2': {'l0': 0.99, 'l1': 0.01}
        }

        # Factors
        self._f0 = Factor(
            variables=(self._difficulty, ),
            function=self._f_cpd_difficulty,
            name='f0'
        )
        self._f1 = Factor(
            variables=(self._intelligence, ),
            function=self._f_cpd_intelligence,
            name='f1'
        )
        self._f2 = Factor(
            variables=(
                self._difficulty,
                self._intelligence,
                self._grade
            ),
            function=self._f_cpd_grade,
            name='f2'
        )
        self._f3 = Factor(
            variables=(
                self._intelligence,
                self._sat
            ),
            function=self._f_cpd_sat,
            name='f3'
        )
        self._f4 = Factor(
            variables=(
                self._grade,
                self._letter
            ),
            function=self._f_cpd_letter,
            name='f4'
        )
        factors = (
            self._f0,
            self._f1,
            self._f2,
            self._f3,
            self._f4
        )
        Model.__init__(self, factors, variables)

    # Factor functions
    def _f_cpd_difficulty(self, x):
        return self._cpd_difficulty[x]

    def _f_cpd_intelligence(self, x):
        return self._cpd_intelligence[x]

    def _f_cpd_grade(self, x, y, z):
        return self._cpd_grade[(x, y)][z]

    def _f_cpd_sat(self, x, y):
        return self._cpd_sat[x][y]

    def _f_cpd_letter(self, x, y):
        return self._cpd_letter[x][y]
