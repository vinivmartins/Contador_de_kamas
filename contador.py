import tkinter as tk
from tkinter import ttk

total_kamas_acumuladas = 0
meta_diaria_inicial = 200.0  # Meta diária fixa inicial em R$
meta_restante = meta_diaria_inicial

class Cliente:
    def __init__(self, nome, lutas, frame, row):
        self.nome = nome
        self.lutas = lutas
        self.lutas_anteriores = 0
        self.frame = frame
        self.row = row

        self.label_nome = ttk.Entry(frame)
        self.label_nome.insert(0, nome)
        self.label_nome.grid(row=row, column=0, padx=5)

        self.label_lutas = tk.Entry(frame, width=5)
        self.label_lutas.insert(0, str(lutas))
        self.label_lutas.grid(row=row, column=1, padx=5)

        self.atualizar_cor()

    def diminuir_luta(self):
        if self.lutas > 0:
            self.lutas -= 1
            self.label_lutas.delete(0, tk.END)
            self.label_lutas.insert(0, str(self.lutas))
            self.atualizar_cor()

    def atualizar_cor(self):
        if self.lutas == 0:
            self.label_lutas.config(bg="red")
        else:
            self.label_lutas.config(bg="white")

    def atualizar_dados(self):
        try:
            self.nome = self.label_nome.get()
            nova_luta = int(self.label_lutas.get())
            self.lutas_anteriores = self.lutas
            self.lutas = nova_luta
            self.atualizar_cor()
        except ValueError:
            pass

def criar_interface(clientes, pause_event):
    global total_kamas_acumuladas, meta_restante

    def iniciar():
        for cliente in clientes:
            cliente.atualizar_dados()
        calcular_kamas_e_lucro(somar=True, modo='inicial')
        pause_event.clear()

    def atualizar():
        for cliente in clientes:
            cliente.atualizar_dados()
        calcular_kamas_e_lucro(somar=True, modo='delta')

    def definir_total_kamas():
        global total_kamas_acumuladas
        try:
            total_kamas_acumuladas = int(entry_kamas_totais.get())
            calcular_kamas_e_lucro(somar=False)
        except ValueError:
            pass

    def calcular_kamas_e_lucro(somar=True, modo='delta'):
        global total_kamas_acumuladas, meta_restante
        total_kamas = 0

        for cliente in clientes:
            if modo == 'delta':
                diferenca = cliente.lutas - cliente.lutas_anteriores
            else:
                diferenca = cliente.lutas

            if diferenca >= 5:
                total_kamas += diferenca * 360_000
            elif diferenca >= 3:
                total_kamas += diferenca * 366_000
            elif diferenca >= 1:
                total_kamas += diferenca * 400_000

        if somar:
            total_kamas_acumuladas += total_kamas

        lucro = total_kamas_acumuladas / 1_000_000 * 5.8
        meta_restante = max(0, meta_diaria_inicial - lucro)

        label_kamas.config(text=f"Kamas Totais: {total_kamas_acumuladas:,} 🪙")
        label_lucro.config(text=f"Lucro Diário: R${lucro:.2f}")
        label_meta.config(text=f"Meta Restante: R${meta_restante:.2f}")

    root = tk.Tk()
    root.title("Contador de Lutas - Dofus")

    ttk.Label(root, text="Nome").grid(row=0, column=0)
    ttk.Label(root, text="Lutas").grid(row=0, column=1)

    frame = ttk.Frame(root)
    frame.grid(row=1, column=0, columnspan=3)

    for i in range(5):
        clientes.append(Cliente(f"Cliente {i+1}", 0, frame, i))

    ttk.Button(root, text="Iniciar", command=iniciar).grid(row=2, column=0, pady=10)
    ttk.Button(root, text="Atualizar Dados", command=atualizar).grid(row=2, column=1, pady=10)

    entry_kamas_totais = ttk.Entry(root)
    entry_kamas_totais.grid(row=3, column=0, padx=5, pady=5)
    ttk.Button(root, text="Definir Kamas Totais", command=definir_total_kamas).grid(row=3, column=1, padx=5)

    label_kamas = ttk.Label(root, text="Kamas Totais: 0 🪙", font=("Segoe UI", 10, "bold"))
    label_kamas.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    label_lucro = ttk.Label(root, text="Lucro Diário: R$0.00", font=("Segoe UI", 10, "bold"))
    label_lucro.grid(row=5, column=0, columnspan=2)

    label_meta = ttk.Label(root, text=f"Meta Restante: R${meta_restante:.2f}", font=("Segoe UI", 10, "bold"), foreground="blue")
    label_meta.grid(row=6, column=0, columnspan=2, pady=(10, 0))

    return root
