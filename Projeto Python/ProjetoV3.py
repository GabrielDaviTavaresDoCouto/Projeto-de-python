import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciador de Tarefas")

        self.create_widgets()
        self.create_database()

        # Configurar o redimensionamento responsivo
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        # Método para criar os widgets
        self.widgets = {}  # Dicionário para armazenar os widgets

        self.widgets['frame'] = self.create_frame(self.root, bg="#333333")

        self.widgets['label_tarefa'] = self.create_label(self.widgets['frame'], text="Tarefa:", bg="#333333", fg="white")
        self.widgets['entry_tarefa'] = self.create_entry(self.widgets['frame'], width=48)
        self.widgets['label_prioridade'] = self.create_label(self.widgets['frame'], text="Prioridade:", bg="#333333", fg="white")
        self.widgets['combo_prioridade'] = self.create_combobox(self.widgets['frame'], values=["Baixa", "Média", "Alta"], width=45, state="readonly")
        self.widgets['combo_prioridade'].current(0)
        self.widgets['btn_adicionar'] = self.create_button(self.widgets['frame'], text="Adicionar", command=self.adicionar_e_listar_tarefas, bg="#4CAF50", padx=40, pady=1, fg="white")
        self.widgets['btn_excluir'] = self.create_button(self.widgets['frame'], text="Excluir", command=self.excluir_tarefa, bg="#FF5733", padx=50, pady=1, fg="white")
        self.widgets['tree'] = self.create_treeview(self.widgets['frame'], columns=("ID", "Tarefa", "Prioridade"), show="headings", height=10)
       
        # Posicionamento do frame centralizado na janela
        self.widgets['frame'].grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Configuração do redimensionamento responsivo do frame
        self.widgets['frame'].grid_rowconfigure(4, weight=1)
        self.widgets['frame'].grid_columnconfigure(0, weight=1)

        # Posicionamento dos widgets dentro do frame
        self.widgets['label_tarefa'].grid(row=0, column=0, padx=2, pady=2, sticky="w")
        self.widgets['entry_tarefa'].grid(row=0, column=1, padx=2, pady=2, sticky="w")
        self.widgets['label_prioridade'].grid(row=1, column=0, padx=2, pady=2, sticky="w")
        self.widgets['combo_prioridade'].grid(row=1, column=1, padx=2, pady=2, sticky="w")
        self.widgets['btn_adicionar'].grid(row=2, column=1, columnspan=2, padx=2, pady=2, sticky="w")
        self.widgets['btn_excluir'].grid(row=2,column=1, columnspan=2, padx=150, pady=2, sticky="e")
        self.widgets['tree'].grid(row=4, column=0, columnspan=2, padx=2, pady=2, sticky="nsew")


        # Adicionando os cabeçalhos
        self.widgets['tree'].heading("ID", text="ID")
        self.widgets['tree'].heading("Tarefa", text="Tarefa")
        self.widgets['tree'].heading("Prioridade", text="Prioridade")

    def create_frame(self, parent, **kwargs):
        return tk.Frame(parent, **kwargs)

    def create_label(self, parent, **kwargs):
        return tk.Label(parent, **kwargs)

    def create_entry(self, parent, **kwargs):
        return tk.Entry(parent, **kwargs)

    def create_combobox(self, parent, **kwargs):
        return ttk.Combobox(parent, **kwargs)

    def create_button(self, parent, **kwargs):
        return tk.Button(parent, **kwargs)

    def create_treeview(self, parent, **kwargs):
        return ttk.Treeview(parent, **kwargs)

    def create_database(self):
        # Método para criar o banco de dados
        self.conexao = sqlite3.connect("tarefas.db")
        cursor = self.conexao.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS tarefas (id INTEGER PRIMARY KEY, tarefa TEXT, prioridade TEXT)")
        self.conexao.commit()

    def adicionar_e_listar_tarefas(self):
        tarefa = self.widgets['entry_tarefa'].get()
        prioridade = self.widgets['combo_prioridade'].get()

        if tarefa:
            cursor = self.conexao.cursor()
            cursor.execute("INSERT INTO tarefas (tarefa, prioridade) VALUES (?, ?)", (tarefa, prioridade))
            self.conexao.commit()
            messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")
            self.widgets['entry_tarefa'].delete(0, tk.END)
            self.widgets['combo_prioridade'].current(0)
        
            # Atualizar a lista de tarefas
            self.listar_tarefas()
        else:
            messagebox.showerror("Erro", "Por favor, insira uma tarefa.")

    def listar_tarefas(self):
        self.widgets['tree'].delete(*self.widgets['tree'].get_children())
        cursor = self.conexao.cursor()
        cursor.execute("SELECT id, tarefa, prioridade FROM tarefas")
        tarefas = cursor.fetchall()

        for tarefa in tarefas:
            self.widgets['tree'].insert("", tk.END, values=(tarefa[0], tarefa[1], tarefa[2]))

    def excluir_tarefa(self):
        selecionados = self.widgets['tree'].selection()

        if not selecionados:
            messagebox.showerror("Erro", "Selecione uma tarefa para excluir.")
            return

        if messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir a tarefa selecionada?"):
            for item in selecionados:
                id_tarefa = self.widgets['tree'].item(item, "values")[0]
                cursor = self.conexao.cursor()
                cursor.execute("DELETE FROM tarefas WHERE id=?", (id_tarefa,))
                self.conexao.commit()
                self.widgets['tree'].delete(item)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    # Configurar o redimensionamento da janela principal
    root.geometry("600x360")  # Definindo o tamanho da janela
    root.mainloop()
