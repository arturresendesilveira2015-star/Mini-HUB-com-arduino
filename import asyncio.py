import asyncio
import threading
import pygame
from bleak import BleakClient

# =========================
# CONFIGURAÇÃO BLE
# =========================
JDY16_ADDRESS = "3C:A5:51:9A:26:B5"
CHAR_UUID = "0000ffe3-0000-1000-8000-00805f9b34fb"
send_queue = ["","","","",""]  # fila de mensagens para enviar
connected = False

# =========================
# FUNÇÃO BLE
# =========================
async def ble_loop():
    global connected
    try:
        async with BleakClient(JDY16_ADDRESS) as client:
            connected = True
            print("✅ Conectado ao JDY-16")

            # Loop contínuo de envio
            while True:
                if send_queue:
                    msg = send_queue[0] + send_queue[1] + send_queue[2] + send_queue[3] + send_queue[4] + "\n"
                    await client.write_gatt_char(CHAR_UUID, msg.encode())
                    print(msg)
                await asyncio.sleep(0.3)
    except Exception as e:
        print("⚠️ Erro BLE:", e)
    finally:
        connected = False

def run_ble():
    asyncio.run(ble_loop())

# =========================
# INTERFACE PYGAME
# =========================
pygame.init()
screen = pygame.display.set_mode((1000, 200))
pygame.display.set_caption("JDY-16 Bluetooth Terminal")
font = pygame.font.Font(None, 32)
font2 = pygame.font.Font(None, 16)
clock = pygame.time.Clock()

user_input = ""

# Inicia BLE em thread paralela
ble_thread = threading.Thread(target=run_ble, daemon=True)
ble_thread.start()

# =========================
# LOOP PRINCIPAL
# =========================
running = True
while running:
    send_queue[0] = "1D"
    send_queue[1] = "2D"
    send_queue[2] = "3D"
    send_queue[3] = "4D"
    send_queue[4] = "5D"
    screen.fill((255, 255, 255))

    status_text = "Conectado" if connected else "⏳ Conectando..."
    status = font.render(status_text, True, (255, 255, 0) if not connected else (100, 255, 100))
    screen.blit(status, (800, 150))
    pygame.draw.rect(screen, (0, 255, 255), (50, 50, 99, 99))
    texto_conf = font2.render("Botão Esquerdo", True, (0, 0, 0))
    screen.blit(texto_conf, (50, 80))
    pygame.draw.rect(screen, (0, 255, 255), (200, 50, 99, 99))
    texto_conf = font2.render("Botão Direito", True, (0, 0, 0))
    screen.blit(texto_conf, (200, 80))
    pygame.draw.rect(screen, (0, 255, 255), (350, 50, 99, 99))
    texto_conf = font2.render("Botão Cima", True, (0, 0, 0))
    screen.blit(texto_conf, (350, 80))
    pygame.draw.rect(screen, (0, 255, 255), (500, 50, 99, 99))
    texto_conf = font2.render("Botão Baixo", True, (0, 0, 0))
    screen.blit(texto_conf, (500, 80))
    pygame.draw.rect(screen, (0, 255, 255), (650, 50, 99, 99))
    texto_conf = font2.render("Botão Selecionar", True, (0, 0, 0))
    screen.blit(texto_conf, (650, 80))

    posicao = pygame.mouse.get_pos()
    if 50 <= posicao[0] <= 149 and 50 <= posicao[1] <= 149 and pygame.mouse.get_pressed()[0]:
        send_queue[0] = "1L"
        pygame.draw.rect(screen, (0, 125, 125), (50, 50, 100, 100))
    if 200 <= posicao[0] <= 299 and 50 <= posicao[1] <= 149 and pygame.mouse.get_pressed()[0]:
        send_queue[1] = "2L"
        pygame.draw.rect(screen, (0, 125, 125), (200, 50, 100, 100))
    if 350 <= posicao[0] <= 449 and 50 <= posicao[1] <= 149 and pygame.mouse.get_pressed()[0]:
        send_queue[2] = "3L"
        pygame.draw.rect(screen, (0, 125, 125), (350, 50, 100, 100))
    if 500 <= posicao[0] <= 599 and 50 <= posicao[1] <= 149 and pygame.mouse.get_pressed()[0]:
        send_queue[3] = "4L"
        pygame.draw.rect(screen, (0, 125, 125), (500, 50, 100, 100))
    if 650 <= posicao[0] <= 749 and 50 <= posicao[1] <= 149 and pygame.mouse.get_pressed()[0]:
        send_queue[4] = "5L"
        pygame.draw.rect(screen, (0, 125, 125), (650, 50, 100, 100))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x: 
                running = False
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
