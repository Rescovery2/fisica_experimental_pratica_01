from Mathematics.Mathematics_simulations import statistics
from Physics import incerteza
import matplotlib.pyplot as plt
import sympy
import scipy.stats
import numpy

# Determinação do erro das medidas
print('DETERMINAÇÃO DOS ERROS')

dict_dados_1 = {'VALOR (mm)': [7.2,
                               7.5,
                               7.8,
                               7.1,
                               7.4,
                               7.4,
                               7.6,
                               7.6,
                               7.5,
                               7.2,
                               ]}

dados_1 = statistics.DataSet(data=dict_dados_1)
erro = round(dados_1.get_sample_std_mean_deviation(column='VALOR (mm)'), 1)
media = dados_1.get_column_mean(column='VALOR (mm)')
desvio_padrao = dados_1.get_column_sample_std(column='VALOR (mm)')
desvios = dados_1.get_deviations(column='VALOR (mm)')
quadrado_desvios = [desvio ** 2 for desvio in desvios]

print(f'''
{dados_1}

Média = {media}
Desvio padrão amostral = {desvio_padrao}
Erro = {erro}
''')


# Parte principal do experimento
def espessura_unitaria_erro(dados: dict):
    quantidades = list(dados.values())[0]
    valores = list(dados.values())[1]
    espessuras = []

    for indice, quantidade in enumerate(quantidades):
        valor = valores[indice]
        n, l = sympy.symbols('n l')
        expr = l / n

        espessura = round(incerteza.aplicar_funcao(func=expr, n=quantidade, l=valor), 4)
        espessuras.append(espessura)

    return {'QUANTIDADE': quantidades,
            'VELOR MEDIDO (mm)': valores,
            'ESPESSURA (mm)': espessuras}


def espessura_unitaria(dados: dict):
    quantidades = list(dados.values())[0]
    valores = list(dados.values())[1]
    espessuras = []

    for indice, quantidade in enumerate(quantidades):
        valor = valores[indice].x
        espessura = valor / quantidade
        espessuras.append(espessura)

    return {'QUANTIDADE': quantidades,
            'VELOR MEDIDO (mm)': valores,
            'ESPESSURA (mm)': espessuras}


dict_dados_2 = {'QUANTIDADE': [40,
                               30,
                               20,
                               10],
                'VELOR MEDIDO (mm)': [incerteza.Erro(3.90, erro),
                                      incerteza.Erro(2.90, erro),
                                      incerteza.Erro(1.80, erro),
                                      incerteza.Erro(0.90, erro),
                                      ]}

dict_dados_3 = espessura_unitaria_erro(dict_dados_2)
dados_2 = statistics.DataSet(data=dict_dados_3)

# Plotagem de gráficos e ajuste de regressão linear
quantidades = espessura_unitaria(dict_dados_2)['QUANTIDADE']
espessuras = espessura_unitaria(dict_dados_2)['ESPESSURA (mm)']

k, alpha, rvalue, pvalue, std = scipy.stats.linregress(x=quantidades, y=espessuras)

# Visualização dos resultados
print(f'''
{dados_2}

REGRESSÃO LINEAR

k = {k}
alpha = {alpha}
r = {rvalue}
desvio padrão = {std}''')

n = numpy.linspace(start=0, stop=40, num=50)
l = [k * x + alpha for x in n]

plt.style.use(plt.style.available[5])
plt.title('')
plt.xlabel('Quantidade de folhas')
plt.ylabel('Espessura (mm)')
plt.plot(quantidades, espessuras, 'o', label='dados empíricos')
plt.plot(n, l, label='regressão linear')
plt.legend()
plt.show()
