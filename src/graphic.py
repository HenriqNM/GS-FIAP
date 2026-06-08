from typing import List
import matplotlib.pyplot as plt
import time


def gerar_grafico(nome_sensor: str, indices: List[int], medias: List[float]) -> None:
    if not indices or not medias:
        print(f"\nNão há dados disponíveis para gerar o gráfico do sensor: {nome_sensor}")
        return

    print(f"\nGerando gráfico de variação para o sensor: {nome_sensor}...")
    time.sleep(2)

    plt.figure(figsize=(10, 5))
    plt.plot(indices, medias, marker='o', linestyle='-', color='g', label=f'Média Móvel ({nome_sensor})')

    plt.title(f'Variação Histórica da Média - Sensor: {nome_sensor}') 
    plt.xlabel('Número da Leitura (Sequencial do Sensor)')
    plt.ylabel('Valor da Média Móvel')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='best')

    plt.show()