import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import sqlite3
import bcrypt
import matplotlib.pyplot as plt 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg 
import datetime
import matplotlib.dates as mdates

class FrameLogin(ctk.CTkFrame):
    def __init__(self, master, conn, cursor):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        # Configurar grid 
        self.grid_columnconfigure(0, weight=1) # Coluna esquerda 
        self.grid_columnconfigure(1, weight=1) # Coluna direita 
        self.grid_rowconfigure(0, weight=4) # Linha superior - 0
        self.grid_rowconfigure(1, weight=1) # Linha do meio - 1
        self.grid_rowconfigure(2, weight=1) # Linha do meio - 2
        self.grid_rowconfigure(3, weight=4) # Linha do meio - 3
        self.grid_rowconfigure(4, weight=20) # Linha inferior - 4

        lb_login = ctk.CTkLabel(self, text="LOGIN", font=("", 50))
        lb_login.grid(row=0,column=0, columnspan = 2, pady=20)

        lb_user = ctk.CTkLabel(self, text="Usuário")
        lb_user.grid(row=1, column=0, padx=55, pady=10, sticky = "e")
        self.entry_user = ctk.CTkEntry(self)
        self.entry_user.grid(row=1, column=1, pady=10, sticky = "w")

        lb_senha = ctk.CTkLabel(self, text="Senha  ")
        lb_senha.grid(row=2, column=0, padx=55, pady=10, sticky = "e")
        self.entry_senha = ctk.CTkEntry(self, show='*')
        self.entry_senha.grid(row=2, column=1, pady=10, sticky = "w")

        bt_entrar = ctk.CTkButton(self, text="Entrar", command=self.realizar_login)
        bt_entrar.grid(row=3, column=0, padx=20, pady=20, sticky = "e")
        bt_novocadastro = ctk.CTkButton(self, text="Novo Cadastro", command=lambda: master.mostrar_frame(master.frame_cadastro))
        bt_novocadastro.grid(row=3, column=1, padx=20, pady=20, sticky = "w")

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
                self.entry_user.delete(0, ctk.END)
                self.entry_senha.delete(0, ctk.END)
                return
        messagebox.showerror("Erro", "Usuário ou senha incorretos.")



class GestorFinanceiro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Gestor Financeiro")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

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

        # Inicializar os frames corretamente com os argumentos necessários
        self.frame_login = FrameLogin(self, self.conn, self.cursor)
        self.frame_cadastro = FrameCadastro(self, self.conn, self.cursor)
        self.frame_menu = FrameMenu(self)
        self.frame_receitas = FrameReceitas(self, self.conn, self.cursor)
        self.frame_despesas = FrameDespesas(self, self.conn, self.cursor)
        self.frame_money = FrameMoney(self, self.conn, self.cursor)
        self.frame_card = FrameCard(self, self.conn, self.cursor)

        self.mostrar_frame(self.frame_login)

    def mostrar_frame(self, frame):
        frame.tkraise()

    def formatar_campo_data(self, var):
        """
        Função para formatar automaticamente o campo de data para dd/mm/yyyy.
        """
        def formatar_data(*args):
            valor = var.get()
            novo_valor = self.aplicar_mascara_data(valor)
            if novo_valor != valor:
                var.set(novo_valor)
        var.trace_add('write', formatar_data)

    def aplicar_mascara_data(self, valor):
        """
        Aplica a máscara de data (dd/mm/yyyy) ao valor fornecido.
        """
        valor = valor.replace('/', '')  # Remove as barras existentes
        resultado = ''
        if len(valor) >= 1:
            resultado += valor[:2]
        if len(valor) >= 3:
            resultado += '/' + valor[2:4]
        if len(valor) >= 5:
            resultado += '/' + valor[4:8]
        return resultado[:10]  # Limita ao tamanho máximo de 10 caracteres

    
