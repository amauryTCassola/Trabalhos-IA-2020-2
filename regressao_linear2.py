# -*- coding: utf-8 -*-

# Regressão Linear Simples



# Commented out IPython magic to ensure Python compatibility.
# %matplotlib inline
from IPython.display import HTML
import sys
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np





"""#### Definição da função de custo"""

def compute_cost(theta_0, theta_1, theta_2, x, y, z):
    """
    Calcula o erro quadratico medio
    
    Args:
        theta_0 (float): intercepto da reta 
        theta_1 (float): parâmetro que multiplica x
        theta_2 (float): parâmetro que multiplica z
        x,y,x: valores
    Retorna:
        float: o erro quadratico medio
    """
    total_cost = 0



    n=np.size(x,0)
    
    
    for i in range(n):
      total_cost += ((theta_0 + (theta_1 * x[i]) + (theta_2 * z[i])) - y[i]) ** 2
    

    total_cost = (1/n)*total_cost
    
    
    
    return total_cost



def step_gradient(theta_0_current, theta_1_current, theta_2_current, x, y, z, alpha):
    """Calcula um passo em direção ao EQM mínimo
    
    Args:
        theta_0_current (float): valor atual de theta_0
        theta_1_current (float): valor atual de theta_1
        theta_2_current (float): valor atual de theta_2
        x,y,z: vetor com dados de treinamento (x,y,z)
        alpha (float): taxa de aprendizado / tamanho do passo 
    
    Retorna:
        tupla: (theta_0, theta_1, theta_2) os novos valores de theta_0, theta_1, theta_2
    """
    
    theta_0_updated = 0
    theta_1_updated = 0
    theta_2_updated = 0
    
    ### SEU CODIGO AQUI

    n=np.size(data,0)
    
    derivada_0 = 0
    derivada_1 = 0
    derivada_2 = 0
  
    for i in range(n-1):
      derivada_0 += (theta_0_current + (theta_1_current * x[i]) + (theta_2_current * z[i])) - y[i]
      derivada_1 += ((theta_0_current + (theta_1_current * x[i]) + (theta_2_current * z[i])) - y[i])*x[i]
      derivada_2 += ((theta_0_current + (theta_1_current * x[i]) + (theta_2_current * z[i])) - y[i])*z[i]
    derivada_0=(2/n)*derivada_0
    derivada_1=(2/n)*derivada_1 
    derivada_2=(2/n)*derivada_2 
    
    
    theta_0_updated = theta_0_current - (alpha * derivada_0)
    theta_1_updated = theta_1_current - (alpha * derivada_1)
    theta_2_updated = theta_2_current - (alpha * derivada_2)
    
    
    
    return theta_0_updated, theta_1_updated, theta_2_updated


def gradient_descent(x, y, z, starting_theta_0, starting_theta_1, starting_theta_2, learning_rate, num_iterations):
    """executa a descida do gradiente
    
    Args:
        x,y,z: dados de treinamento, x, y e z
        starting_theta_0 (float): valor inicial de theta0 
        starting_theta_1 (float): valor inicial de theta1
        starting_theta_2 (float): valor inicial de theta2
        learning_rate (float): hyperparâmetro para ajustar o tamanho do passo durante a descida do gradiente
        num_iterations (int): hyperparâmetro que decide o número de iterações que cada descida de gradiente irá executar
    
    Retorna:
        list : os primeiros dois parâmetros são o Theta0 e Theta1, que armazena o melhor ajuste da curva. O terceiro e quarto parâmetro, são vetores com o histórico dos valores para Theta0 e Theta1.
    """

    # valores iniciais
    theta_0 = starting_theta_0
    theta_1 = starting_theta_1
    theta_2 = starting_theta_2

    
    # variável para armazenar o custo ao final de cada step_gradient
    cost_graph = []
    
    # vetores para armazenar os valores de Theta0 e Theta1 apos cada iteração de step_gradient (pred = Theta1*x + Theta0)
    theta_0_progress = []
    theta_1_progress = []
    theta_2_progress = []
    
    # Para cada iteração, obtem novos (Theta0,Theta1) e calcula o custo (EQM)
    """
    num_iterations = 10
    """
    for i in range(num_iterations):
        cost_graph.append(compute_cost(theta_0, theta_1, theta_2, x, y, z))
        theta_0, theta_1, theta_2 = step_gradient(theta_0, theta_1, theta_2, x, y, z, alpha=0.0001)
        theta_0_progress.append(theta_0)
        theta_1_progress.append(theta_1)
        theta_2_progress.append(theta_2)
        
    return [theta_0, theta_1, theta_2, cost_graph, theta_0_progress, theta_1_progress, theta_2_progress]

"""#### Executa a função gradient_descent() para obter os parâmetros otimizados, Theta0 e Theta1."""
def normaliza(norm):
    norm_max = np.amax(norm)
    norm_min = np.amin(norm)
    for i in (range(len(norm))):
            norm[i] = (norm[i] - norm_min) / (norm_max - norm_min)
    return norm

def animate(i,theta_0_prog,theta_1_prog):
    pred = theta_1_prog[i] * x + theta_0_prog[i]
    line.set_data(x,pred)
    return line,

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("usage: launch_1attr.sh data.csv iter")

    else:
        iter = int(sys.argv[2])
        arquivo = sys.argv[1]
        data = np.genfromtxt(arquivo, delimiter=',')

        #Extrair colunas para análise
        x = np.array(data[1:,46])
        y = np.array(data[1:,80])
        z = np.array(data[1:,17])

        x = normaliza(x)
        z = normaliza(z)
        
        
#Gráfico dos dados
        plt.figure(figsize=(10, 6))
        plt.scatter(x,y)
        plt.xlabel('GrvLivArea')
        plt.ylabel('Sale Price')
        plt.title('Dados')
        plt.show()

        theta_0, theta_1, theta_2, cost_graph, theta_0_progress, theta_1_progress, theta_2_progress = gradient_descent(x, y, z, starting_theta_0=0, starting_theta_1=0, starting_theta_2=0, learning_rate=0, num_iterations=iter)

        #Imprimir parâmetros otimizados
        print ('Theta_0: ', theta_0)
        print ('Theta_1: ', theta_1)
        print ('Theta_2: ', theta_2)

        #Imprimir erro com os parâmetros otimizados
        print ('Erro Quadrático Médio: ', compute_cost(theta_0, theta_1, theta_2, x, y, z))

        """#### Gráfico do custo por iteração"""

        plt.figure(figsize=(10, 6))
        plt.plot(cost_graph)
        plt.xlabel('No. de interações')
        plt.ylabel('Custo')
        plt.title('Custo por iteração')
        plt.show()

        """A descida do gradiente converge depois de `5` iterações (verifique !)

        #### Gráfico de linha com melhor ajuste
        """

        #Gráfico de dispersão do conjunto de dados
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y)
        #Valores preditos de y
        pred = theta_1 * x + theta_0
        #Gráfico de linha do melhor ajuste
        plt.plot(x, pred, c='r')
        plt.xlabel('GrLivArea')
        plt.ylabel('Sale Price')
        plt.title('Melhor ajuste')
        plt.show()

        """### Progresso da descida do gradiente com o número de iterações"""



        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        theta_0 = theta_0_progress[0]
        theta_1 = theta_1_progress[0]
        pred = theta_1*x + theta_0
        
        line = ax.plot(x,pred, '-',c='r')[0]



        ani = animation.FuncAnimation(fig, animate, frames=len(theta_0_progress), fargs=(theta_0_progress,theta_1_progress,))
        ax.scatter(x,y)
        HTML(ani.to_jshtml())

