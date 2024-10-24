
import tkinter as tk

def mostrar_frame(frame):
    frame.tkraise()




####### Funções para o frame de receitas #######
# Função para lançar receita
def lancar_receita():
    valor = entrada_valor.get()
    data = entrada_data.get()
    descricao = entrada_descricao.get()
    
    if valor and data and descricao:
        receita = f"Valor: {valor}, Data: {data}, Descrição: {descricao}"
        lista_receitas.insert(tk.END, receita)  # Adiciona a receita ao Listbox
        # Limpa os campos após o lançamento
        entrada_valor.delete(0, tk.END)
        entrada_data.delete(0, tk.END)
        entrada_descricao.delete(0, tk.END)

# Função para remover a receita selecionada
def remover_receita():
    try:
        selected_item_index = lista_receitas.curselection()[0]  # Pega o índice da receita selecionada
        lista_receitas.delete(selected_item_index)  # Remove a receita do Listbox
        print("Receita removida")
    except IndexError:
        print("Nenhuma receita selecionada para remover.")
##########



####### Funções para o frame de despesas #######
def lancar_despesa():
    valor = entrada_valor_despesa.get()
    data = entrada_data_despesa.get()
    descricao = entrada_descricao_despesa.get()
    local = entrada_local_despesa.get()
    tipo_pagamento = entrada_tipo_pagamento_despesa.get()
    tipo = entrada_tipo_despesa.get()
    
    if valor and data and descricao and local and tipo_pagamento and tipo:
        despesa = f"Valor: {valor}, Data: {data}, Local: {local}, Tipo: {tipo}, Pagamento: {tipo_pagamento}, Descrição: {descricao}"
        lista_despesas.insert(tk.END, despesa)  # Adiciona a despesa ao Listbox
        # Limpa os campos após o lançamento
        entrada_valor_despesa.delete(0, tk.END)
        entrada_data_despesa.delete(0, tk.END)
        entrada_descricao_despesa.delete(0, tk.END)
        entrada_local_despesa.delete(0, tk.END)
        entrada_tipo_pagamento_despesa.delete(0, tk.END)
        entrada_tipo_despesa.delete(0, tk.END)

# Função para remover a despesa selecionada
def remover_despesa():
    try:
        selected_item_index = lista_despesas.curselection()[0]  # Pega o índice da despesa selecionada
        lista_despesas.delete(selected_item_index)  # Remove a despesa do Listbox
        print("Despesa removida")
    except IndexError:
        print("Nenhuma despesa selecionada para remover.")
##########





####### Funções para o frame de dinheiro guardado #######

# Variável para armazenar o valor total investido
total_investido = 0.0

def lancar_money():
    global total_investido
    valor = entrada_valor_money.get()
    rendimento = entrada_rendimento_money.get()

    if valor and rendimento:
        try:
            valor_float = float(valor)
            total_investido += valor_float  # Atualiza o valor total investido
            lb_total_investido.config(text=f"Total Investido: R$ {total_investido:.2f}")
            
            # Limpa os campos após o lançamento
            entrada_valor_money.delete(0, tk.END)
            entrada_rendimento_money.delete(0, tk.END)
        except ValueError:
            print("Por favor, insira um valor numérico válido para o valor.")
##########



####### Funções para o frame de cartão #######
def lancar_cartao():
    nome = entrada_nome_cartao.get()
    bandeira = entrada_bandeira_cartao.get()
    limite = entrada_limite_cartao.get()
    fatura = entrada_fatura_cartao.get()

    if nome and bandeira and limite and fatura:
        cartao = f"Nome: {nome}, Bandeira: {bandeira}, Limite: {limite}, Fatura: {fatura}"
        lista_cartoes.insert(tk.END, cartao)
        # Limpa os campos após o lançamento
        entrada_nome_cartao.delete(0, tk.END)
        entrada_bandeira_cartao.delete(0, tk.END)
        entrada_limite_cartao.delete(0, tk.END)
        entrada_fatura_cartao.delete(0, tk.END)

