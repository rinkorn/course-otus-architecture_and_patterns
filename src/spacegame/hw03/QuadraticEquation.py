EPS = 1e-7


class ParamAZeroError(Exception):
    pass


class ConvertToFloatError(Exception):
    pass


class QuadraticEquation:
    def __init__(self, a, b, c) -> None:
        self.a = a
        self.b = b
        self.c = c

    def solve(self) -> list:
        try:
            a = float(self.a)
            b = float(self.b)
            c = float(self.c)
        except:
            raise ConvertToFloatError

        discr = b**2 - 4 * a * c

        if abs(a) < EPS:
            raise ParamAZeroError

        roots = [None, None]
        if discr > EPS:
            roots[0] = (-b + (discr) ** 0.5) / (2 * a)
            roots[1] = (-b - (discr) ** 0.5) / (2 * a)
            roots.sort()
        elif abs(discr) < EPS:
            roots[0] = -b / (2 * a)
        return roots


if __name__ == "__main__":
    equation = QuadraticEquation(1, 2, 1.0000001)
    roots = equation.solve()
    print(f"Roots: {roots}")