class FrameCadastro(ctk.CTkFrame):
    def __init__(self, master, conn, cursor):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        # Configurar grid 
        self.grid_columnconfigure(0, weight=1) # Coluna esquerda 
        self.grid_columnconfigure(1, weight=1) # Coluna direita 
        self.grid_rowconfigure(0, weight=4) # Linha superior - 0
        self.grid_rowconfigure(1, weight=1) # Linha do meio - 1
        self.grid_rowconfigure(2, weight=1) # Linha do meio - 2
        self.grid_rowconfigure(3, weight=4) # Linha do meio - 3
        self.grid_rowconfigure(4, weight=20) # Linha inferior - 4

        lb_cadastro = ctk.CTkLabel(self, text="CADASTRO", font=("", 50))
        lb_cadastro.grid(row=0,column=0, columnspan = 2, pady=20)

        lb_user2 = ctk.CTkLabel(self, text="Usuário")
        lb_user2.grid(row=1, column=0, padx=55, pady=10, sticky = "e")
        self.entry_user2 = ctk.CTkEntry(self)
        self.entry_user2.grid(row=1, column=1, pady=10, sticky = "w")

        lb_senha2 = ctk.CTkLabel(self, text="Senha  ")
        lb_senha2.grid(row=2, column=0, padx=55, pady=10, sticky = "e")
        self.entry_senha2 = ctk.CTkEntry(self, show='*')
        self.entry_senha2.grid(row=2, column=1, pady=10, sticky = "w")

        bt_cadastrar = ctk.CTkButton(self, text="Cadastrar", command=self.realizar_cadastro)
        bt_cadastrar.grid(row=3, column=0, padx=20, pady=20, sticky = "e")
        bt_voltar = ctk.CTkButton(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_login))
        bt_voltar.grid(row=3, column=1, padx=20, pady=20, sticky = "w")

    def realizar_cadastro(self):
        usuario = self.entry_user2.get().strip()
        senha = self.entry_senha2.get().strip()

        if not usuario or not senha:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")
            return

        hashed_senha = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        try:
            self.cursor.execute("INSERT INTO usuarios (usuario, senha) VALUES (?, ?)", (usuario, hashed_senha))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            self.master.mostrar_frame(self.master.frame_login)
            self.entry_user2.delete(0, ctk.END)
            self.entry_senha2.delete(0, ctk.END)
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Nome de usuário já existe.")

