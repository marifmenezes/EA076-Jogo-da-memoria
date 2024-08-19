from machine import Pin, ADC, SoftI2C
import neopixel
import time
from ssd1306 import SSD1306_I2C
import random

# Configurações da matriz de LEDs e do joystick
NUM_LEDS = 25  # Número total de LEDs na matriz 5x5
np = neopixel.NeoPixel(Pin(7), NUM_LEDS)  # Inicializa a matriz de LEDs no GPIO7
i2c = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c)

# Mapeamento da matriz 5x5 com os índices dos LEDs
LED_MATRIX = [
    [24, 23, 22, 21, 20],  # Linha 1
    [15, 16, 17, 18, 19],  # Linha 2
    [14, 13, 12, 11, 10],  # Linha 3
    [5, 6, 7, 8, 9],       # Linha 4
    [4, 3, 2, 1, 0]        # Linha 5
]

# Configuração do Joystick e botões
x_axis = ADC(Pin(27))  # Eixo X do joystick no GPIO27
y_axis = ADC(Pin(26))  # Eixo Y do joystick no GPIO26
button_B = Pin(6, Pin.IN, Pin.PULL_UP)  # Botão A no GPIO5

# Posição central da matriz 5x5
CENTER_POS = [2, 2]  # Centro da matriz
current_pos = [2, 2]  # Posição atual do cursor

# Função para ler o valor do joystick
def read_joystick():
    # Converte os valores do joystick para uma escala de 0 a 10
    x_val = x_axis.read_u16() // 6554  
    y_val = y_axis.read_u16() // 6554  
    return x_val, y_val

# Função para mover o cursor dentro dos limites da matriz
def move_cursor(pos):
    x, y = pos
    # Restringe o movimento dentro dos limites 0-4 da matriz
    if x < 0: x = 0
    if x > 4: x = 4
    if y < 0: y = 0
    if y > 4: y = 4
    return [x, y]
    
# Função para limitar a luminosidade a 10%
def intensidade(color):
	return tuple(int(c * 0.1) for c in color)

# Função para exibir a posição do cursor com uma cor específica
def display_position(pos, color=intensidade((255, 255, 255))):
    np.fill((0, 0, 0))  # Limpa a matriz
    np[LED_MATRIX[pos[0]][pos[1]]] = color  # Acende o LED na posição atual
    np.write()  # Atualiza a matriz
    
def led_aceso(pos, color=intensidade((255, 255, 255))):
    np[LED_MATRIX[pos[0]][pos[1]]] = color  # Acende o LED na posição atual
    np.write()  # Atualiza a matriz


# Função para exibir a sequência de LEDs a serem memorizados
def display_sequence(sequence, color=intensidade((255, 255, 255))):
    np.fill((0, 0, 0))  # Limpa a matriz
    for pos in sequence:
        np[LED_MATRIX[pos[0]][pos[1]]] = color  # Acende cada LED da sequência
    np.write()  # Atualiza a matriz
    time.sleep(2)  # Aguarda 2 segundos para memorização
    np.fill((0, 0, 0))  # Apaga os LEDs
    np.write()

# Função para desenhar texto no OLED
def draw_text(text, y):
    oled.fill(0)
    oled.text(text, 0, y)
    oled.show()

# Função para verificar se a entrada do jogador está correta
def check_player_input(player_sequence, correct_sequence):
	# Ordena cada sublista dentro das listas
	sorted_player_sequence = [sorted(sublist) for sublist in player_sequence]
	sorted_correct_sequence = [sorted(sublist) for sublist in correct_sequence]
    
	# Ordena as listas principais para garantir que as sublistas estejam na mesma ordem
	sorted_player_sequence.sort()
	sorted_correct_sequence.sort()
    
	# Compara as sequências
	return sorted_player_sequence == sorted_correct_sequence



# Função principal para jogar um nível
def play_level(level):
    correct_sequence = []  # Lista para armazenar a sequência correta
    used_positions = set()  # Conjunto para armazenar posições já usadas
    
    while len(correct_sequence) < level:
        pos = (random.randint(0, 4), random.randint(0, 4))  # Gera uma posição aleatória como uma tupla
        if pos not in used_positions:
            correct_sequence.append(pos)  # Adiciona à sequência correta
            used_positions.add(pos)  # Marca a posição como usada
    
    display_sequence(correct_sequence)  # Exibe a sequência ao jogador

    print("Gabarito", correct_sequence)
    
    player_sequence = []  # Lista para armazenar a sequência do jogador
    current_pos = CENTER_POS  # Inicializa o cursor na posição central
    display_position(current_pos)  # Exibe o cursor na posição central

    while len(player_sequence) < len(correct_sequence):
        # Lê o movimento do joystick
        x_val, y_val = read_joystick()
        if x_val > 6:  # Move o cursor para a direita
            current_pos[1] -= 1
        elif x_val < 4:  # Move o cursor para a esquerda
            current_pos[1] += 1
        if y_val > 6:  # Move o cursor para baixo
            current_pos[0] -= 1
        elif y_val < 4:  # Move o cursor para cima
            current_pos[0] += 1
        time.sleep(0.1)
        current_pos = move_cursor(current_pos)  # Ajusta o cursor dentro dos limites
        display_position(current_pos)  # Exibe a nova posição do cursor
        
        
        for pos in player_sequence:
            led_aceso(pos, color=intensidade((255, 255, 255)))

        # Verifica se o botão A foi pressionado para confirmar a posição
        if not button_B.value():
            draw_text("Pressione B!", 15)
            player_sequence.append(current_pos.copy())  # Adiciona a posição à sequência do jogador
            time.sleep(0.5)  # Aguarda para evitar múltiplas entradas
            print("Chute", player_sequence)
            
            for pos in player_sequence:
                display_position(pos, color=intensidade((255, 255, 255)))
            

    
    # Verifica se o jogador acertou ou errou
    if check_player_input(player_sequence, correct_sequence):
        # Se acertou, exibe os LEDs em verde
        display_sequence(correct_sequence, color=intensidade((0, 255, 0)))
        return True
    else:
        # Se errou, exibe os LEDs corretos em vermelho
        display_sequence(correct_sequence, color=intensidade((255, 0, 0)))
        return False

# Função principal do jogo
def main():
    level = 1  # Inicia no nível 1
    while level <= 15:  # O jogo continua até o nível 15
        print("Nível:", level)  # Exibe o nível atual
        if play_level(level):  # Se o jogador passar o nível
            level += 1  # Avança para o próximo nível
        else:
            np.fill((0, 0, 0))
            level = 1  # Reinicia o jogo em caso de erro
        time.sleep(2)  # Pausa antes do próximo nível

    # Se o jogador completar os 15 níveis, exibe fogos de artifício
    fireworks()

# Função para exibir "fogos de artifício" após vencer o jogo
def fireworks():
    for _ in range(5):  # Exibe 5 vezes o efeito de fogos
        for i in range(NUM_LEDS):
            # Gera cores aleatórias para cada LED
            np[i] = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        np.write()  # Atualiza a matriz
        time.sleep(0.5)  # Pausa entre os efeitos
        np.fill((0, 0, 0))  # Limpa a matriz
        np.write()

# Inicializa o jogo
main()
