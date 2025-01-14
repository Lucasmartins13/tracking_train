Este projeto utiliza a biblioteca OpenCV para realizar o rastreamento de pontos em um vídeo, calcular distâncias entre pontos e trajetórias, e estabilizar os frames do vídeo. O usuário seleciona dois pontos de interesse, e o programa processa o vídeo para fornecer informações visuais e numéricas sobre o movimento dos pontos selecionados.

## **Funcionalidades**

Seleção de Pontos: Permite ao usuário selecionar dois pontos no primeiro frame do vídeo.

Estabilização de Vídeo: Reduz oscilações de câmera utilizando fluxos ópticos e transformações afins.

Rastreamento de Pontos: Monitora o movimento dos pontos selecionados utilizando o método Lucas-Kanade.

Trajetórias: Desenha as trajetórias dos pontos ao longo do vídeo.

Cálculo de Distâncias: Calcula a distância percorrida por um ponto e a distância atual entre os dois pontos.

## **Tecnologias Utilizadas**

. Python

. OpenCV

. NumPy

## **como usar**

Certifique-se de ter o Python 3.x instalado.

Instale as dependências necessárias executando:

pip install opencv-python numpy

Adicione o vídeo que deseja processar (renomeie para cut_vid.mp4 ou altere o nome no código, se necessário).

Execute o programa:

python rastreamento.py

Na janela do vídeo:

Clique para selecionar dois pontos de interesse.

Pressione a barra de espaço para iniciar o processamento.

Pressione Q para sair a qualquer momento.

## **Saída do programa**

O vídeo será exibido com os seguintes elementos:

Trajetórias dos pontos selecionados (apenas para o primeiro ponto).

Linha conectando os dois pontos selecionados.

Informativos com:

Distância entre os dois pontos (em pixels).

Distância percorrida pelo primeiro ponto (em pixels).

## **Estrutura do código**

Seleção de Pontos: A função select_point registra os cliques do usuário no primeiro frame.

Estabilização de Frames: A função stabilize_frame utiliza fluxo óptico para corrigir movimentos da câmera.

Rastreamento de Pontos: Utiliza o método Lucas-Kanade para calcular a nova posição dos pontos em cada frame.

Cálculo de Distâncias: A função calculate_distances calcula a distância percorrida e a distância entre pontos.

## **Controles**

Espaço: Inicia o processamento após a seleção dos pontos.

Q: Fecha o programa.

## **Requisitos do sistema**

Python 3.6 ou superior

Biblioteca OpenCV (4.x ou superior)

NumPy
