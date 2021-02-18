from sympy import *
import numpy as np


class Problem:
    x, y = symbols("x y")

    def __init__(self, utility, Px, Py, income):
        """
        :param utility: continuous function from 0 to infinity
        :param Px: price of good x
        :param Py: price of good y
        :param income: consumer income
        """
        self.income = income
        self.Px = Px
        self.Py = Py
        self.utility = utility

    @property
    def mrs_xy(self):
        return diff(parse_expr(self.utility), self.x) / diff(parse_expr(self.utility), self.y)

    def optimum_point(self):
        budget = self.Px * self.x + self.Py * self.y - self.income
        if self.mrs_xy.is_Number:
            if self.mrs_xy > self.Px / self.Py:
                return {self.x: self.income / self.Px, self.y: 0}
            else:
                return {self.x: 0, self.y: self.income / self.Py}
        optimum = solve([self.mrs_xy - self.Px / self.Py, budget], dict=True)[0]
        if optimum[self.x] < 0 or optimum[self.y] < 0:
            return {self.x: 0, self.y: self.income / self.Py} if optimum[self.x] < 0 \
                else {self.x: self.income / self.Px, self.y: 0}
        return optimum

    def income_consumption_curve(self, start_income, final_income):
        temp_income = self.income
        xys = []
        for income in np.arange(start_income, final_income, (final_income - start_income) / 100):
            self.income = income
            xys.append(self.optimum_point())
        self.income = temp_income
        return [xy[self.x] for xy in xys], [xy[self.y] for xy in xys]

    def engel_curve(self):
        self.income = symbols("I")
        budget = self.Px * self.x + self.Py * self.y - self.income
        x, y = solve(self.mrs_xy - self.Px / self.Py, self.x)[0], solve(self.mrs_xy - self.Px / self.Py, self.y)[0]
        return solve(budget.subs(self.y, y), self.x)[0], solve(budget.subs(self.x, x), self.y)[0]

    def price_consumption_curve(self, start_px, final_px):
        xys = []
        for price in np.arange(start_px, final_px, (final_px - start_px) / 100):
            self.Px = price
            xys.append(self.optimum_point())
        return [xy[self.x] for xy in xys], [xy[self.y] for xy in xys]

    def demand_curve(self, start_px, final_px):
        pass


def main():
    problem = Problem(utility="x*y", Px=2, Py=1, income=10)
    print(problem.price_consumption_curve(1, 10))


if __name__ == "__main__":
    main()