class FrameMenu(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        lb_menu = ctk.CTkLabel(self, text="MENU", font=("", 50))
        lb_menu.pack(pady=40)

        bt_receitas = ctk.CTkButton(self, text="Receitas", command=lambda: master.mostrar_frame(master.frame_receitas))
        bt_receitas.pack(padx=20, pady=10)

        bt_despesas = ctk.CTkButton(self, text="Despesas", command=lambda: master.mostrar_frame(master.frame_despesas))
        bt_despesas.pack(padx=20, pady=10)

        bt_money = ctk.CTkButton(self, text="Dinheiro Guardado", command=lambda: master.mostrar_frame(master.frame_money))
        bt_money.pack(padx=20, pady=10)

        bt_card = ctk.CTkButton(self, text="Cartões", command=lambda: master.mostrar_frame(master.frame_card))
        bt_card.pack(padx=20, pady=10)

        bt_sair = ctk.CTkButton(self, text="Sair", command=self.master.quit)
        bt_sair.pack(padx=20, pady=10)



class FrameReceitas(ctk.CTkFrame):
    def __init__(self, master, conn, cursor):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        
        # Formatar campos de data automaticamente
        self.data_var = tk.StringVar()
        self.master.formatar_campo_data(self.data_var)

        # Criar a tabela de receitas se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS receitas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                descricao TEXT
            )
        ''')
        self.conn.commit()
        
        lb_receita = ctk.CTkLabel(self, text="RECEITAS", font=("", 20))
        lb_receita.pack(pady=10)

        lb_valor = ctk.CTkLabel(self, text="Valor:")
        lb_valor.place(relx=0.1, rely=0.15)
        self.entrada_valor = ctk.CTkEntry(self)
        self.entrada_valor.place(relx=0.3, rely=0.15)

        lb_data = ctk.CTkLabel(self, text="Data (dd/mm/yyyy):")
        lb_data.place(relx=0.1, rely=0.25)
        self.entrada_data = ctk.CTkEntry(self, textvariable=self.data_var)
        self.entrada_data.place(relx=0.3, rely=0.25)

        lb_descricao = ctk.CTkLabel(self, text="Descrição:")
        lb_descricao.place(relx=0.1, rely=0.35)
        self.entrada_descricao = ctk.CTkEntry(self)
        self.entrada_descricao.place(relx=0.3, rely=0.35)

        self.lista_receitas = ctk.CTkScrollableFrame(self, width=400, height=200)
        self.lista_receitas.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.25)

        bt_lancar = ctk.CTkButton(self, text="Lançar Receita", command=self.lancar_receita)
        bt_lancar.place(relx=0.2, rely=0.8, anchor="center")

        bt_remover = ctk.CTkButton(self, text="Remover Receita", command=self.remover_receita)
        bt_remover.place(relx=0.8, rely=0.8, anchor="center")

        bt_voltar_menu = ctk.CTkButton(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu.place(relx=0.5, rely=0.9, anchor="center")

        # Preparar o gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.35)

        # Armazenar dados de receitas
        self.dados_receitas = []

        # Variável para armazenar o item selecionado
        self.item_selecionado = None

        self.carregar_receitas()

    def carregar_receitas(self):
        self.cursor.execute("SELECT id, valor, data, descricao FROM receitas")
        registros = self.cursor.fetchall()
        for registro in registros:
            receita_id, valor, data, descricao = registro
            try:
                data_formatada = datetime.datetime.strptime(data, "%d/%m/%Y").date()
                self.dados_receitas.append((data_formatada, valor))
                self.adicionar_item_lista(receita_id, valor, data, descricao)
            except ValueError:
                continue  # Ignora registros com data inválida
        self.atualizar_grafico()

    def lancar_receita(self):
        valor = self.entrada_valor.get().strip()
        data = self.entrada_data.get().strip()
        descricao = self.entrada_descricao.get().strip()

        if valor and data and descricao:
            try:
                valor_float = float(valor)
                data_formatada = datetime.datetime.strptime(data, "%d/%m/%Y").date()
                data_str = data_formatada.strftime("%d/%m/%Y")
                
                # Inserir no banco de dados
                self.cursor.execute("INSERT INTO receitas (valor, data, descricao) VALUES (?, ?, ?)", 
                                    (valor_float, data_str, descricao))
                self.conn.commit()
                receita_id = self.cursor.lastrowid

                # Adicionar na lista
                self.dados_receitas.append((data_formatada, valor_float))
                self.adicionar_item_lista(receita_id, valor_float, data_str, descricao)
                self.atualizar_grafico()

                # Limpa os campos de entrada
                self.entrada_valor.delete(0, ctk.END)
                self.entrada_data.delete(0, ctk.END)
                self.entrada_descricao.delete(0, ctk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def adicionar_item_lista(self, receita_id, valor, data, descricao):
        item_frame = ctk.CTkFrame(self.lista_receitas)
        item_frame.pack(fill="x", padx=10, pady=5)
        
        item_label = ctk.CTkLabel(
            item_frame, 
            text=f"ID: {receita_id} | Valor: R$ {valor:.2f}, Data: {data}, Descrição: {descricao}",
            anchor="w"
        )
        item_label.pack(side="left", expand=True, fill="x")
        
        select_button = ctk.CTkButton(
            item_frame, 
            text="Selecionar", 
            width=10, 
            command=lambda f=item_frame, id=receita_id: self.selecionar_item(f, id)
        )
        select_button.pack(side="right")

    def selecionar_item(self, item_frame, receita_id):
        # Remove a seleção anterior (se houver)
        if self.item_selecionado:
            self.item_selecionado['frame'].configure(fg_color="transparent")
        
        # Destaca o item selecionado
        item_frame.configure(fg_color="blue")
        self.item_selecionado = {'frame': item_frame, 'id': receita_id}

    def remover_receita(self):
        if self.item_selecionado:
            receita_id = self.item_selecionado['id']
            try:
                # Remover do banco de dados
                self.cursor.execute("DELETE FROM receitas WHERE id = ?", (receita_id,))
                self.conn.commit()

                # Remover da lista de dados
                self.dados_receitas = [r for r in self.dados_receitas if r[0] != 
                                       datetime.datetime.strptime(
                                           self.item_selecionado['frame'].winfo_children()[0].cget("text").split(", ")[1].split(": ")[1], 
                                           "%d/%m/%Y"
                                       ).date() or r[1] != float(
                                           self.item_selecionado['frame'].winfo_children()[0].cget("text").split(", ")[0].split(": ")[1].replace("R$ ", "")
                                       )]
                
                # Remove o item selecionado da interface
                self.item_selecionado['frame'].destroy()
                self.item_selecionado = None
                self.atualizar_grafico()
                messagebox.showinfo("Sucesso", "Receita removida com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Nenhuma receita selecionada para remover.")

    def atualizar_grafico(self):
        self.ax.clear()
        if self.dados_receitas:
            receitas_por_mes = {}
            for data, valor in self.dados_receitas:
                mes = data.strftime("%Y-%m")
                if mes in receitas_por_mes:
                    receitas_por_mes[mes] += valor
                else:
                    receitas_por_mes[mes] = valor
            meses = sorted(receitas_por_mes.keys())
            valores = [receitas_por_mes[mes] for mes in meses]
            self.ax.bar(meses, valores)
            self.ax.set_xlabel("Data")
            self.ax.set_ylabel("Valor (R$)")
            self.ax.set_title("Receitas Mensais")
        self.canvas.draw()



class FrameDespesas(ctk.CTkFrame):
    def __init__(self, master, conn, cursor):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        # Formatar campos de data automaticamente
        self.data_var = tk.StringVar()
        self.master.formatar_campo_data(self.data_var)

        # Criar a tabela de despesas se não existir
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                valor REAL NOT NULL,
                data TEXT NOT NULL,
                local TEXT,
                tipo_pagamento TEXT,
                tipo TEXT,
                descricao TEXT
            )
        ''')
        self.conn.commit()

        lb_despesa = ctk.CTkLabel(self, text="DESPESAS", font=("", 20))
        lb_despesa.pack(pady=10)

        lb_valor_despesa = ctk.CTkLabel(self, text="Valor:")
        lb_valor_despesa.place(relx=0.1, rely=0.15)
        self.entrada_valor_despesa = ctk.CTkEntry(self)
        self.entrada_valor_despesa.place(relx=0.35, rely=0.15)

        lb_data_despesa = ctk.CTkLabel(self, text="Data (dd/mm/yyyy):")
        lb_data_despesa.place(relx=0.1, rely=0.2)
        self.entrada_data_despesa = ctk.CTkEntry(self, textvariable=self.data_var)
        self.entrada_data_despesa.place(relx=0.35, rely=0.2)

        lb_local_despesa = ctk.CTkLabel(self, text="Local:")
        lb_local_despesa.place(relx=0.1, rely=0.25)
        self.entrada_local_despesa = ctk.CTkEntry(self)
        self.entrada_local_despesa.place(relx=0.35, rely=0.25)

        lb_tipo_pagamento_despesa = ctk.CTkLabel(self, text="Tipo de Pagamento:")
        lb_tipo_pagamento_despesa.place(relx=0.1, rely=0.3)
        self.entrada_tipo_pagamento_despesa = ctk.CTkEntry(self)
        self.entrada_tipo_pagamento_despesa.place(relx=0.35, rely=0.3)

        lb_tipo_despesa = ctk.CTkLabel(self, text="Tipo:")
        lb_tipo_despesa.place(relx=0.1, rely=0.35)
        self.entrada_tipo_despesa = ctk.CTkEntry(self)
        self.entrada_tipo_despesa.place(relx=0.35, rely=0.35)

        lb_descricao_despesa = ctk.CTkLabel(self, text="Descrição:")
        lb_descricao_despesa.place(relx=0.1, rely=0.4)
        self.entrada_descricao_despesa = ctk.CTkEntry(self)
        self.entrada_descricao_despesa.place(relx=0.35, rely=0.4)

        # Usar CTkScrollableFrame para a lista de despesas
        self.lista_despesas = ctk.CTkScrollableFrame(self, width=400, height=200)
        self.lista_despesas.place(relx=0.1, rely=0.5, relwidth=0.8, relheight=0.3)

        # Variável para armazenar o item selecionado
        self.item_selecionado = None

        bt_lancar_despesa = ctk.CTkButton(self, text="Lançar Despesa", command=self.lancar_despesa)
        bt_lancar_despesa.place(relx=0.2, rely=0.85, anchor="center")

        bt_remover_despesa = ctk.CTkButton(self, text="Remover Despesa", command=self.remover_despesa)
        bt_remover_despesa.place(relx=0.8, rely=0.85, anchor="center")

        bt_voltar_menu_despesas = ctk.CTkButton(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu_despesas.place(relx=0.5, rely=0.95, anchor="center")

        # Preparar o gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.35)

        # Armazenar dados de despesas
        self.dados_despesas = []

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
                data_formatada = datetime.datetime.strptime(data, "%d/%m/%Y").date()

                # Inserir no banco de dados
                self.cursor.execute("""
                    INSERT INTO despesas (valor, data, local, tipo_pagamento, tipo, descricao) 
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (valor_float, data_formatada.strftime("%d/%m/%Y"), local, tipo_pagamento, tipo, descricao))
                self.conn.commit()
                despesa_id = self.cursor.lastrowid

                # Adicionar na lista
                self.dados_despesas.append((data_formatada, valor_float))
                self.adicionar_item_lista(despesa_id, valor_float, data_formatada.strftime("%d/%m/%Y"), local, tipo_pagamento, tipo, descricao)
                self.atualizar_grafico()

                # Limpa os campos de entrada
                self.entrada_valor_despesa.delete(0, ctk.END)
                self.entrada_data_despesa.delete(0, ctk.END)
                self.entrada_descricao_despesa.delete(0, ctk.END)
                self.entrada_local_despesa.delete(0, ctk.END)
                self.entrada_tipo_pagamento_despesa.delete(0, ctk.END)
                self.entrada_tipo_despesa.delete(0, ctk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o valor.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def adicionar_item_lista(self, despesa_id, valor, data, local, tipo_pagamento, tipo, descricao):
        item_frame = ctk.CTkFrame(self.lista_despesas)
        item_frame.pack(fill="x", padx=10, pady=5)
        
        item_label = ctk.CTkLabel(
            item_frame, 
            text=f"ID: {despesa_id} | Valor: R$ {valor:.2f}, Data: {data}, Local: {local}, Tipo Pagamento: {tipo_pagamento}, Tipo: {tipo}, Descrição: {descricao}",
            anchor="w"
        )
        item_label.pack(side="left", expand=True, fill="x")
        
        select_button = ctk.CTkButton(
            item_frame, 
            text="Selecionar", 
            width=10, 
            command=lambda f=item_frame, id=despesa_id: self.selecionar_item(f, id)
        )
        select_button.pack(side="right")

    def selecionar_item(self, item_frame, despesa_id):
        # Remove a seleção anterior (se houver)
        if self.item_selecionado:
            self.item_selecionado['frame'].configure(fg_color="transparent")
        
        # Destaca o item selecionado
        item_frame.configure(fg_color="blue")
        self.item_selecionado = {'frame': item_frame, 'id': despesa_id}

    def remover_despesa(self):
        if self.item_selecionado:
            despesa_id = self.item_selecionado['id']
            try:
                # Remover do banco de dados
                self.cursor.execute("DELETE FROM despesas WHERE id = ?", (despesa_id,))
                self.conn.commit()

                # Remover da lista de dados
                self.dados_despesas = [r for r in self.dados_despesas if r[0] != 
                                       datetime.datetime.strptime(
                                           self.item_selecionado['frame'].winfo_children()[0].cget("text").split(", ")[1].split(": ")[1] , 
                                           "%d/%m/%Y"
                                       ).date() or r[1] != float(
                                           self.item_selecionado['frame'].winfo_children()[0].cget("text").split(", ")[0].split(": ")[1].replace("R$ ", "")
                                       )]
                
                # Remove o item selecionado da interface
                self.item_selecionado['frame'].destroy()
                self.item_selecionado = None
                self.atualizar_grafico()
                messagebox.showinfo("Sucesso", "Despesa removida com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showerror("Erro", "Nenhuma despesa selecionada para remover.")

    def atualizar_grafico(self):
        self.ax.clear()
        if self.dados_despesas:
            despesas_por_mes = {}
            for data, valor in self.dados_despesas:
                mes = data.strftime("%Y-%m")
                if mes in despesas_por_mes:
                    despesas_por_mes[mes] += valor
                else:
                    despesas_por_mes[mes] = valor
            meses = sorted(despesas_por_mes.keys())
            valores = [despesas_por_mes[mes] for mes in meses]
            self.ax.bar(meses, valores)
            self.ax.set_xlabel("Data")
            self.ax.set_ylabel("Valor (R$)")
            self.ax.set_title("Despesas Mensais")
        self.canvas.draw()



class FrameMoney(ctk.CTkFrame):
    def __init__(self, master, conn, cursor):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)
        
        # Formatar campos de data automaticamente
        self.data_var = tk.StringVar()
        self.master.formatar_campo_data(self.data_var)

        lb_money = ctk.CTkLabel(self, text="DINHEIRO GUARDADO", font=("", 20))
        lb_money.pack(pady=10)

        lb_valor_money = ctk.CTkLabel(self, text="Valor:")
        lb_valor_money.place(relx=0.1, rely=0.2)
        self.entrada_valor_money = ctk.CTkEntry(self)
        self.entrada_valor_money.place(relx=0.3, rely=0.2)

        lb_rendimento_money = ctk.CTkLabel(self, text="Rendimento Anual (%):")
        lb_rendimento_money.place(relx=0.1, rely=0.3)
        self.entrada_rendimento_money = ctk.CTkEntry(self)
        self.entrada_rendimento_money.place(relx=0.3, rely=0.3)

        lb_data_money = ctk.CTkLabel(self, text="Data (dd/mm/yyyy):")
        lb_data_money.place(relx=0.1, rely=0.4)
        self.entrada_data_money = ctk.CTkEntry(self, textvariable=self.data_var)
        self.entrada_data_money.place(relx=0.3, rely=0.4)

        self.lb_total_investido = ctk.CTkLabel(self, text=f"Total Investido: R$ 0.00", font=("", 15))
        self.lb_total_investido.place(relx=0.5, rely=0.65, anchor="center")

        bt_lancar_money = ctk.CTkButton(self, text="Lançar", command=self.lancar_money)
        bt_lancar_money.place(relx=0.5, rely=0.75, anchor="center")

        bt_voltar_menu_money = ctk.CTkButton(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu_money.place(relx=0.5, rely=0.85, anchor="center")

        # Preparar o gráfico
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().place(relx=0.5, rely=0.1, relwidth=0.4, relheight=0.4)

        # Armazenar dados dos investimentos
        self.dados_investimentos = []

    def lancar_money(self):
        valor = self.entrada_valor_money.get().strip()
        rendimento = self.entrada_rendimento_money.get().strip()
        data = self.entrada_data_money.get().strip()

        if valor and rendimento and data:
            try:
                valor_float = float(valor)
                rendimento_anual = float(rendimento)
                data_formatada = datetime.datetime.strptime(data, "%d/%m/%Y").date()
                
                # Inserir no banco de dados (exemplo, ajuste conforme necessário)
                # self.cursor.execute("INSERT INTO money (valor, rendimento, data) VALUES (?, ?, ?)", 
                #                     (valor_float, rendimento_anual, data_formatada.strftime("%d/%m/%Y")))
                # self.conn.commit()

                # Armazenar os dados do investimento
                self.dados_investimentos.append((data_formatada, valor_float, rendimento_anual))
                self.atualizar_grafico()

                # Atualizar o total investido
                total_investido = sum([inv[1] for inv in self.dados_investimentos])
                self.lb_total_investido.configure(text=f"Total Investido: R$ {total_investido:.2f}")

                # Limpa os campos de entrada
                self.entrada_valor_money.delete(0, tk.END)
                self.entrada_rendimento_money.delete(0, tk.END)
                self.entrada_data_money.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira valores numéricos válidos para o valor e rendimento.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def atualizar_grafico(self):
        self.ax.clear()

        if self.dados_investimentos:
            # Encontrar a data inicial mais antiga e a data final (hoje)
            data_inicial = min(inv[0] for inv in self.dados_investimentos)
            data_final = datetime.date.today()

            # Criar lista de datas mensais
            datas_mensais = []
            valores_mensais = []

            # Iterar sobre os meses a partir da data inicial até a data final
            data_atual = data_inicial.replace(day=1)
            while data_atual <= data_final:
                datas_mensais.append(data_atual)
                
                # Calcular valor acumulado para cada investimento nesta data
                valor_total_mes = 0
                for investimento in self.dados_investimentos:
                    if investimento[0] <= data_atual:
                        dias_desde_investimento = (data_atual - investimento[0]).days
                        
                        # Cálculo com rendimento diário
                        taxa_diaria = (1 + (investimento[2] / 100)) ** (1/365) - 1
                        valor_acumulado = investimento[1] * ((1 + taxa_diaria) ** dias_desde_investimento)
                        
                        valor_total_mes += valor_acumulado

                valores_mensais.append(valor_total_mes)
                
                # Avançar para o próximo mês
                if data_atual.month == 12:
                    data_atual = data_atual.replace(year=data_atual.year + 1, month=1)
                else:
                    data_atual = data_atual.replace(month=data_atual.month + 1)

            # Plotar gráfico
            self.ax.plot(datas_mensais, valores_mensais, marker='o')
            self.ax.set_xlabel("Data")
            self.ax.set_ylabel("Valor Acumulado (R$)")
            self.ax.set_title("Evolução Mensal do Patrimônio")
            
            # Formatar datas no eixo X
            self.ax.xaxis.set_major_locator(mdates.MonthLocator())
            self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')

            # Atualizar total investido exibido
            total_investido = valores_mensais[-1]
            self.lb_total_investido.configure(text=f"Total Investido: R$ {total_investido:.2f}")

        self.canvas.draw()


class FrameCard(ctk.CTkFrame):
    def __init__(self, master, conn, cursor):
        super().__init__(master)
        self.master = master
        self.conn = conn
        self.cursor = cursor
        self.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)

        lb_card = ctk.CTkLabel(self, text="CARTÕES", font=("", 20))
        lb_card.pack(pady=10)

        lb_nome_cartao = ctk.CTkLabel(self, text="Nome:")
        lb_nome_cartao.place(relx=0.1, rely=0.15)
        self.entrada_nome_cartao = ctk.CTkEntry(self)
        self.entrada_nome_cartao.place(relx=0.3, rely=0.15)

        lb_bandeira_cartao = ctk.CTkLabel(self, text="Bandeira:")
        lb_bandeira_cartao.place(relx=0.1, rely=0.25)
        self.entrada_bandeira_cartao = ctk.CTkEntry(self)
        self.entrada_bandeira_cartao.place(relx=0.3, rely=0.25)

        lb_limite_cartao = ctk.CTkLabel(self, text="Limite:")
        lb_limite_cartao.place(relx=0.1, rely=0.35)
        self.entrada_limite_cartao = ctk.CTkEntry(self)
        self.entrada_limite_cartao.place(relx=0.3, rely=0.35)

        lb_fatura_cartao = ctk.CTkLabel(self, text="Fatura:")
        lb_fatura_cartao.place(relx=0.1, rely=0.45)
        self.entrada_fatura_cartao = ctk.CTkEntry(self)
        self.entrada_fatura_cartao.place(relx=0.3, rely=0.45)

        self.lista_cartoes = ctk.CTkScrollableFrame(self, width=400, height=200)
        self.lista_cartoes.place(relx=0.1, rely=0.55, relwidth=0.8, relheight=0.3)

        bt_lancar_cartao = ctk.CTkButton(self, text="Lançar Cartão", command=self.lancar_cartao)
        bt_lancar_cartao.place(relx=0.2, rely=0.88, anchor="center")

        bt_pagar_fatura = ctk.CTkButton(self, text="Pagar Fatura", command=self.pagar_fatura)
        bt_pagar_fatura.place(relx=0.5, rely=0.88, anchor="center")

        bt_remover_cartao = ctk.CTkButton(self, text="Remover Cartão", command=self.remover_cartao)
        bt_remover_cartao.place(relx=0.8, rely=0.88, anchor="center")

        bt_voltar_menu_card = ctk.CTkButton(self, text="Voltar", command=lambda: master.mostrar_frame(master.frame_menu))
        bt_voltar_menu_card.place(relx=0.5, rely=0.95, anchor="center")

        self.item_selecionado = None

    def lancar_cartao(self):
        nome = self.entrada_nome_cartao.get().strip()
        bandeira = self.entrada_bandeira_cartao.get().strip()
        limite = self.entrada_limite_cartao.get().strip()
        fatura = self.entrada_fatura_cartao.get().strip()

        if nome and bandeira and limite and fatura:
            try:
                limite_float = float(limite)
                # Inserir no banco de dados (exemplo, ajuste conforme necessário)
                # self.cursor.execute("INSERT INTO cartoes (nome, bandeira, limite, fatura) VALUES (?, ?, ?, ?)", 
                #                     (nome, bandeira, limite_float, fatura))
                # self.conn.commit()

                # Cria um frame para cada item (para permitir seleção)
                item_frame = ctk.CTkFrame(self.lista_cartoes)
                item_frame.pack(fill="x", padx=10, pady=5)
                
                # Label com as informações
                item_label = ctk.CTkLabel(
                    item_frame, 
                    text=f"Nome: {nome}, Bandeira: {bandeira}, Limite: R$ {limite_float:.2f}, Fatura: {fatura}",
                    anchor="w"
                )
                item_label.pack(side="left", expand=True, fill="x")
                
                # Botão de seleção para cada item
                select_button = ctk.CTkButton(
                    item_frame, 
                    text="Selecionar", 
                    width=10, 
                    command=lambda f=item_frame: self.selecionar_item(f)
                )
                select_button.pack(side="right")

                # Limpa os campos de entrada
                self.entrada_nome_cartao.delete(0, ctk.END)
                self.entrada_bandeira_cartao.delete(0, ctk.END)
                self.entrada_limite_cartao.delete(0, ctk.END)
                self.entrada_fatura_cartao.delete(0, ctk.END)
            except ValueError:
                messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para o limite.")
        else:
            messagebox.showwarning("Atenção", "Por favor, preencha todos os campos.")

    def selecionar_item(self, item_frame):
        # Remove a seleção anterior (se houver)
        if self.item_selecionado:
            self.item_selecionado.configure(fg_color="transparent")
        
        # Destaca o item selecionado
        item_frame.configure(fg_color="blue")
        self.item_selecionado = item_frame

    def pagar_fatura(self):
        if self.item_selecionado:
            item_label = self.item_selecionado.winfo_children()[0]
            current_text = item_label.cget("text")
            if " - Fatura paga" not in current_text:
                updated_text = current_text + " - Fatura paga"
                item_label.configure(text=updated_text)
                messagebox.showinfo("Sucesso", "Fatura paga com sucesso.")
            else:
                messagebox.showinfo("Informação", "Fatura já está paga.")
        else:
            messagebox.showerror("Erro", "Nenhum cartão selecionado para pagar a fatura.")

    def remover_cartao(self):
        if self.item_selecionado:
            # Remover do banco de dados (exemplo, ajuste conforme necessário)
            # self.cursor.execute("DELETE FROM cartoes WHERE id = ?", (cartao_id,))
            # self.conn.commit()

            # Remover o item selecionado da interface
            self.item_selecionado.destroy()
            self.item_selecionado = None
            messagebox.showinfo("Sucesso", "Cartão removido com sucesso.")
        else:
            messagebox.showerror("Erro", "Nenhum cartão selecionado para remover.")


# Inicializar a aplicação
if __name__ == "__main__":
    app = GestorFinanceiro()
    app.after(0, lambda: app.state('zoomed'))
    app.mainloop()
