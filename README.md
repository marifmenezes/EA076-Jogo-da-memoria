# EE076-Laboratorio-de-Embarcados

## Descrição

O projeto consiste em utilizar a matriz de LEDs RGB 5x5 para criar um Jogo da Memória. O nível inicial do jogo utiliza apenas um led de posição aleatória para que o jogador memorize e tenha oportunidade de se familiarizar com o mecanismo do jogo em um nível simples. A luz será mostrada por um intervalo de tempo e depois será desligada. Em seguida será disponibilizado um led na posição central, o jogador deverá utilizar o joystick para posicionar o led no local memorizado e confirmar com um dos botões onde deseja “fixar” a luz. 

## Detalhamento do jogo
Nosso jogo consiste em um desafio de memória utilizando uma matriz 5x5 do Bitdoglab para exibir imagens que devem ser memorizadas.Nele utilizaremos:
- Matriz de LED
- Joystick
- Botão B
- Display


 O funcionamento do jogo é o seguinte:
No primeiro nível, um único LED acenderá em uma posição aleatória na matriz.
O LED permanecerá aceso por 2 segundos e depois apagará.
Após o LED apagar, um LED central na matriz 5x5, de cor branca, será aceso para indicar que o jogador pode iniciar a jogada.
O jogador deve utilizar o joystick para mover o LED aceso, procurando a posição do LED que havia acendido anteriormente.
A mensagem "Pressione B!" aparecerá na tela, indicando que o jogador deve pressionar o botão B para confirmar a posição que acredita ser a correta.
Após a confirmação, o LED escolhido permanecerá aceso até que o jogador selecione todos os LEDs que apareceram.
Se a posição estiver correta, os LEDs confirmados acenderão na cor verde e o jogador avançará para o próximo nível, onde mais um LED será adicionado, aumentando o desafio até que 15 LEDs sejam memorizados na última fase.
Se o jogador errar, os LEDs corretos acenderão na cor vermelha, e o jogador será retornado ao nível 1.
Ao completar todos os 15 níveis, os LEDs acenderão em um padrão que simula fogos de artifício.
Os níveis avançam de 1 a 15, com a quantidade de LEDs a serem memorizados correspondendo ao número do nível (por exemplo, nível 1 = 1 LED; nível 2 = 2 LEDs).


## Código

Em seguida, definimos as funções que vão compor o código principal do projeto. 
- Read joystick: Lê os valores dos eixos X e Y do joystick e os converte em uma escala de 0 a 10.
- Move cursor: Move o cursor dentro dos limites da matriz 5x5.
- Display position(pos, color): Exibe a posição do cursor na matriz de LEDs com uma cor específica.
- Intensidade: define o quão forte será a intensidade do led na matriz 5x5
- Led aceso: função para acender os leds na posição informada
- Display sequence: limpa a matriz, acende cada led na posição a ser memorizado por 2s e apaga os leds
- Draw text: permite a escrita no display, será utilizada para mostrar “Pressione B!”
- Check player input: ordena as sublistas e listas que guardam as posições selecionadas pelo jogador e as com a sequência correta para comparação 
- Play level
  - Gera uma sequência aleatória de posições de LEDs para o nível atual.
  - Exibe a sequência de LEDs para o jogador memorizar.
  - O jogador usa o joystick para mover o cursor e seleciona posições, que são comparadas com a sequência correta.
  - Se o jogador acertar, os LEDs ficam verdes; se errar, ficam vermelhos.
- Fireworks: Exibe um efeito visual de "fogos de artifício" na matriz de LEDs quando o jogador completa todos os níveis.

A função principal Main inicia o jogo no nível 1 e avança até o nível 15, ou reinicia no nível 1 se o jogador errar.

