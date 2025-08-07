import speech_recognition as sr
import threading
import time

comandos_validos = ["up", "down", "left", "right", "arriba", "abajo", "izquierda", "derecha"]

# Variables globales para hilo y control
detener_hilo = False
comando_actual = None
idioma = "es-ES"  # Por defecto español
hilo = None

def _reconocimiento():
    global comando_actual, detener_hilo, idioma
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

    while not detener_hilo:
        try:
            with mic as source:
                print(f"[VOZ] Escuchando en idioma {idioma}...")
                audio = recognizer.listen(source, timeout=5)
            texto = recognizer.recognize_google(audio, language=idioma).lower()
            print(f"[VOZ] Comando detectado: {texto}")

            # Normalizar comandos ingles/español a up/down/left/right
            if texto in ["arriba", "up"]:
                comando_actual = "up"
            elif texto in ["abajo", "down"]:
                comando_actual = "down"
            elif texto in ["izquierda", "left"]:
                comando_actual = "left"
            elif texto in ["derecha", "right"]:
                comando_actual = "right"
            else:
                comando_actual = None
        except sr.UnknownValueError:
            comando_actual = None
        except sr.WaitTimeoutError:
            comando_actual = None
        except Exception as e:
            print(f"[VOZ] Error: {e}")
            comando_actual = None
        time.sleep(0.05)

def iniciar():
    global hilo, detener_hilo
    detener_hilo = False
    hilo = threading.Thread(target=_reconocimiento)
    hilo.daemon = True
    hilo.start()

def detener():
    global detener_hilo, hilo
    detener_hilo = True
    if hilo is not None:
        hilo.join()

def get_comando():
    global comando_actual
    comando = comando_actual
    comando_actual = None
    return comando

def set_idioma(nuevo_idioma):
    global idioma, detener_hilo, hilo
    # Mapear nombre legible a código idioma
    if nuevo_idioma.lower() in ["español", "espanol"]:
        idioma = "es-ES"
    elif nuevo_idioma.lower() == "ingles":
        idioma = "en-US"
    else:
        idioma = "es-ES"  # fallback

    # Reiniciar hilo para aplicar nuevo idioma
    detener()
    iniciar()
    print(f"[VOZ] Idioma cambiado a {nuevo_idioma} ({idioma})")
