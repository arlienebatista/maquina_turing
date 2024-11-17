import tkinter as tk
from tkinter import ttk, messagebox

class TuringMachine:
    def __init__(self):
        self.fita = ['B'] * 100  # Fita com 100 células inicializadas com branco (B)
        self.cabeca = 50  # Posição inicial da cabeça de leitura
        self.estado_atual = 'q0'  # Estado inicial
        self.programa = {}  # Dicionário para armazenar as transições

    def adicionar_transicao(self, estado_atual, simbolo_atual, novo_estado, novo_simbolo, movimento):
        self.programa[(estado_atual, simbolo_atual)] = (novo_estado, novo_simbolo, movimento)

    def executar_passo(self):
        if self.estado_atual == 'qf':  # Estado final
            return False
        
        simbolo_atual = self.fita[self.cabeca]
        if (self.estado_atual, simbolo_atual) not in self.programa:
            return False
        
        novo_estado, novo_simbolo, movimento = self.programa[(self.estado_atual, simbolo_atual)]
        self.fita[self.cabeca] = novo_simbolo
        self.estado_atual = novo_estado
        
        if movimento == 'D':
            self.cabeca += 1
        elif movimento == 'E':
            self.cabeca -= 1
            
        return True

class Interface:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Máquina de Turing")
        self.maquina = TuringMachine()
        
        # Configuração da interface
        self.criar_widgets()
        
    def criar_widgets(self):
        # Frame para entrada de transições
        frame_transicoes = ttk.LabelFrame(self.root, text="Adicionar Transição")
        frame_transicoes.pack(padx=10, pady=5, fill="x")
        
        # Campos de entrada
        ttk.Label(frame_transicoes, text="Estado Atual:").grid(row=0, column=0, padx=5, pady=5)
        self.estado_atual = ttk.Entry(frame_transicoes, width=10)
        self.estado_atual.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frame_transicoes, text="Símbolo Atual:").grid(row=0, column=2, padx=5, pady=5)
        self.simbolo_atual = ttk.Entry(frame_transicoes, width=10)
        self.simbolo_atual.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(frame_transicoes, text="Novo Estado:").grid(row=1, column=0, padx=5, pady=5)
        self.novo_estado = ttk.Entry(frame_transicoes, width=10)
        self.novo_estado.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(frame_transicoes, text="Novo Símbolo:").grid(row=1, column=2, padx=5, pady=5)
        self.novo_simbolo = ttk.Entry(frame_transicoes, width=10)
        self.novo_simbolo.grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(frame_transicoes, text="Movimento (E/D):").grid(row=1, column=4, padx=5, pady=5)
        self.movimento = ttk.Entry(frame_transicoes, width=10)
        self.movimento.grid(row=1, column=5, padx=5, pady=5)
        
        # Botão para adicionar transição
        ttk.Button(frame_transicoes, text="Adicionar Transição", 
                  command=self.adicionar_transicao).grid(row=2, column=0, columnspan=6, pady=10)
        
        # Frame para visualização da fita
        frame_fita = ttk.LabelFrame(self.root, text="Fita")
        frame_fita.pack(padx=10, pady=5, fill="x")
        
        self.canvas_fita = tk.Canvas(frame_fita, height=100)
        self.canvas_fita.pack(fill="x", padx=5, pady=5)
        
        # Frame para controles
        frame_controles = ttk.Frame(self.root)
        frame_controles.pack(padx=10, pady=5, fill="x")
        
        ttk.Button(frame_controles, text="Executar Passo", 
                  command=self.executar_passo).pack(side="left", padx=5)
        ttk.Button(frame_controles, text="Reset", 
                  command=self.reset).pack(side="left", padx=5)
        
    def adicionar_transicao(self):
        try:
            self.maquina.adicionar_transicao(
                self.estado_atual.get(),
                self.simbolo_atual.get(),
                self.novo_estado.get(),
                self.novo_simbolo.get(),
                self.movimento.get().upper()
            )
            messagebox.showinfo("Sucesso", "Transição adicionada com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            
    def desenhar_fita(self):
        self.canvas_fita.delete("all")
        x = 50
        y = 50
        tamanho_celula = 30
        
        # Desenha células visíveis da fita
        for i in range(max(0, self.maquina.cabeca - 5), min(len(self.maquina.fita), self.maquina.cabeca + 6)):
            # Desenha retângulo
            self.canvas_fita.create_rectangle(x, y - tamanho_celula/2, 
                                           x + tamanho_celula, y + tamanho_celula/2)
            # Desenha símbolo
            self.canvas_fita.create_text(x + tamanho_celula/2, y, 
                                       text=self.maquina.fita[i])
            
            # Destaca a posição atual da cabeça
            if i == self.maquina.cabeca:
                self.canvas_fita.create_polygon(x + tamanho_celula/2, y - tamanho_celula/2 - 10,
                                              x + tamanho_celula/2 - 10, y - tamanho_celula/2 - 20,
                                              x + tamanho_celula/2 + 10, y - tamanho_celula/2 - 20,
                                              fill="red")
            
            x += tamanho_celula
            
        # Mostra estado atual
        self.canvas_fita.create_text(50, 20, 
                                   text=f"Estado Atual: {self.maquina.estado_atual}",
                                   anchor="w")
            
    def executar_passo(self):
        if self.maquina.executar_passo():
            self.desenhar_fita()
        else:
            messagebox.showinfo("Fim", "Máquina parou!")
            
    def reset(self):
        self.maquina = TuringMachine()
        self.desenhar_fita()

if __name__ == "__main__":
    root = tk.Tk()
    app = Interface(root)
    root.mainloop()
