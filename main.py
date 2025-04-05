import threading
from contador import criar_interface
from teclado import iniciar_escuta_shift

clientes = []
pause_event = threading.Event()
pause_event.set()  # Começa pausado

def atualizar_interface():
    for cliente in clientes:
        cliente.atualizar_dados()

if __name__ == "__main__":
    print("Criando interface...")
    root = criar_interface(clientes, pause_event)

    # Listener de teclado em segundo plano
    thread = threading.Thread(target=iniciar_escuta_shift, args=(clientes, atualizar_interface), daemon=True)
    thread.start()

    print("Iniciando mainloop...")
    root.mainloop()
