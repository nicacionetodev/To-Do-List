import customtkinter as ctk

# Classe Tarefa
class Tarefa:
    def __init__(self, titulo: str, status: str = "A Fazer"):
        self.titulo = titulo
        self.status = status

    def mudar_status(self, novo_status: str):
        if novo_status in ["A Fazer", "Executando", "Feito"]:
            self.status = novo_status

    def __repr__(self):
        return f"{self.titulo} - [{self.status}]"
    
class WidgetTarefa(ctk.CTkFrame):
    def __init__(self, master, tarefa, mover_callback):
        super().__init__(master, fg_color="#f0f0f0", corner_radius=6, height=40)
        self.tarefa = tarefa
        self.mover_callback = mover_callback

        self.label = ctk.CTkLabel(self, text=tarefa.titulo, anchor="w")
        self.label.pack(fill="both", expand=True, padx=10)

        # Bind para drag
        self.bind("<Button-1>", self.start_drag)
        self.bind("<B1-Motion>", self.do_drag)
        self.bind("<ButtonRelease-1>", self.stop_drag)
        self.label.bind("<Button-1>", self.start_drag)
        self.label.bind("<B1-Motion>", self.do_drag)
        self.label.bind("<ButtonRelease-1>", self.stop_drag)

        self._drag_data = {"x": 0, "y": 0}

    def start_drag(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y
        self.lift()

    def do_drag(self, event):
        dx = event.x - self._drag_data["x"]
        dy = event.y - self._drag_data["y"]
        x = self.winfo_x() + dx
        y = self.winfo_y() + dy
        self.place(x=x, y=y)

    def stop_drag(self, event):
        x_root = self.winfo_pointerx()
        y_root = self.winfo_pointery()
        self.mover_callback(self.tarefa, x_root, y_root)

# Classe Tarefa App
class TarefaAPP:
    def __init__(self):
        
        ctk.set_appearance_mode("Light")
        ctk.set_default_color_theme("green")

        self.janela = ctk.CTk()  
        self.janela.title("Lista de Afazeres")
        self.janela.geometry("1000x500")
        
        
        self.tarefas = []

        self.interface()

   
    def interface(self):
        # Janela principal
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(0, weight=1)

        self.frame_principal = ctk.CTkFrame(master=self.janela)
        self.frame_principal.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(4, weight=1)

        # Entrada de tarefa
        self.entrada = ctk.CTkEntry(master=self.frame_principal, placeholder_text="Nova Tarefa")
        self.entrada.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.entrada.bind("<KeyRelease>", self.atualizar_contador)
        self.cor_borda_padrao = self.entrada.cget("border_color")
        self.contador_caracteres = ctk.CTkLabel(master=self.frame_principal, text="0/80", text_color="gray")
        self.contador_caracteres.grid(row=0, column=1, sticky="e", padx=10)

        # Botão adicionar
        self.botao_adicionar = ctk.CTkButton(master=self.frame_principal, text="Adicionar", command=self.adicionar_tarefa)
        self.botao_adicionar.grid(row=1, column=0, columnspan=2, pady=5)

        self.label_erro = ctk.CTkLabel(master=self.frame_principal, text="", text_color="red")
        self.label_erro.grid(row=2, column=0, columnspan=2)

        # Frame colunas: é um container para as 3 colunas de status
        self.frame_colunas = ctk.CTkFrame(master=self.frame_principal)
        self.frame_colunas.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(10,0))
        self.frame_colunas.grid_columnconfigure(0, weight=1)
        self.frame_colunas.grid_columnconfigure(1, weight=1)
        self.frame_colunas.grid_columnconfigure(2, weight=1)
        self.frame_colunas.grid_rowconfigure(0, weight=1)

        # Colunas de tarefas
        self.frame_a_fazer = ctk.CTkScrollableFrame(master=self.frame_colunas, label_text="A Fazer", fg_color="#b6d0f4")
        self.frame_a_fazer.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_executando = ctk.CTkScrollableFrame(master=self.frame_colunas, label_text="Executando", fg_color="#9bbff0")
        self.frame_executando.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.frame_feito = ctk.CTkScrollableFrame(master=self.frame_colunas, label_text="Feito", fg_color="#80adf0")
        self.frame_feito.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        # Configurações visuais adicionais (tema)
        self.tema = {
            "fundo": "#e6f0fa",
            "texto": "#1a2e53",
            "borda": "#6990d0",
            "botao": "#5378cc",
            "hover": "#3c5db1",
            "alerta": "#d94f4f"
        }
        self.janela.configure(fg_color=self.tema["fundo"])
        self.frame_principal.configure(fg_color=self.tema["fundo"])
        self.frame_colunas.configure(fg_color=self.tema["fundo"])
        self.frame_a_fazer.configure(fg_color="#b6d0f4")
        self.frame_executando.configure(fg_color="#9bbff0")
        self.frame_feito.configure(fg_color="#80adf0")

        self.entrada.configure(border_color=self.tema["borda"], text_color=self.tema["texto"])
        self.botao_adicionar.configure(fg_color=self.tema["botao"], hover_color=self.tema["hover"], text_color="white")
        self.contador_caracteres.configure(text_color=self.tema["texto"])
        self.label_erro.configure(text_color=self.tema["alerta"])
        
    def adicionar_tarefa(self):
        titulo = self.entrada.get()
       
        tamanho= len(titulo)

        if tamanho>80:
            excesso=tamanho-80
            self.label_erro.configure(text=f"Você ultrapssou o limite em {excesso} caracteres.")
            self.entrada.configure(border_color="red")
            return

        if titulo.strip()=="":
            self.label_erro.configure(text="A tarefa não pode estar vazia.")
            self.entrada.configure(border_color="red")
            return

        if titulo:
            if self.contar_tarefas_por_status("A Fazer") >= 10:
                self.label_erro.configure(text='Limite de 10 tarefas "A Fazer" antingido.')
                return
            nova_tarefa= Tarefa(titulo)
            self.tarefas.append(nova_tarefa)
              
            self.entrada.delete(0, ctk.END)
            self.label_erro.configure(text="")
            self.atualizar_lista() 
            self.atualizar_contador()

    def atualizar_lista(self):
        for frame in [self.frame_a_fazer,self.frame_executando,self.frame_feito]:
            for widget in frame.winfo_children():
                widget.destroy()
        
        for tarefa in self.tarefas:
            if tarefa.status == "A Fazer":
                frame=self.frame_a_fazer
            elif tarefa.status == "Executando":
                frame=self.frame_executando
            else:
                frame= self.frame_feito
            linha = ctk.CTkFrame(master=frame)
            linha.pack(fill="x", padx=5, pady=2)
            
            label_coluna= ctk.CTkLabel(master=linha, text=tarefa.titulo,anchor="w")
            label_coluna.pack(side="left",fill="x",expand=True)

            botao_opcoes = ctk.CTkButton(master=linha,text="⋮", width=28,height=28,fg_color="transparent", text_color="black")


            botao_opcoes.configure(command=lambda b=botao_opcoes, t=tarefa: self.abrir_menu_tarefa(b, t))
            botao_opcoes.pack(side="right", padx=5)
        
          
    def abrir_menu_tarefa(self,botao,tarefa):
        x = botao.winfo_rootx()
        y = botao.winfo_rooty() + botao.winfo_height()

        menu=ctk.CTkToplevel(self.janela)
        menu.configure(fg_color=self.tema["fundo"])
        menu.geometry(f'180x180+{x}+{y}')
        menu.wm_overrideredirect(True)

        ctk.CTkLabel(menu,text="Alterar Status").pack(pady=(5,0))

        opcoes = ctk.CTkOptionMenu(master=menu,values=["A Fazer","Executando","Feito"],command=lambda novo_status: (self.mudar_status_tarefa(tarefa, novo_status), menu.destroy()))

        opcoes.set(tarefa.status)
        opcoes.pack(pady=5)

         # Botão de renomear
        ctk.CTkButton( master=menu, text="✏️ Renomear", command=lambda: (menu.destroy(), self.iniciar_renomear_tarefa(tarefa)) ).pack(pady=2)

        #Botão de excluir
        ctk.CTkButton(master=menu,text="Excluir 🗑️",fg_color="red",hover_color="cc0000",command=lambda:(self.excluir_tarefa(tarefa),menu.destroy())).pack(pady=(5,10))
        menu.configure(fg_color=self.tema["secundario"])

        ctk.CTkButton(
        master=menu,
        text="Excluir 🗑️",
        fg_color=self.tema["alerta"],
        hover_color="#a30006",
        text_color=self.tema["texto"]
)
    def iniciar_renomear_tarefa(self,tarefa):
        self.atualizar_lista()

        for frame in [self.frame_a_fazer, self.frame_executando, self.frame_feito]:
            for linha in frame.winfo_children():
                for widget in linha.winfo_children():
                    if isinstance(widget,ctk.CTkLabel) and widget.cget("text") == tarefa.titulo:
                        widget.destroy()
                        entrada= ctk.CTkEntry(master=linha)
                        entrada.insert(0,tarefa.titulo)
                        entrada.pack(side="left",fill="x",expand=True)
                        entrada.focus()

                        def confirmar(event=None):
                            novo = entrada.get().strip()
                            if novo:
                                tarefa.titulo=novo
                            self.atualizar_lista()
                        entrada.bind("<Return>",confirmar)
                        entrada.bind("<FocusOut>",confirmar)
                        return

    def excluir_tarefa(self, tarefa):
        self.tarefas.remove(tarefa)
        self.atualizar_lista()

    def contar_tarefas_por_status(self,status):
        return sum(1 for tarefas in self.tarefas if tarefas.status == status)

    def mudar_status_tarefa(self, tarefa, novo_status):
        if self.contar_tarefas_por_status(novo_status) >= 10:
             self.label_erro.configure(text=f"Limite de 10 tarefas '{novo_status}' atingido.")
             return

        tarefa.mudar_status(novo_status)
        self.label_erro.configure(text="")  # limpa erro anterior
        self.atualizar_lista()
    
    def atualizar_contador(self, event=None):
        texto = self.entrada.get()
        tamanho=len(texto)
        self.contador_caracteres.configure(text=f"{tamanho}/80")

        if tamanho>80:
            self.entrada.configure(border_color="red")
        else:
            self.entrada.configure(border_color=self.cor_borda_padrao)

    def iniciar(self):
        self.janela.mainloop()

# Função principal
def main():
    app = TarefaAPP()  
    
    app.iniciar()  

if __name__ == "__main__":
    main()