def pagar_fatura():
    try:
        selected_item_index = lista_cartoes.curselection()[0]  # Pega o índice do cartão selecionado
        current_text = lista_cartoes.get(selected_item_index)  # Pega o texto atual do item
        lista_cartoes.delete(selected_item_index)  # Remove o item atual da lista
        lista_cartoes.insert(selected_item_index, current_text + " - Fatura paga")  # Adiciona "Fatura paga"
    except IndexError:
        print("Nenhum cartão selecionado para pagar a fatura.")

def remover_cartao():
    try:
        selected_item_index = lista_cartoes.curselection()[0]  # Pega o índice do cartão selecionado
        lista_cartoes.delete(selected_item_index)  # Remove o cartão da lista
    except IndexError:
        print("Nenhum cartão selecionado para remover.")

##########













janela = tk.Tk()
janela.title("Gestor Financeiro")
janela.geometry("500x500")


# Tela de login
frame_login = tk.Frame(janela, bg='green')
frame_login.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

lb_login = tk.Label(frame_login, text="LOGIN", font=("", 20))
lb_login.pack(pady=10)

lb_user = tk.Label(frame_login, text = "Usuário")
lb_user.place(relx = 0.1, rely = 0.2)

entry_user = tk.Entry(frame_login)
entry_user.place(relx = 0.2, rely = 0.2)

lb_senha = tk.Label(frame_login, text = "Senha")
lb_senha.place(relx = 0.1, rely = 0.3)

entry_senha = tk.Entry(frame_login)
entry_senha.place(relx = 0.2, rely = 0.3)

bt_entrar = tk.Button(frame_login, text = "Entrar", command=lambda: mostrar_frame(frame_menu))                ### Esse botão deve realizar a verificação dos dados de login e direcionar ao menu principal
bt_entrar.place(relx = 0.2, rely = 0.4)

bt_novocadastro = tk.Button(frame_login, text = "Novo Cadastro", command=lambda: mostrar_frame(frame_cadastro))
bt_novocadastro.place(relx = 0.6, rely = 0.4)


# Tela de cadastro
frame_cadastro = tk.Frame(janela, bg='blue')
frame_cadastro.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

lb_cadastro = tk.Label(frame_cadastro, text="CADASTRO", font=("", 20))
lb_cadastro.pack(pady=10)

lb_user2 = tk.Label(frame_cadastro, text = "Usuário")
lb_user2.place(relx = 0.1, rely = 0.2)

entry_user2 = tk.Entry(frame_cadastro)
entry_user2.place(relx = 0.2, rely = 0.2)

lb_senha2 = tk.Label(frame_cadastro, text = "Senha")
lb_senha2.place(relx = 0.1, rely = 0.3)

entry_senha2 = tk.Entry(frame_cadastro)
entry_senha2.place(relx = 0.2, rely = 0.3)

bt_cadastrar = tk.Button(frame_cadastro, text = "Cadastrar")      ### Esse botão deve retornar para o frame_login e deve realizar o cadastro
bt_cadastrar.place(relx = 0.6, rely = 0.4)



##############   MENU   ##############

frame_menu = tk.Frame(janela, bg='red')
frame_menu.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

lb_menu = tk.Label(frame_menu, text="MENU", font=("", 20))
lb_menu.pack(pady=20)

bt_receitas = tk.Button(frame_menu, text = "Receitas", command = lambda: mostrar_frame(frame_receitas))
bt_receitas.pack(padx = 10, pady = 10)

bt_despesas = tk.Button(frame_menu, text = "Despesas", command = lambda: mostrar_frame(frame_despesas))
bt_despesas.pack(padx = 10, pady = 10)

bt_money = tk.Button(frame_menu, text = "Dinheiro Guardado", command = lambda: mostrar_frame(frame_money))
bt_money.pack(padx = 10, pady = 10)

bt_card = tk.Button(frame_menu, text = "Cartões", command = lambda: mostrar_frame(frame_card))
bt_card.pack(padx = 10, pady = 10)

#############



# Frame de Receitas
frame_receitas = tk.Frame(janela, bg='lightblue')
frame_receitas.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

# Labels e campos de entrada para valor, data e descrição
lb_receita = tk.Label(frame_receitas, text="RECEITAS", font=("", 20))
lb_receita.pack(pady=10)

