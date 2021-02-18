from sympy import *
from matplotlib import pyplot as plt
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

    def engel_curves(self):
        budget = self.Px * self.x + self.Py * self.y - symbols("I")
        x, y = solve(self.mrs_xy - self.Px / self.Py, self.x)[0], solve(self.mrs_xy - self.Px / self.Py, self.y)[0]
        return solve(budget.subs(self.y, y), dict=True)[0], solve(budget.subs(self.x, x), dict=True)[0]

    def demand_curves(self):
        budget = symbols("Px") * self.x + self.Py * self.y - self.income
        demand_x = solve([self.mrs_xy - symbols("Px") / self.Py, budget], dict=True)[0]
        budget = self.Px * self.x + symbols("Py") * self.y - self.income
        demand_y = solve([self.mrs_xy - self.Px / symbols("Py"), budget], dict=True)[0]
        return demand_x, demand_y

    def income_consumption_curve(self):
        engel_x, engel_y = self.engel_curves()
        return solve(engel_x[symbols("I")] - engel_y[symbols("I")], self.y)[0]

    def show_plots(self):
        budget = lambdify(self.x, solve(self.Px * self.x + self.Py * self.y - self.income, self.y)[0], "numpy")
        xy_optimum = self.optimum_point()
        expr_u = solve(parse_expr(self.utility).subs(list(xy_optimum.items())) - parse_expr(self.utility), self.y)[-1]
        utility = lambdify(self.x, expr_u, "numpy")
        x = np.linspace(0.1, self.income / self.Px, 1000)
        y = np.linspace(0.1, self.income / self.Py, 1000)

        fig, axs = plt.subplots(nrows=5, ncols=1, figsize=(5, 20))
        axs[0].axis(ymin=0, ymax=self.income / self.Py, xmin=0, xmax=self.income / self.Px)
        axs[0].set_title("Consumer optimum")
        axs[0].plot(x, utility(x))
        axs[0].plot(x, budget(x))
        axs[0].scatter(xy_optimum[self.x], xy_optimum[self.y], color='red')
        axs[0].set_xlabel("Product X")
        axs[0].set_ylabel("Product Y")

        income = np.linspace(0, self.income * 2, 1000)
        engel = self.engel_curves()
        income_x = lambdify(self.x, engel[0][symbols("I")], "numpy")
        income_y = lambdify(self.y, engel[1][symbols("I")], "numpy")
        axs[1].axis(ymin=0, xmin=0, xmax=max(income_x(income)), ymax=max(income))
        axs[1].set_title("Engel curve for product X")
        axs[1].plot(income_x(income), income, color="green")
        axs[1].set_xlabel("Income I")
        axs[1].set_ylabel("Product X")
        axs[2].axis(ymin=0, xmin=0, xmax=max(income_y(income)), ymax=max(income))
        axs[2].set_title("Engel curve for product Y")
        axs[2].plot(income_y(income), income, color="gold")
        axs[2].set_xlabel("Income I")
        axs[2].set_ylabel("Product Y")

        demand_xy = self.demand_curves()
        demand_x, demand_y = lambdify(self.x, demand_xy[0][symbols("Px")], "numpy"), lambdify(self.y, demand_xy[1][
            symbols("Py")], "numpy")
        axs[3].axis(ymin=0, xmin=0, ymax=max(demand_x(x)), xmax=max(x))
        axs[3].set_title("Product demand  X")
        axs[3].plot(x, demand_x(x), color="purple")
        axs[3].set_xlabel("Product X")
        axs[3].set_ylabel("Price X")
        axs[4].axis(ymin=0, xmin=0, ymax=max(demand_y(y)), xmax=max(y))
        axs[4].set_title("Product demand  Y")
        axs[4].plot(y, demand_y(y), color="red")
        axs[4].set_xlabel("Product Y")
        axs[4].set_ylabel("Price Y")

        fig.tight_layout()
        plt.show()


def main():
    problem = Problem(utility="x*y**4", Px=1, Py=4, income=40)
    problem.show_plots()


if __name__ == "__main__":
    main()
