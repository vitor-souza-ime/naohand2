import qi
import cv2
import numpy as np
import mediapipe as mp
import time

# Configuração da sessão com o NAO
NAO_IP = "172.15.4.178"   # altere para o IP do seu NAO
NAO_PORT = 9559

session = qi.Session()
try:
    session.connect(f"tcp://{NAO_IP}:{NAO_PORT}")
    print("Conectado ao NAO!")
except RuntimeError:
    print("Erro: não foi possível conectar ao NAO.")
    exit(1)

# Serviços do NAO
video_service = session.service("ALVideoDevice")
tts_service = session.service("ALTextToSpeech")  # Serviço de fala

# Inscrição na câmera do NAO (640x480, RGB)
subscriber_id = video_service.subscribeCamera(
    "camera_test", 0, 1, 11, 30
)

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.3
)

def detect_gesture(landmarks):
    # Coordenadas dos dedos
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]
    index_mcp = landmarks[5]
    middle_mcp = landmarks[9]
    ring_mcp = landmarks[13]
    pinky_mcp = landmarks[17]

    finger_tips = [index_tip, middle_tip, ring_tip, pinky_tip]
    finger_mcps = [index_mcp, middle_mcp, ring_mcp, pinky_mcp]
    fingers_up = 0

    for tip, mcp in zip(finger_tips, finger_mcps):
        if tip.y < mcp.y - 0.05:
            fingers_up += 1

    if fingers_up == 5:
        y_positions = [tip.y for tip in finger_tips]
        if max(y_positions) - min(y_positions) < 0.2:
            return "Open Hand"

    if fingers_up > 0:
        return f"{fingers_up} Finger"

    return "No Gesture"

frame_count = 0

print("Pressione 'q' para sair.")

# Obter serviço de movimento
motion_service = session.service("ALMotion")

# Deixar o corpo todo mole
motion_service.setStiffnesses("Body", 0.0)

while True:
    nao_image = video_service.getImageRemote(subscriber_id)
    if nao_image is None:
        continue

    frame_count += 1

    width, height = nao_image[0], nao_image[1]
    array = nao_image[6]

    try:
        frame = np.frombuffer(array, dtype=np.uint8).reshape((height, width, 3))
    except:
        continue

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    i=time.time()
    results = hands.process(frame_rgb)
    f=time.time()-i

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks.landmark)

            # NAO fala o gesto detectado
            # tts_service.say(gesture)
            print(gesture+" t="+str(f)+"s")

            cv2.putText(frame, gesture, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No hands detected", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.imshow("Finger Counting", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finalizar
video_service.unsubscribe(subscriber_id)
cv2.destroyAllWindows()
hands.close()
print("Finalizado!")
