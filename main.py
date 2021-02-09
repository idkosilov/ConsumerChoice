from sympy import symbols, solve, lambdify, sqrt
import numpy as np
import matplotlib.pyplot as plt


def utility(x, y):
    return 2*sqrt(x) + y


def main():
    x, y = symbols("x y")
    income = 10
    price_x = 1
    price_y = 2
    budget_limit = income - (price_x * x + price_y * y)

    MRS_xy = utility(x, y).diff(x) / utility(x, y).diff(y)
    system = [MRS_xy - price_x / price_y, budget_limit]
    optimum_xy = solve(system, x, y)
    optimum_u = solve(utility(x, y).subs([(x, optimum_xy[0][0]), (y, optimum_xy[0][1])]) - utility(x, y), y)
    budget_line = solve(budget_limit, y)

    print(f"Оптимальный набор: x = {optimum_xy[0][0]}, y = {optimum_xy[0][1]}")
    print(f"Общая полезность: U = {utility(x, y).subs([(x, optimum_xy[0][0]), (y, optimum_xy[0][1])])}")

    xs = np.arange(0.1, optimum_xy[0][0]*2, 0.001, float)
    Income = lambdify(x, budget_line[0], "numpy")(xs)
    Utility = lambdify(x, optimum_u[0], "numpy")(xs)
    plt.xlabel('Количество товара X')
    plt.ylabel('Количество товара Y')
    plt.title('Равновесие потребительского выбора', fontsize=17)
    plt.plot(xs, Utility, label="Кривая безразличия")
    plt.plot(xs, Income, label="Бюджетное ограничение")
    plt.plot(optimum_xy[0][0], optimum_xy[0][1], "o", label="Точка равновесия")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
