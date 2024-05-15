import tkinter as tk 
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")

        # Mudando a cor de fundo de toda a janela
        self.root.configure(bg="#333333")

        # Mudando a cor de fundo do frame
        self.frame = tk.Frame(self.root, bg="#333333")
        self.frame.pack(padx=20, pady=20)

        # Utilizando a fonte CCMarianChurchland e mudando a cor de fundo das labels
        self.label_tarefa = tk.Label(self.frame, text="Tarefa:", bg="#333333", fg="white", font=("CCMarianChurchland", 20))
        self.label_tarefa.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Adicionando um pouco de espaçamento entre a entrada e a label
        self.entry_tarefa = tk.Entry(self.frame, width=35)
        self.entry_tarefa.grid(row=0, column=1, padx=5, pady=5)

        self.label_prioridade = tk.Label(self.frame, text="Prioridade:", bg="#333333", fg="white", font=("CCMarianChurchland", 20))
        self.label_prioridade.grid(row=1, column=0, sticky="w", padx=5, pady=5)

        # Utilizando a fonte CCMarianChurchland para a combobox
        self.combo_prioridade = ttk.Combobox(self.frame, values=["Baixa", "Média", "Alta"], width=27, font=("CCMarianChurchland", 10))
        self.combo_prioridade.current(0)
        self.combo_prioridade.grid(row=1, column=1, padx=5, pady=5)

        # Utilizando a fonte CCMarianChurchland e mudando a cor do botão Adicionar
        self.btn_adicionar = tk.Button(self.frame,width=20, height=1, text="Adicionar", command=self.adicionar_tarefa, bg="#4CAF50", fg="white", font=("CCMarianChurchland", 12, "bold"))
        self.btn_adicionar.grid(row=2, column=0, pady=10, padx=10, sticky="e")

        # Utilizando a fonte CCMarianChurchland e mudando a cor do botão Excluir
        self.btn_excluir = tk.Button(self.frame, width=20, height=1, text="Excluir", command=self.excluir_tarefa, bg="#FF5733", fg="white", font=("CCMarianChurchland", 12, "bold"))
        self.btn_excluir.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Ajustando a altura da Treeview
        self.tree = ttk.Treeview(self.root, columns=("ID", "Tarefa", "Prioridade"), show="headings", height=10)
        self.tree.heading("ID", text="ID")
        self.tree.heading("Tarefa", text="Tarefa")
        self.tree.heading("Prioridade", text="Prioridade")
        self.tree.column("ID", width=50)  # Definindo a largura da coluna ID
        self.tree.column("Tarefa", width=250)  # Definindo a largura da coluna Tarefa
        self.tree.column("Prioridade", width=100)  # Definindo a largura da coluna Prioridade
        self.tree.pack(padx=20, pady=20)

        # Mudando a cor e a fonte do botão Listar Tarefas
        self.btn_listar = tk.Button(self.root, text="Listar Tarefas", command=self.listar_tarefas, bg="#007BFF", fg="white", font=("Arial", 12, "bold"))
        self.btn_listar.pack(pady=10)

        # Conectar ao banco de dados SQLite
        self.conexao = sqlite3.connect("tarefas.db")
        self.criar_tabela_tarefas()

    def criar_tabela_tarefas(self):
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY, tarefa TEXT, prioridade TEXT)")
        self.conexao.commit()

    def adicionar_tarefa(self):
        tarefa = self.entry_tarefa.get()
        prioridade = self.combo_prioridade.get()

        if tarefa:
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO tarefas (tarefa, prioridade) VALUES (?, ?)", (tarefa, prioridade))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            self.entry_tarefa.delete(0, tk.END)
            self.combo_prioridade.current(0)
        else:
            messagebox.showerror("Erro", "Por favor, insira uma tarefa.")

    def listar_tarefas(self):
        self.tree.delete(*self.tree.get_children())
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, tarefa, prioridade FROM tarefas")
        tarefas = cursor.fetchall()

        for tarefa in tarefas:
            self.tree.insert("", tk.END, values=(tarefa[0], tarefa[1], tarefa[2]))

    def excluir_tarefa(self):
        selecionados = self.tree.selection()

        if not selecionados:
            messagebox.showerror("Erro", "Selecione uma tarefa para excluir.")
            return

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir a tarefa selecionada?"):
            for item in selecionados:
                id_tarefa = self.tree.item(item, "values")[0]  
                cursor = self.conexao.cursor()
                cursor.execute("DELETE FROM tarefas WHERE id=?", (id_tarefa,))
                self.conexao.commit()
                self.tree.delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()
