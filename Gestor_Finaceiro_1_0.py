import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt

class GestorFinanceiro(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestor Financeiro")
        self.geometry("500x500")

        self.total_investido = 0.0

        # Conectar ao banco de dados SQLite
        self.conn = sqlite3.connect('gestor_financeiro.db')
        self.cursor = self.conn.cursor()

        # Criar a tabela de usuários se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha BLOB NOT NULL
            )
        ''')
        self.conn.commit()

        self.frame_login = FrameLogin(self, self.conn, self.cursor)
        self.frame_cadastro = FrameCadastro(self, self.conn, self.cursor)
        self.frame_menu = FrameMenu(self)
        self.frame_receitas = FrameReceitas(self)
        self.frame_despesas = FrameDespesas(self)
        self.frame_money = FrameMoney(self)
        self.frame_card = FrameCard(self)

        self.mostrar_frame(self.frame_login)

    def mostrar_frame(self, frame):
        frame.tkraise()

class FrameLogin(tk.Frame):
    def __init__(self, master, conn, cursor):
        super().__init__(master, bg='green')
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_login = tk.Label(self, text="LOGIN", font=("", 20), bg='green')
        lb_login.pack(pady=10)

        lb_user = tk.Label(self, text="Usuário", bg='green')
        lb_user.place(relx=0.1, rely=0.2)

        self.entry_user = tk.Entry(self)
        self.entry_user.place(relx=0.2, rely=0.2)

        lb_senha = tk.Label(self, text="Senha", bg='green')
        lb_senha.place(relx=0.1, rely=0.3)

        self.entry_senha = tk.Entry(self, show='*')
        self.entry_senha.place(relx=0.2, rely=0.3)

        bt_entrar = tk.Button(self, text="Entrar", command=self.realizar_login)
        bt_entrar.place(relx=0.2, rely=0.4)

        bt_novocadastro = tk.Button(self, text="Novo Cadastro", command=lambda: master.mostrar_frame(master.frame_cadastro))
        bt_novocadastro.place(relx=0.6, rely=0.4)

    def realizar_login(self):
        usuario = self.entry_user.get().strip()
        senha = self.entry_senha.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        self.cursor.execute("SELECT senha FROM usuarios WHERE usuario = ?", (usuario,))
        result = self.cursor.fetchone()
        if result:
            stored_hash = result[0]
            if bcrypt.checkpw(senha.encode('utf-8'), stored_hash):
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                self.master.mostrar_frame(self.master.frame_menu)
                # Limpar os campos após o login
                self.entry_user.delete(0, tk.END)
                self.entry_senha.delete(0, tk.END)
                return
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")

class FrameCadastro(tk.Frame):
    def __init__(self, master, conn, cursor):
        super().__init__(master, bg='blue')
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_cadastro = tk.Label(self, text="CADASTRO", font=("", 20), bg='blue')
        lb_cadastro.pack(pady=10)

        lb_user2 = tk.Label(self, text="Usuário", bg='blue')
        lb_user2.place(relx=0.1, rely=0.2)

        self.entry_user2 = tk.Entry(self)
        self.entry_user2.place(relx=0.2, rely=0.2)

        lb_senha2 = tk.Label(self, text="Senha", bg='blue')
        lb_senha2.place(relx=0.1, rely=0.3)

        self.entry_senha2 = tk.Entry(self, show='*')
        self.entry_senha2.place(relx=0.2, rely=0.3)

        bt_cadastrar = tk.Button(self, text="Cadastrar", command=self.realizar_cadastro)
        bt_cadastrar.place(relx=0.6, rely=0.4)

    def realizar_cadastro(self):
        usuario = self.entry_user2.get().strip()
        senha = self.entry_senha2.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        # Hash da senha usando bcrypt
        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        try:
            self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, hashed_senha))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.master.mostrar_frame(self.master.frame_login)
            # Limpar os campos após o cadastro
            self.entry_user2.delete(0, tk.END)
            self.entry_senha2.delete(0, tk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de usuário já existe.")

class FrameMenu(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='red')
        self.master = master
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_menu = tk.Label(self, text="MENU", font=("", 20), bg='red')
        lb_menu.pack(pady=20)

        bt_receitas = tk.Button(self, text="Receitas", command=lambda: master.mostrar_frame(master.frame_receitas))
        bt_receitas.pack(padx=10, pady=10)

        bt_despesas = tk.Button(self, text="Despesas", command=lambda: master.mostrar_frame(master.frame_despesas))
        bt_despesas.pack(padx=10, pady=10)

        bt_money = tk.Button(self, text="Dinheiro Guardado", command=lambda: master.mostrar_frame(master.frame_money))
        bt_money.pack(padx=10, pady=10)

        bt_card = tk.Button(self, text="Cartões", command=lambda: master.mostrar_frame(master.frame_card))
        bt_card.pack(padx=10, pady=10)

        bt_sair = tk.Button(self, text="Sair", command=self.master.quit)
        bt_sair.pack(padx=10, pady=10)

class FrameReceitas(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='lightblue')
        self.master = master
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_receita = tk.Label(self, text="RECEITAS", font=("", 20), bg='lightblue')
        lb_receita.pack(pady=10)

        lb_valor = tk.Label(self, text="Valor:", bg='lightblue')
        lb_valor.place(relx=0.1, rely=0.15)
        self.entrada_valor = tk.Entry(self)
        self.entrada_valor.place(relx=0.3, rely=0.15)

        lb_data = tk.Label(self, text="Data:", bg='lightblue')
        lb_data.place(relx=0.1, rely=0.25)
        self.entrada_data = tk.Entry(self)
        self.entrada_data.place(relx=0.3, rely=0.25)

        lb_descricao = tk.Label(self, text="Descrição:", bg='lightblue')
        lb_descricao.place(relx=0.1, rely=0.35)
        self.entrada_descricao = tk.Entry(self)
        self.entrada_descricao.place(relx=0.3, rely=0.35)

        self.lista_receitas = tk.Listbox(self)
        self.lista_receitas.place(relx=0.1, rely=0.45, relwidth=0.75, relheight=0.3)

        bt_lancar = tk.Button(self, text="Lançar Receita", command=self.lancar_receita)
        bt_lancar.place(relx=0.2, rely=0.8)

        bt_remover = tk.Button(self, text="Remover Receita", command=self.remover_receita)
        bt_remover.place(relx=0.6, rely=0.8)

        bt_voltar_menu = tk.Button(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu.place(relx=0.45, rely=0.9)

    def lancar_receita(self):
        valor = self.entrada_valor.get().strip()
        data = self.entrada_data.get().strip()
        descricao = self.entrada_descricao.get().strip()

        if valor and data and descricao:
            try:
                valor_float = float(valor)
                receita = f"Valor: R$ {valor_float:.2f}, Data: {data}, Descrição: {descricao}"
                self.lista_receitas.insert(tk.END, receita)
                self.entrada_valor.delete(0, tk.END)
                self.entrada_data.delete(0, tk.END)
                self.entrada_descricao.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o valor.")
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def remover_receita(self):
        try:
            selected_item_index = self.lista_receitas.curselection()[0]
            self.lista_receitas.delete(selected_item_index)
            messagebox.showinfo("Sucesso", "Receita removida com sucesso.")
        except IndexError:
            messagebox.showerror("Erro", "Nenhuma receita selecionada para remover.")

class FrameDespesas(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='lightcoral')
        self.master = master
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_despesa = tk.Label(self, text="DESPESAS", font=("", 20), bg='lightcoral')
        lb_despesa.pack(pady=10)

        lb_valor_despesa = tk.Label(self, text="Valor:", bg='lightcoral')
        lb_valor_despesa.place(relx=0.1, rely=0.15)
        self.entrada_valor_despesa = tk.Entry(self)
        self.entrada_valor_despesa.place(relx=0.35, rely=0.15)

        lb_data_despesa = tk.Label(self, text="Data:", bg='lightcoral')
        lb_data_despesa.place(relx=0.1, rely=0.2)
        self.entrada_data_despesa = tk.Entry(self)
        self.entrada_data_despesa.place(relx=0.35, rely=0.2)

        lb_local_despesa = tk.Label(self, text="Local:", bg='lightcoral')
        lb_local_despesa.place(relx=0.1, rely=0.25)
        self.entrada_local_despesa = tk.Entry(self)
        self.entrada_local_despesa.place(relx=0.35, rely=0.25)

        lb_tipo_pagamento_despesa = tk.Label(self, text="Tipo de Pagamento:", bg='lightcoral')
        lb_tipo_pagamento_despesa.place(relx=0.1, rely=0.3)
        self.entrada_tipo_pagamento_despesa = tk.Entry(self)
        self.entrada_tipo_pagamento_despesa.place(relx=0.35, rely=0.3)

        lb_tipo_despesa = tk.Label(self, text="Tipo:", bg='lightcoral')
        lb_tipo_despesa.place(relx=0.1, rely=0.35)
        self.entrada_tipo_despesa = tk.Entry(self)
        self.entrada_tipo_despesa.place(relx=0.35, rely=0.35)

        lb_descricao_despesa = tk.Label(self, text="Descrição:", bg='lightcoral')
        lb_descricao_despesa.place(relx=0.1, rely=0.4)
        self.entrada_descricao_despesa = tk.Entry(self)
        self.entrada_descricao_despesa.place(relx=0.35, rely=0.4)

        self.lista_despesas = tk.Listbox(self)
        self.lista_despesas.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.3)

        bt_lancar_despesa = tk.Button(self, text="Lançar Despesa", command=self.lancar_despesa)
        bt_lancar_despesa.place(relx=0.2, rely=0.82)

        bt_remover_despesa = tk.Button(self, text="Remover Despesa", command=self.remover_despesa)
        bt_remover_despesa.place(relx=0.6, rely=0.82)

        bt_voltar_menu_despesas = tk.Button(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu_despesas.place(relx=0.45, rely=0.92)

    def lancar_despesa(self):
        valor = self.entrada_valor_despesa.get().strip()
        data = self.entrada_data_despesa.get().strip()
        descricao = self.entrada_descricao_despesa.get().strip()
        local = self.entrada_local_despesa.get().strip()
        tipo_pagamento = self.entrada_tipo_pagamento_despesa.get().strip()
        tipo = self.entrada_tipo_despesa.get().strip()

        if valor and data and descricao and local and tipo_pagamento and tipo:
            try:
                valor_float = float(valor)
                despesa = f"Valor: R$ {valor_float:.2f}, Data: {data}, Local: {local}, Tipo: {tipo}, Pagamento: {tipo_pagamento}, Descrição: {descricao}"
                self.lista_despesas.insert(tk.END, despesa)
                self.entrada_valor_despesa.delete(0, tk.END)
                self.entrada_data_despesa.delete(0, tk.END)
                self.entrada_descricao_despesa.delete(0, tk.END)
                self.entrada_local_despesa.delete(0, tk.END)
                self.entrada_tipo_pagamento_despesa.delete(0, tk.END)
                self.entrada_tipo_despesa.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o valor.")
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def remover_despesa(self):
        try:
            selected_item_index = self.lista_despesas.curselection()[0]
            self.lista_despesas.delete(selected_item_index)
            messagebox.showinfo("Sucesso", "Despesa removida com sucesso.")
        except IndexError:
            messagebox.showerror("Erro", "Nenhuma despesa selecionada para remover.")

class FrameMoney(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='lightgreen')
        self.master = master
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_money = tk.Label(self, text="DINHEIRO GUARDADO", font=("", 20), bg='lightgreen')
        lb_money.pack(pady=10)

        lb_valor_money = tk.Label(self, text="Valor:", bg='lightgreen')
        lb_valor_money.place(relx=0.1, rely=0.2)
        self.entrada_valor_money = tk.Entry(self)
        self.entrada_valor_money.place(relx=0.3, rely=0.2)

        lb_rendimento_money = tk.Label(self, text="Rendimento:", bg='lightgreen')
        lb_rendimento_money.place(relx=0.1, rely=0.3)
        self.entrada_rendimento_money = tk.Entry(self)
        self.entrada_rendimento_money.place(relx=0.3, rely=0.3)

        self.lb_total_investido = tk.Label(self, text=f"Total Investido: R$ {master.total_investido:.2f}", font=("", 15), bg='lightgreen')
        self.lb_total_investido.place(relx=0.25, rely=0.5)

        bt_lancar_money = tk.Button(self, text="Lançar", command=self.lancar_money)
        bt_lancar_money.place(relx=0.45, rely=0.7)

        bt_voltar_menu_money = tk.Button(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu_money.place(relx=0.45, rely=0.85)

    def lancar_money(self):
        valor = self.entrada_valor_money.get().strip()
        rendimento = self.entrada_rendimento_money.get().strip()

        if valor and rendimento:
            try:
                valor_float = float(valor)
                rendimento_float = float(rendimento)
                self.master.total_investido += valor_float + rendimento_float
                self.lb_total_investido.config(text=f"Total Investido: R$ {self.master.total_investido:.2f}")
                self.entrada_valor_money.delete(0, tk.END)
                self.entrada_rendimento_money.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para o valor e rendimento.")
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

class FrameCard(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg='lightyellow')
        self.master = master
        self.place(relx=0.025, rely=0.025, relwidth=0.95, relheight=0.95)

        lb_card = tk.Label(self, text="CARTÕES", font=("", 20), bg='lightyellow')
        lb_card.pack(pady=10)

        lb_nome_cartao = tk.Label(self, text="Nome:", bg='lightyellow')
        lb_nome_cartao.place(relx=0.1, rely=0.15)
        self.entrada_nome_cartao = tk.Entry(self)
        self.entrada_nome_cartao.place(relx=0.3, rely=0.15)

        lb_bandeira_cartao = tk.Label(self, text="Bandeira:", bg='lightyellow')
        lb_bandeira_cartao.place(relx=0.1, rely=0.25)
        self.entrada_bandeira_cartao = tk.Entry(self)
        self.entrada_bandeira_cartao.place(relx=0.3, rely=0.25)

        lb_limite_cartao = tk.Label(self, text="Limite:", bg='lightyellow')
        lb_limite_cartao.place(relx=0.1, rely=0.35)
        self.entrada_limite_cartao = tk.Entry(self)
        self.entrada_limite_cartao.place(relx=0.3, rely=0.35)

        lb_fatura_cartao = tk.Label(self, text="Fatura:", bg='lightyellow')
        lb_fatura_cartao.place(relx=0.1, rely=0.45)
        self.entrada_fatura_cartao = tk.Entry(self)
        self.entrada_fatura_cartao.place(relx=0.3, rely=0.45)

        self.lista_cartoes = tk.Listbox(self)
        self.lista_cartoes.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.3)

        bt_lancar_cartao = tk.Button(self, text="Lançar Cartão", command=self.lancar_cartao)
        bt_lancar_cartao.place(relx=0.15, rely=0.86)

        bt_pagar_fatura = tk.Button(self, text="Pagar Fatura", command=self.pagar_fatura)
        bt_pagar_fatura.place(relx=0.41, rely=0.86)

        bt_remover_cartao = tk.Button(self, text="Remover Cartão", command=self.remover_cartao)
        bt_remover_cartao.place(relx=0.65, rely=0.86)

        bt_voltar_menu_card = tk.Button(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu_card.place(relx=0.44, rely=0.93)

    def lancar_cartao(self):
        nome = self.entrada_nome_cartao.get().strip()
        bandeira = self.entrada_bandeira_cartao.get().strip()
        limite = self.entrada_limite_cartao.get().strip()
        fatura = self.entrada_fatura_cartao.get().strip()

        if nome and bandeira and limite and fatura:
            try:
                limite_float = float(limite)
                cartao = f"Nome: {nome}, Bandeira: {bandeira}, Limite: R$ {limite_float:.2f}, Fatura: {fatura}"
                self.lista_cartoes.insert(tk.END, cartao)
                self.entrada_nome_cartao.delete(0, tk.END)
                self.entrada_bandeira_cartao.delete(0, tk.END)
                self.entrada_limite_cartao.delete(0, tk.END)
                self.entrada_fatura_cartao.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o limite.")
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def pagar_fatura(self):
        try:
            selected_item_index = self.lista_cartoes.curselection()[0]
            current_text = self.lista_cartoes.get(selected_item_index)
            if " - Fatura paga" not in current_text:
                updated_text = current_text + " - Fatura paga"
                self.lista_cartoes.delete(selected_item_index)
                self.lista_cartoes.insert(selected_item_index, updated_text)
                messagebox.showinfo("Sucesso", "Fatura paga com sucesso.")
            else:
                messagebox.showinfo("Informação", "Fatura já está paga.")
        except IndexError:
            messagebox.showerror("Erro", "Nenhum cartão selecionado para pagar a fatura.")

    def remover_cartao(self):
        try:
            selected_item_index = self.lista_cartoes.curselection()[0]
            self.lista_cartoes.delete(selected_item_index)
            messagebox.showinfo("Sucesso", "Cartão removido com sucesso.")
        except IndexError:
            messagebox.showerror("Erro", "Nenhum cartão selecionado para remover.")

if __name__ == "__main__":
    app = GestorFinanceiro()
    app.mainloop()