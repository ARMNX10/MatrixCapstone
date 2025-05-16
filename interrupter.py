# interrupter.py
# Handles keyboard interrupt for TTS (pyttsx3) using pynput
from pynput import keyboard

interrupt_flag = False


def on_press(key):
    global interrupt_flag
    try:
        if key.char and key.char.lower() == 'i':
            interrupt_flag = True
            return False  # Stop listener after pressing 'i'
    except AttributeError:
        pass


def listen_for_interrupt():
    global interrupt_flag
    interrupt_flag = False
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener


def was_interrupted():
    global interrupt_flag
    return interrupt_flag
