# Gestor-Financeiro
Grupo: Luciano Damitz Pinheiro, Douglas Francisco Bolina Sibuya
 - Conceito: Desenvolver uma aplicação para realizar gestão financeira de modo a auxiliar o usuário a tomar decisões mais conscientes sobre seu dinheiro de forma intuitiva e que seja de fácil utilização. 
 - Função: O programa possuirá mecanismo para registrar de despesas, receitas, dinheiro guardado, programa de pontos, informações sobre os cartões de crédito e de débito e investimentos. A ferramenta também fornecerá visualizações com gráficos diários, semanais, mensais e anuais informando como o dinheiro está sendo usado, facilitando o usuário a ter consciência sobre como utilizar melhor seu dinheiro e tomar decisões sobre sua vida financeira a curto e a longo prazo de  modo a auxiliar o usuário a atingir seus objetivos. 
 - Motivação: Muitas pessoas têm dificuldade de gerir os seus recursos financeiros e com esse intuito projeto visa facilitar essa gestão de forma simplificada e descomplicada melhorando os hábitos financeiros e auxiliando para que os usuários realizem seus sonhos e atinjam seus objetivos.


## Diagrama de Classes
![image](.images/Diagrama_de_Classe_e_Relacionamento.png)

## Fluxograma
![image](.images/Fluxograma.drawio.png)

## Tutorial
O programa será feito em Python e será utilizada a biblioteca Tkinter para confecção de sua interface gráfica. Ao realizar uma instalação padrão de Python, o Tkinter já deve ser instalado junto. Para confirmar, é possível verificar utilizando o seguinte comando no prompt de comando: “pip install tk”. Estando o Python e a biblioteca Tkinter devidamente instalados e prontos para uso, pode-se começar a criar a interface gráfica. Como exemplo, temos o seguinte código:

import tkinter as tk

#Criar a janela principal

janela = tk.Tk() 


#Definir o título da janela

janela.title("Minha primeira aplicação Tkinter")


#Tamanho da janela

janela.geometry("400x300")

#Iniciar o loop da aplicação

janela.mainloop()


Na imagem abaixo é possível ver a janela criada com o código acima.

![image](https://github.com/user-attachments/assets/2cc58a60-19d3-46a4-ad6a-3e980d063aa5)


## Esboço GUI

#### Tela de login
![image](.images/Tela_Login.png)

#### Menu
![image](.images/Menu.png)

#### Lançamento de Despesas
![image](.images/Lancar_despesa.png)

#### Lançamento de Receitas
![image](.images/Lancar_receitas.png)

#### Gerenciamento de Cartões
![image](.images/Gerenciar_cartões.png)

#### Tela de dinheiro investido
![image](.images/Dinheiro_Investido.png)


