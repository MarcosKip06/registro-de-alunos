from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()

class Funcs():
    def limpa_aluno(self):
        self.codigo_entry.delete(0, END)
        self.nota1_entry.delete(0, END)
        self.nota2_entry.delete(0, END)
        self.nome_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("alunos.db")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ### Criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alunos (
                cod INTEGER PRIMARY KEY,
                nome_aluno CHAR(40) NOT NULL,
                nota1 INTEGER(2),
                nota2 INTEGER(2)               
            );
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.nota1 = self.nota1_entry.get()
        self.nota2 = self.nota2_entry.get()
    def OnDoubleClick(self, event):
        self.limpa_aluno()
        self.listaAlu.selection()

        for n in self.listaAlu.selection():
            col1, col2, col3, col4 = self.listaAlu.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.nota1_entry.insert(END, col3)
            self.nota2_entry.insert(END, col4)

    def add_aluno(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO alunos (nome_aluno, nota1, nota2)
            VALUES (?, ?, ?)""", (self.nome, self.nota1, self.nota2))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_aluno()
    def altera_aluno(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE alunos SET nome_aluno = ?, nota1 = ?, nota2 = ?
            WHERE cod = ? """,
                            (self.nome, self.nota1, self.nota2, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_aluno()
    def deleta_aluno(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM alunos WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_aluno()
        self.select_lista()

    def select_lista(self):
        self.listaAlu.delete(*self.listaAlu.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_aluno, nota1, nota2 FROM alunos
            ORDER BY nome_aluno ASC; """)
        for i in lista:
            self.listaAlu.insert("", END, values=i)
        self.desconecta_bd()

    def busca_aluno(self):
        self.conecta_bd()
        self.listaAlu.delete(*self.listaAlu.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """ SELECT cod, nome_aluno, nota1, nota2 FROM alunos
            WHERE nome_aluno LIKE '%s' ORDER BY nome_aluno ASC""" % nome)
        buscanomeAlu = self.cursor.fetchall()
        for i in buscanomeAlu:
            self.listaAlu.insert("", END, values=i)
        self.limpa_aluno()
        self.desconecta_bd()


class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()

        root.mainloop()
    def tela(self):
        self.root.title("Registro de Notas")
        self.root.configure(background= '#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width= 900, height= 700)
        self.root.minsize(width=500, height= 400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee',
                             highlightbackground= '#759fe6', highlightthickness=3 )
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)

        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee',
                             highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        ### Criação do botao limpar
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.limpa_aluno)
        self.bt_limpar.place(relx= 0.2, rely=0.1, relwidth=0.1, relheight= 0.15)
        ### Criação do botao buscar
        self.bt_limpar = Button(self.frame_1, text="Buscar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.busca_aluno)
        self.bt_limpar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao novo
        self.bt_limpar = Button(self.frame_1, text="Novo", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command= self.add_aluno)
        self.bt_limpar.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao alterar
        self.bt_limpar = Button(self.frame_1, text="Alterar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.altera_aluno)
        self.bt_limpar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)
        ### Criação do botao apagar
        self.bt_limpar = Button(self.frame_1, text="Apagar", bd=2, bg = '#107db2',fg = 'white'
                                , font = ('verdana', 8, 'bold'), command=self.deleta_aluno)
        self.bt_limpar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        ## Criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
        self.lb_codigo.place(relx= 0.05, rely= 0.05 )

        self.codigo_entry = Entry(self.frame_1 )
        self.codigo_entry.place(relx= 0.05, rely= 0.15, relwidth= 0.08)

        ## Criação da label e entrada do nome
        self.lb_nome = Label(self.frame_1, text="Nome", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx=0.05, rely=0.35)

        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.05, rely=0.45, relwidth=0.8)

        ## Criação da label e entrada do telefone
        self.lb_nota1 = Label(self.frame_1, text="Nota 1", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nota1.place(relx=0.05, rely=0.6)

        self.nota1_entry = Entry(self.frame_1)
        self.nota1_entry.place(relx=0.05, rely=0.7, relwidth=0.08)

        ## Criação da label e entrada da cidade
        self.lb_nota2 = Label(self.frame_1, text="Nota 2", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nota2.place(relx=0.5, rely=0.6)

        self.nota2_entry = Entry(self.frame_1)
        self.nota2_entry.place(relx=0.5, rely=0.7, relwidth=0.08)
    def lista_frame2(self):
        self.listaAlu = ttk.Treeview(self.frame_2, height=3,
                                     column=("col1", "col2", "col3", "col4"))
        self.listaAlu.heading("#0", text="")
        self.listaAlu.heading("#1", text="Codigo")
        self.listaAlu.heading("#2", text="Nome")
        self.listaAlu.heading("#3", text="Nota 1")
        self.listaAlu.heading("#4", text="Nota 2")
        self.listaAlu.column("#0", width=1)
        self.listaAlu.column("#1", width=50)
        self.listaAlu.column("#2", width=200)
        self.listaAlu.column("#3", width=125)
        self.listaAlu.column("#4", width=125)
        self.listaAlu.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaAlu.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.96, rely=0.1, relwidth=0.04, relheight=0.85)
        self.listaAlu.bind("<Double-1>", self.OnDoubleClick)



Application()
