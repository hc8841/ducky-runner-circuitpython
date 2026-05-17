import time
import board
import digitalio
import usb_hid
import os
import sys
from adafruit_hid.keyboard import Keyboard
import adafruit_ducky
import adafruit_logging as logging

# --- Configuração do LED ---
try:
    led = digitalio.DigitalInOut(board.LED)
    led.direction = digitalio.Direction.OUTPUT
    led_available = True
except ValueError:
    led_available = False
    print("LED não encontrado na placa. Prosseguindo sem ele.")

def piscar_led(vezes=1, intervalo=0.1):
    """Faz o LED piscar um número específico de vezes."""
    if led_available:
        for _ in range(vezes):
            led.value = True
            time.sleep(intervalo)
            led.value = False
            time.sleep(intervalo)

def piscar_led_continuo(ativo):
    """Liga/desliga o LED em modo contínuo."""
    if led_available:
        led.value = ativo
        if ativo:
            time.sleep(0.05)

# --- Configuração do Logger ---
logger = logging.getLogger("ducky_runner")
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler("execution_log.txt")
log_handler.setLevel(logging.INFO)
logger.addHandler(log_handler)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

# --- Carregar Configuração e Inicializar Layout ---
def carregar_configuracao():
    """
    Lê o arquivo config.txt na raiz.
    Formato esperado: 
        Linha 1: Nome do módulo do layout
        Linha 2: Delay inicial (opcional)
    """
    layout_modulo = "adafruit_hid.keyboard_layout_us"  # Padrão: US
    nome_layout_classe = "KeyboardLayoutUS"            # Padrão: US
    delay_inicial = 1000                               # Padrão: 1000 ms

    try:
        with open("/config.txt", "r") as f:
            linhas = f.read().strip().splitlines()
            if len(linhas) >= 1 and linhas[0].strip():
                nome_modulo = linhas[0].strip()
                # Mapeia nomes de arquivo para importações dinâmicas
                # Mapeia o nome do arquivo de layout para a importação correta
                mod_layout_map = {
                    "keyboard_layout_us":     ("adafruit_hid.keyboard_layout_us", "KeyboardLayoutUS"),
                    "keyboard_layout_win_br": ("keyboard_layout_win_br", "KeyboardLayout"),
                    "keyboard_layout_win_pt": ("keyboard_layout_win_pt", "KeyboardLayout"),
                    "keyboard_layout_win_fr": ("keyboard_layout_win_fr", "KeyboardLayout"),
                    "keyboard_layout_win_de": ("keyboard_layout_win_de", "KeyboardLayout"),
                    "keyboard_layout_win_es": ("keyboard_layout_win_es", "KeyboardLayout"),
                    "keyboard_layout_win_it": ("keyboard_layout_win_it", "KeyboardLayout"),
                }
                if nome_modulo in mod_layout_map:
                    layout_modulo, nome_layout_classe = mod_layout_map[nome_modulo]
                else:
                    logger.warning(f"Layout '{nome_modulo}' não reconhecido. Usando padrão US.")
                    layout_modulo, nome_layout_classe = "adafruit_hid.keyboard_layout_us", "KeyboardLayoutUS"
            if len(linhas) >= 2 and linhas[1].strip().isdigit():
                delay_inicial = int(linhas[1].strip())
    except OSError:
        logger.info("Arquivo config.txt não encontrado. Usando configurações padrão (US layout).")
    except Exception as e:
        logger.error(f"Erro ao ler config.txt: {e}. Usando padrão.")
    return layout_modulo, nome_layout_classe, delay_inicial

def inicializar_layout(layout_modulo, nome_layout_classe, keyboard):
    """Importa dinamicamente e inicializa o layout do teclado."""
    try:
        # Importa o módulo especificado
        modulo_layout = __import__(layout_modulo, fromlist=[nome_layout_classe])
        classe_layout = getattr(modulo_layout, nome_layout_classe)
        keyboard_layout = classe_layout(keyboard)
        logger.info(f"Layout inicializado com sucesso: {layout_modulo}.{nome_layout_classe}")
        return keyboard_layout
    except Exception as e:
        logger.error(f"Falha ao importar layout '{layout_modulo}.{nome_layout_classe}': {e}")
        raise

time.sleep(1)  # Pequena pausa para evitar race condition

layout_modulo, nome_layout_classe, delay_inicial = carregar_configuracao()
keyboard = Keyboard(usb_hid.devices)
keyboard_layout = inicializar_layout(layout_modulo, nome_layout_classe, keyboard)

logger.info(f"Delay inicial configurado: {delay_inicial} ms")

# Inicializa Ducky com o layout carregado
try:
    duck = adafruit_ducky.Ducky("payload.txt", keyboard, keyboard_layout)
    logger.info("Arquivo payload.txt carregado com sucesso.")
except Exception as e:
    logger.error(f"Falha ao carregar payload.txt: {e}")
    while True:
        piscar_led(3, 0.2)
        time.sleep(2)

# --- Execução do Script ---
logger.info("Iniciando execução do DuckScript...")
piscar_led(2, 0.2)

# Aguarda o delay inicial configurado
time.sleep(delay_inicial / 1000.0)

linha_atual = 1
result = True
linhas_executadas = 0

while result is not False:
    try:
        piscar_led_continuo(True)
        result = duck.loop()
        piscar_led_continuo(False)
    except Exception as e:
        logger.error(f"Erro na linha {linha_atual}: {e}")
        piscar_led(5, 0.1)
        break

    if result is False:
        logger.info("Fim do script alcançado.")
        break

    linha_atual += 1
    linhas_executadas += 1
    time.sleep(0.05)

# --- Log Final ---
logger.info("=== RESUMO DA EXECUÇÃO ===")
logger.info(f"Total de linhas executadas: {linhas_executadas}")
logger.info("Execução finalizada.")
piscar_led(3, 0.3)