from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error


class Login:
    def __init__(self):
        self.janela_login = Tk()
        self.janela_login.title('Login')
        self.janela_login.geometry('300x220')
        self.janela_login.configure(background='#1e3743')

        self.label_usuario = Label(self.janela_login, text='Usuário', bg='#1e3743', fg='white')
        self.label_usuario.pack(pady=10)

        self.entry_usuario = Entry(self.janela_login)
        self.entry_usuario.pack(pady=5)

        self.label_senha = Label(self.janela_login, text='Senha', bg='#1e3743', fg='white')
        self.label_senha.pack(pady=10)

        self.entry_senha = Entry(self.janela_login, show='*')
        self.entry_senha.pack(pady=5)

        self.btn_login = Button(self.janela_login, text='Login', command=self.login, bg='#107bd2', fg='white')
        self.btn_login.pack(pady=10)

        self.btn_cadastrar = Button(self.janela_login, text='Cadastrar', command=self.abrir_cadastro, bg='#28a745', fg='white')
        self.btn_cadastrar.pack(pady=5)

        self.criar_tabela_usuarios()

        self.janela_login.mainloop()

    def criar_tabela_usuarios(self):
        try:
            conn = mysql.connector.connect(host='localhost', database='NeoStock', user='root', password='toor')
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(50) NOT NULL,
                    usuario VARCHAR(50) NOT NULL UNIQUE,
                    telefone VARCHAR(15),
                    senha VARCHAR(50) NOT NULL
                );
            ''')
            conn.commit()
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao MySQL: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        if not usuario or not senha:
            messagebox.showwarning("Entrada inválida", "Preencha todos os campos.")
            return

        try:
            conn = mysql.connector.connect(host='localhost', database='NeoStock', user='root', password='toor')
            cursor = conn.cursor()
            cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao MySQL: {str(e)}")
            return
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

        if resultado and resultado[0] == senha:
            messagebox.showinfo("Login", "Login realizado com sucesso!")
            self.janela_login.destroy()
            AppLication()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def abrir_cadastro(self):
        self.janela_cadastro = Toplevel(self.janela_login)
        self.janela_cadastro.title("Cadastro")
        self.janela_cadastro.geometry('350x350')
        self.janela_cadastro.configure(background='#1e3743')

        Label(self.janela_cadastro, text="Nome:", bg='#1e3743', fg='white').pack(pady=5)
        self.entry_nome = Entry(self.janela_cadastro)
        self.entry_nome.pack(pady=5)

        Label(self.janela_cadastro, text="Usuário:", bg='#1e3743', fg='white').pack(pady=5)
        self.entry_usuario_cad = Entry(self.janela_cadastro)
        self.entry_usuario_cad.pack(pady=5)

        Label(self.janela_cadastro, text="Telefone:", bg='#1e3743', fg='white').pack(pady=5)
        self.entry_telefone = Entry(self.janela_cadastro)
        self.entry_telefone.pack(pady=5)

        Label(self.janela_cadastro, text="Senha:", bg='#1e3743', fg='white').pack(pady=5)
        self.entry_senha_cad = Entry(self.janela_cadastro, show='*')
        self.entry_senha_cad.pack(pady=5)

        Label(self.janela_cadastro, text="Confirmar Senha:", bg='#1e3743', fg='white').pack(pady=5)
        self.entry_confirma_senha = Entry(self.janela_cadastro, show='*')
        self.entry_confirma_senha.pack(pady=5)

        Button(self.janela_cadastro, text="Cadastrar", bg='#107bd2', fg='white',
               command=self.cadastrar_usuario).pack(pady=15)

    def cadastrar_usuario(self):
        nome = self.entry_nome.get().strip()
        usuario = self.entry_usuario_cad.get().strip()
        telefone = self.entry_telefone.get().strip()
        senha = self.entry_senha_cad.get().strip()
        confirma_senha = self.entry_confirma_senha.get().strip()

        if not nome or not usuario or not senha or not confirma_senha:
            messagebox.showwarning("Entrada inválida", "Preencha todos os campos obrigatórios.")
            return

        if senha != confirma_senha:
            messagebox.showwarning("Erro", "As senhas não conferem.")
            return

        try:
            conn = mysql.connector.connect(host='localhost', database='NeoStock', user='root', password='toor')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO usuarios (nome, usuario, telefone, senha)
                VALUES (%s, %s, %s, %s)
            ''', (nome, usuario, telefone, senha))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            self.janela_cadastro.destroy()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Erro", "Usuário já existe. Escolha outro nome.")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao MySQL: {str(e)}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