lb_valor = tk.Label(frame_receitas, text="Valor:")
lb_valor.place(relx=0.1, rely=0.15)
entrada_valor = tk.Entry(frame_receitas)
entrada_valor.place(relx=0.3, rely=0.15)

lb_data = tk.Label(frame_receitas, text="Data:")
lb_data.place(relx=0.1, rely=0.25)
entrada_data = tk.Entry(frame_receitas)
entrada_data.place(relx=0.3, rely=0.25)

lb_descricao = tk.Label(frame_receitas, text="Descrição:")
lb_descricao.place(relx=0.1, rely=0.35)
entrada_descricao = tk.Entry(frame_receitas)
entrada_descricao.place(relx=0.3, rely=0.35)

# Listbox para exibir as receitas lançadas
lista_receitas = tk.Listbox(frame_receitas)
lista_receitas.place(relx=0.1, rely=0.45, relwidth=0.75, relheight=0.3)

# Botões Lançar e Remover Receita
bt_lancar = tk.Button(frame_receitas, text="Lançar Receita", command=lancar_receita)
bt_lancar.place(relx=0.2, rely=0.8)

bt_remover = tk.Button(frame_receitas, text="Remover Receita", command=remover_receita)
bt_remover.place(relx=0.6, rely=0.8)

# Botão Voltar para o Menu Principal
bt_voltar_menu = tk.Button(frame_receitas, text="Voltar", command=lambda: mostrar_frame(frame_menu))
bt_voltar_menu.place(relx=0.45, rely=0.9)



# Frame de Despesas
frame_despesas = tk.Frame(janela, bg='lightcoral')
frame_despesas.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

lb_despesa = tk.Label(frame_despesas, text="DESPESAS", font=("", 20))
lb_despesa.pack(pady=10)

lb_valor_despesa = tk.Label(frame_despesas, text="Valor:")
lb_valor_despesa.place(relx=0.1, rely=0.15)
entrada_valor_despesa = tk.Entry(frame_despesas)
entrada_valor_despesa.place(relx=0.35, rely=0.15)

lb_data_despesa = tk.Label(frame_despesas, text="Data:")
lb_data_despesa.place(relx=0.1, rely=0.2)
entrada_data_despesa = tk.Entry(frame_despesas)
entrada_data_despesa.place(relx=0.35, rely=0.2)

lb_local_despesa = tk.Label(frame_despesas, text="Local:")
lb_local_despesa.place(relx=0.1, rely=0.25)
entrada_local_despesa = tk.Entry(frame_despesas)
entrada_local_despesa.place(relx=0.35, rely=0.25)

lb_tipo_pagamento_despesa = tk.Label(frame_despesas, text="Tipo de Pagamento:")
lb_tipo_pagamento_despesa.place(relx=0.1, rely=0.3)
entrada_tipo_pagamento_despesa = tk.Entry(frame_despesas)
entrada_tipo_pagamento_despesa.place(relx=0.35, rely=0.3)

lb_tipo_despesa = tk.Label(frame_despesas, text="Tipo:")
lb_tipo_despesa.place(relx=0.1, rely=0.35)
entrada_tipo_despesa = tk.Entry(frame_despesas)
entrada_tipo_despesa.place(relx=0.35, rely=0.35)

lb_descricao_despesa = tk.Label(frame_despesas, text="Descrição:")
lb_descricao_despesa.place(relx=0.1, rely=0.4)
entrada_descricao_despesa = tk.Entry(frame_despesas)
entrada_descricao_despesa.place(relx=0.35, rely=0.4)

# Listbox para exibir as despesas lançadas
lista_despesas = tk.Listbox(frame_despesas)
lista_despesas.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.3)

# Botões para lançar e remover despesas
bt_lancar_despesa = tk.Button(frame_despesas, text="Lançar Despesa", command=lancar_despesa)
bt_lancar_despesa.place(relx=0.2, rely=0.82)

bt_remover_despesa = tk.Button(frame_despesas, text="Remover Despesa", command=remover_despesa)
bt_remover_despesa.place(relx=0.6, rely=0.82)

