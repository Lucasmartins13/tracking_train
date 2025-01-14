Este projeto utiliza a biblioteca OpenCV para realizar o rastreamento de pontos em um vídeo, calcular distâncias entre pontos e trajetórias, e estabilizar os frames do vídeo. O usuário seleciona dois pontos de interesse, e o programa processa o vídeo para fornecer informações visuais e numéricas sobre o movimento dos pontos selecionados.

**Funcionalidades**

Seleção de Pontos: Permite ao usuário selecionar dois pontos no primeiro frame do vídeo.

Estabilização de Vídeo: Reduz oscilações de câmera utilizando fluxos ópticos e transformações afins.

Rastreamento de Pontos: Monitora o movimento dos pontos selecionados utilizando o método Lucas-Kanade.

Trajetórias: Desenha as trajetórias dos pontos ao longo do vídeo.

Cálculo de Distâncias: Calcula a distância percorrida por um ponto e a distância atual entre os dois pontos.
