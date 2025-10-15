import pytest
from types import SimpleNamespace
from src.gestos.components.gesture_mapper import GestureMapper

@pytest.fixture
def gesture_mapper():
    """Pytest fixture to provide a GestureMapper instance."""
    return GestureMapper()

def create_mock_landmarks(finger_states):
    """Crea un objeto de landmarks simulado basado en los estados de los dedos."""
    landmarks = []
    for i in range(21):
        # Simula la posición Y. Si el dedo está 'up', la punta está más alta.
        y_pos = 0.1 if finger_states.get(i, 'down') == 'up' else 0.9
        # Simula la posición X para el pulgar
        x_pos = 0.1 if finger_states.get(i, 'right') == 'left' else 0.9
        landmarks.append(SimpleNamespace(x=x_pos, y=y_pos, z=0))
    
    # Simula la distancia para el clic
    if finger_states.get('click', False):
        landmarks[4].x, landmarks[4].y = 0.5, 0.5
        landmarks[8].x, landmarks[8].y = 0.51, 0.51 # Muy cerca

    return SimpleNamespace(landmark=landmarks)

def test_detect_open_hand(gesture_mapper):
    """Prueba que se detecta correctamente el gesto de mano abierta."""
    # Todos los dedos hacia arriba, excepto el pulgar que se mide en X
    states = {4: 'left', 8: 'up', 12: 'up', 16: 'up', 20: 'up'}
    mock_hand = create_mock_landmarks(states)
    gesture = gesture_mapper.detect_gesture(mock_hand)
    assert gesture == "OPEN_HAND"

def test_detect_fist(gesture_mapper):
    """Prueba que se detecta correctamente el gesto de puño cerrado."""
    # Todos los dedos hacia abajo
    states = {4: 'right', 8: 'down', 12: 'down', 16: 'down', 20: 'down'}
    mock_hand = create_mock_landmarks(states)
    gesture = gesture_mapper.detect_gesture(mock_hand)
    assert gesture == "FIST"

def test_detect_pointing(gesture_mapper):
    """Prueba que se detecta el gesto de apuntar."""
    states = {8: 'up'} # Solo el índice hacia arriba
    mock_hand = create_mock_landmarks(states)
    gesture = gesture_mapper.detect_gesture(mock_hand)
    assert gesture == "POINTING"

def test_detect_click(gesture_mapper):
    """Prueba que se detecta el gesto de clic."""
    states = {'click': True}
    mock_hand = create_mock_landmarks(states)
    gesture = gesture_mapper.detect_gesture(mock_hand)
    assert gesture == "CLICK"