class Funcs:
    def limpa_tela(self, aba=1):
        if aba == 1:
            self.codigo_entry.delete(0, END)
            self.produto_entry.delete(0, END)
            self.quantidade_entry.delete(0, END)
            self.preco_unitario_entry.delete(0, END)
            self.preco_total_entry.config(state='normal')
            self.preco_total_entry.delete(0, END)
            self.preco_total_entry.config(state='readonly')
        else:
            self.codigo_entry_2.delete(0, END)
            self.nome_entry_2.delete(0, END)
            self.cnpj_entry_2.delete(0, END)
            self.telefone_entry_2.delete(0, END)
            self.produto_entry_2.delete(0, END)

    def conecta_bd_produtos(self):
        self.conn_produtos = mysql.connector.connect(host='localhost', database='NeoStock', user='root', password='toor')
        self.cursor_produtos = self.conn_produtos.cursor()

    def desconecta_bd_produtos(self):
        if self.conn_produtos.is_connected():
            self.cursor_produtos.close()
            self.conn_produtos.close()

    def conecta_bd_fornecedores(self):
        self.conn_fornecedores = mysql.connector.connect(host='localhost', database='NeoStock', user='root', password='toor')
        self.cursor_fornecedores = self.conn_fornecedores.cursor()

    def desconecta_bd_fornecedores(self):
        if self.conn_fornecedores.is_connected():
            self.cursor_fornecedores.close()
            self.conn_fornecedores.close()

    def montaTabelas(self):
        self.conecta_bd_produtos()
        self.cursor_produtos.execute('DROP TABLE IF EXISTS produtos;')
        self.cursor_produtos.execute('''
            CREATE TABLE produtos (
                cod INT AUTO_INCREMENT PRIMARY KEY,
                produto VARCHAR(50) NOT NULL,
                quantidade INT,
                preco_unitario DECIMAL(10,2),
                preco_total DECIMAL(10,2)
            );
        ''')
        self.conn_produtos.commit()
        self.desconecta_bd_produtos()

        self.conecta_bd_fornecedores()
        self.cursor_fornecedores.execute('''
            CREATE TABLE IF NOT EXISTS fornecedores (
                cod INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(50) NOT NULL,
                cnpj VARCHAR(20) NOT NULL UNIQUE,
                telefone VARCHAR(15),
                produto VARCHAR(50)
            );
        ''')
        self.conn_fornecedores.commit()
        self.desconecta_bd_fornecedores()

    def variaveis_produtos(self):
        self.codigo = self.codigo_entry.get().strip()
        self.produto = self.produto_entry.get().strip()
        self.quantidade = self.quantidade_entry.get().strip()
        self.preco_unitario = self.preco_unitario_entry.get().strip()
        self.conecta_bd_produtos()

    def calcula_preco_total(self):
        try:
            quantidade_int = int(self.quantidade) if self.quantidade.isdigit() else 0
            preco_float = float(self.preco_unitario.replace(',', '.')) if self.preco_unitario.replace(',', '.', 1).replace('.', '', 1).isdigit() else 0.0
            return round(quantidade_int * preco_float, 2)
        except:
            return 0.0

    def add_produto(self):
        self.variaveis_produtos()
        if not self.produto:
            messagebox.showwarning("Erro", "Preencha o campo Produto!")
            self.desconecta_bd_produtos()
            return
        try:
            quantidade_int = int(self.quantidade) if self.quantidade.isdigit() else 0
            preco_unitario_float = float(self.preco_unitario.replace(',', '.')) if self.preco_unitario.replace(',', '.', 1).replace('.', '', 1).isdigit() else 0.0
            preco_total_float = self.calcula_preco_total()
            self.cursor_produtos.execute('''
                INSERT INTO produtos (produto, quantidade, preco_unitario, preco_total)
                VALUES (%s, %s, %s, %s)
            ''', (self.produto, quantidade_int, preco_unitario_float, preco_total_float))
            self.conn_produtos.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.select_lista_produtos()
            self.limpa_tela(aba=1)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar o produto: {str(e)}")
        finally:
            self.desconecta_bd_produtos()

    def select_lista_produtos(self):
        self.listaProdutos.delete(*self.listaProdutos.get_children())
        self.conecta_bd_produtos()
        self.cursor_produtos.execute('''
            SELECT cod, produto, quantidade, preco_unitario, preco_total FROM produtos
            ORDER BY produto ASC;
        ''')
        lista = self.cursor_produtos.fetchall()
        for i in lista:
            self.listaProdutos.insert('', END, values=i)
        self.desconecta_bd_produtos()

    def OnDoubleClick_produtos(self, event):
        self.limpa_tela(aba=1)
        for selection in self.listaProdutos.selection():
            col1, col2, col3, col4, col5 = self.listaProdutos.item(selection, 'values')
            self.codigo_entry.insert(END, col1)
            self.produto_entry.insert(END, col2)
            self.quantidade_entry.insert(END, col3)
            self.preco_unitario_entry.insert(END, col4)
            self.preco_total_entry.config(state='normal')
            self.preco_total_entry.delete(0, END)
            self.preco_total_entry.insert(END, col5)
            self.preco_total_entry.config(state='readonly')

    def deleta_produto(self):
        self.variaveis_produtos()
        if not self.codigo:
            messagebox.showwarning("Erro", "Selecione um produto para apagar!")
            return
        self.conecta_bd_produtos()
        self.cursor_produtos.execute('DELETE FROM produtos WHERE cod = %s', (self.codigo,))
        self.conn_produtos.commit()
        self.desconecta_bd_produtos()
        messagebox.showinfo("Sucesso", "Produto apagado com sucesso!")
        self.limpa_tela(aba=1)
        self.select_lista_produtos()

    def altera_produto(self):
        self.variaveis_produtos()
        if not self.codigo:
            messagebox.showwarning("Erro", "Selecione um produto para alterar!")
            return
        if not self.produto:
            messagebox.showwarning("Erro", "Preencha o campo Produto!")
            return
        try:
            quantidade_int = int(self.quantidade) if self.quantidade.isdigit() else 0
            preco_unitario_float = float(self.preco_unitario.replace(',', '.')) if self.preco_unitario.replace(',', '.', 1).replace('.', '', 1).isdigit() else 0.0
            preco_total_float = self.calcula_preco_total()
            self.cursor_produtos.execute('''
                UPDATE produtos SET produto = %s, quantidade = %s, preco_unitario = %s, preco_total = %s
                WHERE cod = %s
            ''', (self.produto, quantidade_int, preco_unitario_float, preco_total_float, self.codigo))
            self.conn_produtos.commit()
            messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
            self.select_lista_produtos()
            self.limpa_tela(aba=1)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar produto: {str(e)}")
        finally:
            self.desconecta_bd_produtos()

    def busca_produto(self):
        self.conecta_bd_produtos()
        self.listaProdutos.delete(*self.listaProdutos.get_children())
        nome = self.produto_entry.get().strip()

        if nome:
            self.cursor_produtos.execute('''
                SELECT cod, produto, quantidade, preco_unitario, preco_total FROM produtos
                WHERE produto LIKE %s
                ORDER BY produto ASC
            ''', ('%' + nome + '%',))
        else:
            self.cursor_produtos.execute('''
                SELECT cod, produto, quantidade, preco_unitario, preco_total FROM produtos
                ORDER BY produto ASC
            ''')

        buscanome = self.cursor_produtos.fetchall()
        for i in buscanome:
            self.listaProdutos.insert('', END, values=i)

        self.limpa_tela(aba=1)
        self.desconecta_bd_produtos()

    def variaveis_fornecedores(self):
        self.codigo = self.codigo_entry_2.get().strip()
        self.nome = self.nome_entry_2.get().strip()
        self.cnpj = self.cnpj_entry_2.get().strip()
        self.telefone = self.telefone_entry_2.get().strip()
        self.produto = self.produto_entry_2.get().strip()
        self.conecta_bd_fornecedores()

    def add_fornecedor(self):
        self.variaveis_fornecedores()

        if not self.nome or not self.cnpj:
            messagebox.showwarning("Erro", "Nome e CNPJ são obrigatórios!")
            self.desconecta_bd_fornecedores()
            return

        try:
            self.cursor_fornecedores.execute('''
                INSERT INTO fornecedores (nome, cnpj, telefone, produto)
                VALUES (%s, %s, %s, %s)
            ''', (self.nome, self.cnpj, self.telefone, self.produto))
            self.conn_fornecedores.commit()
            messagebox.showinfo("Sucesso", "Fornecedor cadastrado com sucesso!")
            self.limpa_tela(aba=2)
            self.select_lista_fornecedores()
        except mysql.connector.IntegrityError:
            messagebox.showerror("Erro", "CNPJ já existe. Escolha outro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar fornecedor: {str(e)}")
        finally:
            self.desconecta_bd_fornecedores()

    def select_lista_fornecedores(self):
        self.listaFornecedores.delete(*self.listaFornecedores.get_children())
        self.conecta_bd_fornecedores()
        self.cursor_fornecedores.execute('''
            SELECT cod, nome, cnpj, telefone, produto FROM fornecedores
            ORDER BY nome ASC;
        ''')
        lista = self.cursor_fornecedores.fetchall()
        for i in lista:
            self.listaFornecedores.insert('', END, values=i)
        self.desconecta_bd_fornecedores()

    def OnDoubleClick_fornecedores(self, event):
        self.limpa_tela(aba=2)
        for selection in self.listaFornecedores.selection():
            col1, col2, col3, col4, col5 = self.listaFornecedores.item(selection, 'values')
            self.codigo_entry_2.insert(END, col1)
            self.nome_entry_2.insert(END, col2)
            self.cnpj_entry_2.insert(END, col3)
            self.telefone_entry_2.insert(END, col4)
            self.produto_entry_2.insert(END, col5)

    def deleta_fornecedor(self):
        self.variaveis_fornecedores()
        if not self.codigo:
            messagebox.showwarning("Erro", "Selecione um fornecedor para apagar!")
            self.desconecta_bd_fornecedores()
            return
        self.conecta_bd_fornecedores()
        self.cursor_fornecedores.execute('DELETE FROM fornecedores WHERE cod = %s', (self.codigo,))
        self.conn_fornecedores.commit()
        self.desconecta_bd_fornecedores()
        messagebox.showinfo("Sucesso", "Fornecedor apagado com sucesso!")
        self.limpa_tela(aba=2)
        self.select_lista_fornecedores()

    def altera_fornecedor(self):
        self.variaveis_fornecedores()
        if not self.codigo:
            messagebox.showwarning("Erro", "Selecione um fornecedor para alterar!")
            self.desconecta_bd_fornecedores()
            return
        if not self.nome or not self.cnpj:
            messagebox.showwarning("Erro", "Nome e CNPJ são obrigatórios!")
            self.desconecta_bd_fornecedores()
            return
        self.conecta_bd_fornecedores()
        try:
            self.cursor_fornecedores.execute('''
                UPDATE fornecedores SET nome = %s, cnpj = %s, telefone = %s, produto = %s
                WHERE cod = %s
            ''', (self.nome, self.cnpj, self.telefone, self.produto, self.codigo))
            self.conn_fornecedores.commit()
            messagebox.showinfo("Sucesso", "Fornecedor alterado com sucesso!")
            self.select_lista_fornecedores()
            self.limpa_tela(aba=2)
        except mysql.connector.IntegrityError:
            messagebox.showerror("Erro", "CNPJ já existe. Escolha outro.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao alterar fornecedor: {str(e)}")
        finally:
            self.desconecta_bd_fornecedores()

    def busca_fornecedor(self):
        self.conecta_bd_fornecedores()
        self.listaFornecedores.delete(*self.listaFornecedores.get_children())
        nome = self.nome_entry_2.get().strip()

        if nome:
            self.cursor_fornecedores.execute('''
                SELECT cod, nome, cnpj, telefone, produto FROM fornecedores
                WHERE nome LIKE %s
                ORDER BY nome ASC
            ''', ('%' + nome + '%',))
        else:
            self.cursor_fornecedores.execute('''
                SELECT cod, nome, cnpj, telefone, produto FROM fornecedores
                ORDER BY nome ASC
            ''')

        buscanome = self.cursor_fornecedores.fetchall()
        for i in buscanome:
            self.listaFornecedores.insert('', END, values=i)

        self.limpa_tela(aba=2)
        self.desconecta_bd_fornecedores()


