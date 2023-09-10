EPS = 1e-7


class ParameterAZeroError(Exception):
    pass


class ConvertToFloatError(Exception):
    pass


class QuadraticEquation:
    def __init__(self, a: float, b: float, c: float) -> None:
        self.a = a
        self.b = b
        self.c = c

    def solve(self) -> list:
        try:
            a = float(self.a)
            b = float(self.b)
            c = float(self.c)
        except:  # noqa
            raise ConvertToFloatError

        discr = b**2 - 4 * a * c

        if abs(a) < EPS:
            raise ParameterAZeroError

        roots = []
        if discr > EPS:
            roots.append((-b + (discr) ** 0.5) / (2 * a))
            roots.append((-b - (discr) ** 0.5) / (2 * a))
            roots.sort()
        elif abs(discr) < EPS:
            roots.append(-b / (2 * a))
        return roots


if __name__ == "__main__":
    equation = QuadraticEquation(1.0, 2.0, 1.0000001)
    roots = equation.solve()
    print(f"Roots: {roots}")
