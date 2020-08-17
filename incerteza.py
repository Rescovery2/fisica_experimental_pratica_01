import sympy


def aplicar_funcao(func, **var):
    variaveis = var.keys()
    valores = var.values()
    melhores_estimativas = []
    incertezas = []

    try:
        melhores_estimativas = [erro.x for erro in valores]
        incertezas = [erro.delta_x for erro in valores]
    except AttributeError:
        for erro in valores:
            if isinstance(erro, int) or isinstance(erro, float):
                erro = Erro(erro, 0)

            melhores_estimativas.append(erro.x)
            incertezas.append(erro.delta_x)

    if isinstance(func, sympy.core.Expr):
        subs_melhor_estimativa = []

        for i, v in enumerate(variaveis):
            variavel = v
            melhor_estimativa = melhores_estimativas[i]
            subs_melhor_estimativa.append((variavel, melhor_estimativa))

        melhor_estimativa = func.subs(subs_melhor_estimativa)
        incerteza = 0

        for i, v in enumerate(variaveis):
            variavel = v
            delta = incertezas[i]

            derivada_expr = sympy.diff(func, variavel)
            incerteza = incerteza + (derivada_expr.subs(subs_melhor_estimativa) * delta) ** 2

        incerteza = incerteza ** (1 / 2)

        return Erro(melhor_estimativa, incerteza)


class Erro(object):
    def __init__(self, melhor_estimativa: float, incerteza: float):
        self.x, self.delta_x = melhor_estimativa, incerteza
        self.delta_x_percentual = 100 * incerteza / melhor_estimativa

    def __str__(self):
        return f'{self.x} +/- {self.delta_x}'

    def __add__(self, other):
        return self.soma(other=other)

    def __sub__(self, other):
        return self.subtracao(other=other)

    def __mul__(self, other):
        return self.multiplicacao(other=other)

    def __pow__(self, power, modulo=None):
        return self.potencia(n=power)

    def __round__(self, n: int):
        return self.arredondar(n=n)

    def __abs__(self):
        return f'{self.x} +/- {self.delta_x_percentual} %'

    def soma(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Erro(melhor_estimativa=other, incerteza=0)

        if isinstance(other, Erro):
            p, q = sympy.symbols('p q')
            return aplicar_funcao(func=p + q, p=self, q=other)

    def subtracao(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Erro(melhor_estimativa=other, incerteza=0)

        if isinstance(other, Erro):
            p, q = sympy.symbols('p q')
            return aplicar_funcao(func=p - q, p=self, q=other)

    def multiplicacao(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Erro(melhor_estimativa=other, incerteza=0)

        if isinstance(other, Erro):
            p, q = sympy.symbols('p q')
            return aplicar_funcao(func=p * q, p=self, q=other)

    def divisao(self, other):
        if isinstance(other, int) or isinstance(other, float):
            other = Erro(melhor_estimativa=other, incerteza=0)

        if isinstance(other, Erro):
            p, q = sympy.symbols('p q')
            return aplicar_funcao(func=p / q, p=self, q=other)

    def potencia(self, n: int):
        p = sympy.symbols('p')
        return aplicar_funcao(func=p ** n, p=self)

    def raiz_quadrada(self):
        p = sympy.symbols('p')
        return aplicar_funcao(func=p ** (1 / 2), p=self)

    def raiz_cubica(self):
        p = sympy.symbols('p')
        return aplicar_funcao(func=p ** (1 / 3), p=self)

    def raiz_enesima(self, n: int):
        p = sympy.symbols('p')
        return aplicar_funcao(func=p ** (1 / n), p=self)

    def arredondar(self, n: int):
        self.x = round(self.x, n)
        self.delta_x = round(self.delta_x, n)
        return self