class AppLication(Funcs):
    def __init__(self):
        self.janela = Tk()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista_produtos()
        self.select_lista_fornecedores()
        self.Menus()
        self.abas.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        self.janela.mainloop()

    def tela(self):
        self.janela.title('Cadastro de produtos e fornecedores')
        self.janela.configure(background='#1e3743')
        self.janela.geometry('800x600')
        self.janela.maxsize(900, 700)
        self.janela.minsize(600, 400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.janela, bd=1, bg='gray95',
                             highlightbackground='black', highlightthickness=3)
        self.frame_1.pack_propagate(FALSE)
        self.frame_1.pack(padx=13, pady=13, fill=BOTH, expand=YES)

    def widgets_frame1(self):
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba1.configure(background='gray95')
        self.aba2.configure(background='gray95')
        self.abas.add(self.aba1, text='Cadastro de Produtos')
        self.abas.add(self.aba2, text='Fornecedores')
        self.abas.pack(fill=BOTH, expand=YES)

        self.bt_limpar = Button(self.aba1, text='Limpar', bd=2, bg='#107bd2', fg='white',
                                font=('verdana', 8, 'bold'),
                                command=lambda: self.limpa_tela(aba=1))
        self.bt_limpar.place(relx=0.2, rely=0.03, relwidth=0.1, relheight=0.08)

        self.bt_procurar = Button(self.aba1, text='Procurar', bd=2, bg='#107bd2', fg='white',
                                  font=('verdana', 8, 'bold'), command=self.busca_produto)
        self.bt_procurar.place(relx=0.3, rely=0.03, relwidth=0.1, relheight=0.08)

        self.bt_novo = Button(self.aba1, text='Novo', bd=2, bg='#107bd2', fg='white',
                              font=('verdana', 8, 'bold'), command=self.add_produto)
        self.bt_novo.place(relx=0.6, rely=0.03, relwidth=0.1, relheight=0.08)

        self.bt_alterar = Button(self.aba1, text='Alterar', bd=2, bg='#107bd2', fg='white',
                                 font=('verdana', 8, 'bold'), command=self.altera_produto)
        self.bt_alterar.place(relx=0.7, rely=0.03, relwidth=0.1, relheight=0.08)

        self.bt_apagar = Button(self.aba1, text='Apagar', bd=2, bg='red', fg='white',
                                font=('verdana', 8, 'bold'), command=self.deleta_produto)
        self.bt_apagar.place(relx=0.8, rely=0.03, relwidth=0.1, relheight=0.08)

        self.lb_codigo = Label(self.aba1, text='Código', bg='gray95')
        self.lb_codigo.place(relx=0.05, rely=0.20)

        self.codigo_entry = Entry(self.aba1)
        self.codigo_entry.place(relx=0.05, rely=0.24, relwidth=0.08)

        self.lb_produto = Label(self.aba1, text='Produto', bg='gray95')
        self.lb_produto.place(relx=0.05, rely=0.33)

        self.produto_entry = Entry(self.aba1)
        self.produto_entry.place(relx=0.05, rely=0.37, relwidth=0.5)

        self.lb_quantidade = Label(self.aba1, text='Quantidade', bg='gray95')
        self.lb_quantidade.place(relx=0.05, rely=0.43)

        self.quantidade_entry = Entry(self.aba1)
        self.quantidade_entry.place(relx=0.05, rely=0.48, relwidth=0.1)

        self.lb_preco_unitario = Label(self.aba1, text='Preço Unitário', bg='gray95')
        self.lb_preco_unitario.place(relx=0.20, rely=0.43)

        self.preco_unitario_entry = Entry(self.aba1)
        self.preco_unitario_entry.place(relx=0.20, rely=0.48, relwidth=0.1)

        self.lb_preco_total = Label(self.aba1, text='Preço Total', bg='gray95')
        self.lb_preco_total.place(relx=0.38, rely=0.43)

        self.preco_total_entry = Entry(self.aba1, state='readonly')
        self.preco_total_entry.place(relx=0.38, rely=0.48, relwidth=0.15)

        self.bt_limpar_2 = Button(self.aba2, text='Limpar', bd=2, bg='#107bd2', fg='white',
                                  font=('verdana', 8, 'bold'), command=lambda: self.limpa_tela(aba=2))
        self.bt_limpar_2.place(relx=0.2, rely=0.04, relwidth=0.1, relheight=0.1)

        self.bt_procurar_2 = Button(self.aba2, text='Procurar', bd=2, bg='#107bd2', fg='white',
                                    font=('verdana', 8, 'bold'), command=self.busca_fornecedor)
        self.bt_procurar_2.place(relx=0.3, rely=0.04, relwidth=0.1, relheight=0.1)

        self.bt_novo_2 = Button(self.aba2, text='Novo', bd=2, bg='#107bd2', fg='white',
                                font=('verdana', 8, 'bold'), command=self.add_fornecedor)
        self.bt_novo_2.place(relx=0.6, rely=0.04, relwidth=0.1, relheight=0.1)

        self.bt_alterar_2 = Button(self.aba2, text='Alterar', bd=2, bg='#107bd2', fg='white',
                                   font=('verdana', 8, 'bold'), command=self.altera_fornecedor)
        self.bt_alterar_2.place(relx=0.7, rely=0.04, relwidth=0.1, relheight=0.1)

        self.bt_apagar_2 = Button(self.aba2, text='Apagar', bd=2, bg='red', fg='white',
                                  font=('verdana', 8, 'bold'), command=self.deleta_fornecedor)
        self.bt_apagar_2.place(relx=0.8, rely=0.04, relwidth=0.1, relheight=0.1)

        self.lb_codigo_2 = Label(self.aba2, text='Código', bg='gray95')
        self.lb_codigo_2.place(relx=0.05, rely=0.20)

        self.codigo_entry_2 = Entry(self.aba2)
        self.codigo_entry_2.place(relx=0.05, rely=0.25, relwidth=0.08)

        self.lb_nome_2 = Label(self.aba2, text='Nome', bg='gray95')
        self.lb_nome_2.place(relx=0.38, rely=0.20)

        self.nome_entry_2 = Entry(self.aba2)
        self.nome_entry_2.place(relx=0.38, rely=0.25, relwidth=0.3)

        self.lb_cnpj_2 = Label(self.aba2, text='CNPJ', bg='gray95')
        self.lb_cnpj_2.place(relx=0.05, rely=0.30)

        self.cnpj_entry_2 = Entry(self.aba2)
        self.cnpj_entry_2.place(relx=0.05, rely=0.35, relwidth=0.2)

        self.lb_telefone_2 = Label(self.aba2, text='Telefone', bg='gray95')
        self.lb_telefone_2.place(relx=0.34, rely=0.30)

        self.telefone_entry_2 = Entry(self.aba2)
        self.telefone_entry_2.place(relx=0.34, rely=0.35, relwidth=0.2)

        self.lb_produto_2 = Label(self.aba2, text='Produto', bg='gray95')
        self.lb_produto_2.place(relx=0.63, rely=0.30)

        self.produto_entry_2 = Entry(self.aba2)
        self.produto_entry_2.place(relx=0.63, rely=0.35, relwidth=0.3)

    def lista_frame1(self):
        self.listaProdutos = ttk.Treeview(self.aba1, height=10, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.listaProdutos.heading('#0', text='')
        self.listaProdutos.heading('col1', text='Código')
        self.listaProdutos.heading('col2', text='Produto')
        self.listaProdutos.heading('col3', text='Quantidade')
        self.listaProdutos.heading('col4', text='Preço Unitário')
        self.listaProdutos.heading('col5', text='Preço Total')

        self.listaProdutos.column('#0', width=0, stretch=NO)
        self.listaProdutos.column('col1', width=50)
        self.listaProdutos.column('col2', width=150)
        self.listaProdutos.column('col3', width=80)
        self.listaProdutos.column('col4', width=120)
        self.listaProdutos.column('col5', width=120)

        self.listaProdutos.place(relx=0.01, rely=0.55, relwidth=0.97, relheight=0.45)

        self.scrollLista = Scrollbar(self.aba1, orient='vertical', command=self.listaProdutos.yview)
        self.listaProdutos.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.98, rely=0.55, relwidth=0.02, relheight=0.45)

        self.listaProdutos.bind('<Double-1>', self.OnDoubleClick_produtos)

    def lista_frame2(self):
        self.listaFornecedores = ttk.Treeview(self.aba2, height=10, columns=('col1', 'col2', 'col3', 'col4', 'col5'))
        self.listaFornecedores.heading('#0', text='')
        self.listaFornecedores.heading('col1', text='Código')
        self.listaFornecedores.heading('col2', text='Nome')
        self.listaFornecedores.heading('col3', text='CNPJ')
        self.listaFornecedores.heading('col4', text='Telefone')
        self.listaFornecedores.heading('col5', text='Produto')

        self.listaFornecedores.column('#0', width=0, stretch=NO)
        self.listaFornecedores.column('col1', width=50)
        self.listaFornecedores.column('col2', width=200)
        self.listaFornecedores.column('col3', width=125)
        self.listaFornecedores.column('col4', width=125)
        self.listaFornecedores.column('col5', width=150)

        self.listaFornecedores.place(relx=0.01, rely=0.50, relwidth=0.97, relheight=0.45)

        self.scrollListaFornecedores = Scrollbar(self.aba2, orient='vertical', command=self.listaFornecedores.yview)
        self.listaFornecedores.configure(yscroll=self.scrollListaFornecedores.set)
        self.scrollListaFornecedores.place(relx=0.98, rely=0.50, relwidth=0.02, relheight=0.45)

        self.listaFornecedores.bind('<Double-1>', self.OnDoubleClick_fornecedores)

    def on_tab_changed(self, event):
        pass

    def Menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        aboutmenu = Menu(menubar)

        def Quit():
            self.janela.destroy()

        def mostrar_sobre():
            messagebox.showinfo("Sobre", "Sistema de Controle de Estoque desenvolvido como parte de um trabalho acadêmico pelos alunos: Bruno Santiago, Gabriel Morais, Richard Lucas, Gabriel Henrique.")

        menubar.add_cascade(label='Opções', menu=filemenu)
        menubar.add_cascade(label='Sobre', menu=aboutmenu)

        filemenu.add_command(label='Sair', command=Quit)
        aboutmenu.add_command(label='Info', command=mostrar_sobre)


if __name__ == '__main__':
    Login()
