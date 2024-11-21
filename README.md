# Gestor-Financeiro
Grupo: Luciano Damitz Pinheiro, Douglas Francisco Bolina Sibuya
 - Conceito: Desenvolver uma aplicação para realizar gestão financeira de modo a auxiliar o usuário a tomar decisões mais conscientes sobre seu dinheiro de forma intuitiva e que seja de fácil utilização. 
 - Função: O programa possuirá mecanismo para registrar de despesas, receitas, dinheiro guardado, programa de pontos, informações sobre os cartões de crédito e de débito e investimentos. A ferramenta também fornecerá visualizações com gráficos diários, semanais, mensais e anuais informando como o dinheiro está sendo usado, facilitando o usuário a ter consciência sobre como utilizar melhor seu dinheiro e tomar decisões sobre sua vida financeira a curto e a longo prazo de  modo a auxiliar o usuário a atingir seus objetivos. 
 - Motivação: Muitas pessoas têm dificuldade de gerir os seus recursos financeiros e com esse intuito projeto visa facilitar essa gestão de forma simplificada e descomplicada melhorando os hábitos financeiros e auxiliando para que os usuários realizem seus sonhos e atinjam seus objetivos.


## Diagrama de Classes
![image](.images/Diagrama_de_Classe_e_Relacionamento.png)

## Fluxograma
![image](.images/Fluxograma.png)

## Tutorial
O programa será feito em Python e será utilizada a biblioteca CustomTkinter para confecção de sua interface gráfica. Para realizar a instalação do CustomTkinter pode-se utilizar o seguinte comando no prompt de comando: “pip install customtkinter”. Estando o Python e a biblioteca CustomTkinter devidamente instalados e prontos para uso, pode-se começar a criar a interface gráfica. Como exemplo, temos o seguinte código:

import tkinter as tk
import customtkinter as ctk

#### Criar a janela principal
janela = ctk.CTk()

#### Definir o título da janela
janela.title("Minha primeira aplicação CustomTkinter")

#### Tamanho da janela
janela.geometry("400x300")

#### Adicionar um rótulo com uma mensagem
label = ctk.CTkLabel(janela, text="Olá, CustomTkinter!", font=("Arial", 20))
label.pack(pady=20)

#### Iniciar o loop da aplicação
janela.mainloop()

![image](.images/tutorial_janela.png)

#### Configurar o layout da janela para centralizar os widgets
janela.grid_rowconfigure(0, weight=1)
janela.grid_rowconfigure(1, weight=1)
janela.grid_rowconfigure(2, weight=1)
janela.grid_rowconfigure(3, weight=1)
janela.grid_columnconfigure(0, weight=1)

#### Adicionar um botão
def funcao_exemplo():
    print("Botão clicado!")

botao = ctk.CTkButton(janela, text="Clique Aqui", command=funcao_exemplo)
botao.pack(pady=10)

#### Adicionar uma entrada de texto
entrada = ctk.CTkEntry(janela, placeholder_text="Digite algo aqui")
entrada.pack(pady=10)

#### Adicionar uma caixa de seleção
checkbox = ctk.CTkCheckBox(janela, text="Opção")
checkbox.pack(pady=10)

#### Usando grid para posicionamento mais preciso
label.grid(row=0, column=0, padx=10, pady=10)
botao.grid(row=1, column=0, padx=10, pady=10)

#### Definir o modo de aparência: 'light', 'dark', ou 'system'
ctk.set_appearance_mode("dark")

#### Definir o tema de cor: 'blue', 'green', 'dark-blue'
ctk.set_default_color_theme("blue")

![image](.images/Tutorial_botoes.png)


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