# Botão para voltar ao menu
bt_voltar_menu_despesas = tk.Button(frame_despesas, text="Voltar", command=lambda: mostrar_frame(frame_menu))
bt_voltar_menu_despesas.place(relx=0.45, rely=0.92)




# Frame de Dinheiro Guardado
frame_money = tk.Frame(janela, bg='lightgreen')
frame_money.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

lb_money = tk.Label(frame_money, text="DINHEIRO GUARDADO", font=("", 20))
lb_money.pack(pady=10)

lb_valor_money = tk.Label(frame_money, text="Valor:")
lb_valor_money.place(relx=0.1, rely=0.2)
entrada_valor_money = tk.Entry(frame_money)
entrada_valor_money.place(relx=0.3, rely=0.2)

lb_rendimento_money = tk.Label(frame_money, text="Rendimento:")
lb_rendimento_money.place(relx=0.1, rely=0.3)
entrada_rendimento_money = tk.Entry(frame_money)
entrada_rendimento_money.place(relx=0.3, rely=0.3)

# Rótulo para mostrar o total investido
lb_total_investido = tk.Label(frame_money, text=f"Total Investido: R$ {total_investido:.2f}", font=("", 15))
lb_total_investido.place(relx=0.25, rely=0.5)

# Botão para lançar o valor e o rendimento
bt_lancar_money = tk.Button(frame_money, text="Lançar", command=lancar_money)
bt_lancar_money.place(relx=0.45, rely=0.7)

# Botão para voltar ao menu
bt_voltar_menu_money = tk.Button(frame_money, text="Voltar", command=lambda: mostrar_frame(frame_menu))
bt_voltar_menu_money.place(relx=0.45, rely=0.85)




# Frame de Cartões
frame_card = tk.Frame(janela, bg='lightyellow')
frame_card.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

lb_card = tk.Label(frame_card, text="CARTÕES", font=("", 20))
lb_card.pack(pady=10)

lb_nome_cartao = tk.Label(frame_card, text="Nome:")
lb_nome_cartao.place(relx=0.1, rely=0.15)
entrada_nome_cartao = tk.Entry(frame_card)
entrada_nome_cartao.place(relx=0.3, rely=0.15)

lb_bandeira_cartao = tk.Label(frame_card, text="Bandeira:")
lb_bandeira_cartao.place(relx=0.1, rely=0.25)
entrada_bandeira_cartao = tk.Entry(frame_card)
entrada_bandeira_cartao.place(relx=0.3, rely=0.25)

lb_limite_cartao = tk.Label(frame_card, text="Limite:")
lb_limite_cartao.place(relx=0.1, rely=0.35)
entrada_limite_cartao = tk.Entry(frame_card)
entrada_limite_cartao.place(relx=0.3, rely=0.35)

lb_fatura_cartao = tk.Label(frame_card, text="Fatura:")
lb_fatura_cartao.place(relx=0.1, rely=0.45)
entrada_fatura_cartao = tk.Entry(frame_card)
entrada_fatura_cartao.place(relx=0.3, rely=0.45)

# Listbox para exibir os cartões lançados
lista_cartoes = tk.Listbox(frame_card)
lista_cartoes.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.3)

# Botões para lançar cartão, pagar fatura e remover cartão
bt_lancar_cartao = tk.Button(frame_card, text="Lançar Cartão", command=lancar_cartao)
bt_lancar_cartao.place(relx=0.15, rely=0.86)

bt_pagar_fatura = tk.Button(frame_card, text="Pagar Fatura", command=pagar_fatura)
bt_pagar_fatura.place(relx=0.41, rely=0.86)

bt_remover_cartao = tk.Button(frame_card, text="Remover Cartão", command=remover_cartao)
bt_remover_cartao.place(relx=0.65, rely=0.86)

# Botão para voltar ao menu
bt_voltar_menu_card = tk.Button(frame_card, text="Voltar", command=lambda: mostrar_frame(frame_menu))
bt_voltar_menu_card.place(relx=0.44, rely=0.93)











mostrar_frame(frame_login)

janela.mainloop()




