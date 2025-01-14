import cv2
import numpy as np

# Lista para armazenar os pontos selecionados
points_to_track = []
trajectories = [[]]  # Histórico de posições para o ponto móvel principal

# Variável para iniciar o vídeo após marcar os pontos
start_video = False

# Função para registrar os cliques do mouse
def select_point(event, x, y, flags, param):
    global start_video
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points_to_track) < 2:  # Permitir apenas dois pontos
            points_to_track.append((x, y))  # Adicionar o ponto selecionado
            if len(trajectories) < 2:  # Garantir que haja espaço para o histórico do ponto móvel
                trajectories.append([])
            trajectories[len(points_to_track) - 1].append((x, y))
            print(f"Ponto {len(points_to_track)} selecionado: {x}, {y}")

# Função para estabilizar o vídeo
def stabilize_frame(prev_gray, curr_gray, prev_frame):
    features_prev = cv2.goodFeaturesToTrack(prev_gray, maxCorners=100, qualityLevel=0.01, minDistance=30)
    features_curr, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, features_prev, None)
    valid_points_prev = features_prev[status == 1]
    valid_points_curr = features_curr[status == 1]
    matrix, _ = cv2.estimateAffinePartial2D(valid_points_prev, valid_points_curr)
    stabilized_frame = cv2.warpAffine(prev_frame, matrix, (prev_frame.shape[1], prev_frame.shape[0]))
    return stabilized_frame, matrix

# Função para calcular a distância percorrida
def calculate_distances(trajectory, point2):
    distance_percorrido = 0
    for i in range(1, len(trajectory)):
        x1, y1 = trajectory[i - 1]
        x2, y2 = trajectory[i]
        distance_percorrido += np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    x1, y1 = trajectory[-1]
    x2, y2 = point2
    distance_entre_pontos = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    return distance_entre_pontos, distance_percorrido

# Abrir o vídeo
cap = cv2.VideoCapture('cut_vid.mp4')

# Configurar a janela e registrar o evento do mouse
cv2.namedWindow('Video', cv2.WINDOW_NORMAL)  # Tornar a janela redimensionável
cv2.setMouseCallback('Video', select_point)

# Capturar o primeiro frame do vídeo
ret, frame = cap.read()
if not ret:
    print("Erro ao carregar o vídeo.")
    cap.release()
    exit()

# Obter a taxa de quadros e dimensões do vídeo
fps = cap.get(cv2.CAP_PROP_FPS)
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_delay = int(1000 / fps)  # Tempo de exibição por frame em milissegundos

# Ajustar o tamanho da janela para a resolução do vídeo
cv2.resizeWindow('Video', frame_width, frame_height)

# Mostrar o primeiro frame e esperar a seleção de pontos
while True:
    # Exibir o frame inicial
    display_frame = frame.copy()
    for point in points_to_track:
        cv2.circle(display_frame, point, 8, (0, 0, 255), -1)

    cv2.putText(display_frame, "Marque 2 pontos e pressione ESPACO para iniciar", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Video', display_frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord(' '):  # Pressionar espaço para iniciar o vídeo
        if len(points_to_track) == 2:  # Verificar se os dois pontos foram marcados
            break
        else:
            print("Por favor, marque dois pontos antes de iniciar o vídeo.")

# Configuração do método Lucas-Kanade
lk_params = dict(winSize=(15, 15), maxLevel=2, criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
points_to_track_np = np.array(points_to_track, dtype=np.float32).reshape(-1, 1, 2)
prev_frame = frame
prev_gray = gray_frame

frame_count = 0  # Contador de frames

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 2 != 0:  # Processar apenas frames alternados
        continue

    gray_new = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    stabilized_frame, transform_matrix = stabilize_frame(prev_gray, gray_new, prev_frame)

    # Aplicar Lucas-Kanade aos pontos móveis
    if points_to_track_np is not None and len(points_to_track_np) > 0:
        new_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray_new, points_to_track_np, None, **lk_params)

        for i, (new, old) in enumerate(zip(new_points, points_to_track_np)):
            if status[i] == 1:  # Apenas pontos válidos
                x_new, y_new = new.ravel()
                trajectories[i].append((int(x_new), int(y_new)))  # Atualiza a trajetória

                if i == 0:  # Mostrar a trajetória apenas para o primeiro ponto
                    for j in range(1, len(trajectories[i])):
                        cv2.line(stabilized_frame, trajectories[i][j - 1], trajectories[i][j], (0, 255, 0), 4)

                # Desenhar o ponto atual
                cv2.circle(stabilized_frame, (int(x_new), int(y_new)), 8, (0, 0, 255), -1)

        points_to_track_np = new_points[status == 1].reshape(-1, 1, 2)

    # Traçar linha e calcular distâncias
    if len(points_to_track_np) == 2:
        point1 = points_to_track_np[0].ravel()
        point2 = points_to_track_np[1].ravel()

        # Distâncias
        distance_entre_pontos, distance_percorrido = calculate_distances(trajectories[0], point2)

        # Linha entre os pontos
        cv2.line(stabilized_frame, (int(point1[0]), int(point1[1])), (int(point2[0]), int(point2[1])), (255, 255, 255), 2)

        # Mostrar as distâncias
        cv2.putText(stabilized_frame, f"Distancia entre os pontos: {int(distance_entre_pontos)} px", (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(stabilized_frame, f"Distancia percorrida: {int(distance_percorrido)} px", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Exibir o vídeo estabilizado com os pontos, trajetórias e distâncias
    cv2.imshow('Video', stabilized_frame)

    prev_gray = gray_new
    prev_frame = frame

    # Usar frame_delay para manter a taxa de exibição original
    if cv2.waitKey(frame_delay) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
