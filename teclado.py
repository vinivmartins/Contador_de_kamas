from pynput import keyboard

def iniciar_escuta_shift(clientes, atualizar_interface):
    print("Escutando Shift...")

    def on_press(key):
        if key == keyboard.Key.shift:
            print("Shift pressionado! Diminuindo lutas...")
            for cliente in clientes:
                cliente.diminuir_luta()
            atualizar_interface()

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    # Não usar `listener.join()` para não travar a execução principal
