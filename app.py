import streamlit as st
import numpy as np

# Título y descripción
st.title("Simulación de Fuerzas y Torque en Movimientos de Calistenia")
st.write("""
Esta aplicación permite simular las fuerzas y torques en diferentes progresiones de movimientos de calistenia.
Se analiza el cuerpo humano en segmentos para calcular las fuerzas y torques en cada posición.
""")

# Selección de ejercicio
ejercicio = st.selectbox("Seleccione el ejercicio", ["Front Lever", "V-sit"])

# Selección de progresión
if ejercicio == "Front Lever":
    progresion = st.selectbox("Seleccione la progresión",
                              ["Tuck Front Lever", "Advanced Tuck Front Lever", "Full Front Lever"])
else:
    progresion = st.selectbox("Seleccione la progresión", ["Tuck L-sit", "L-sit", "Full V-sit"])

# Datos de entrada para los segmentos corporales
st.subheader("Datos del cuerpo")
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Tronco**")
    incluir_tronco = st.checkbox("Incluir segmento", value=True, key="tronco")
    if incluir_tronco:
        masa_tronco = st.number_input("Masa del tronco (kg)", value=30.0, min_value=1.0)
        distancia_tronco = st.number_input("Distancia al eje (m)", value=0.4, min_value=0.1)
    else:
        masa_tronco = 0.0
        distancia_tronco = 0.0

with col2:
    st.write("**Piernas**")
    incluir_piernas = st.checkbox("Incluir segmento", value=True, key="piernas")
    if incluir_piernas:
        masa_piernas = st.number_input("Masa de las piernas (kg)", value=20.0, min_value=1.0)
        distancia_piernas = st.number_input("Distancia al eje (m)", value=0.6, min_value=0.1)
    else:
        masa_piernas = 0.0
        distancia_piernas = 0.0

with col3:
    st.write("**Brazos**")
    incluir_brazos = st.checkbox("Incluir segmento", value=True, key="brazos")
    if incluir_brazos:
        masa_brazos = st.number_input("Masa de los brazos (kg)", value=10.0, min_value=1.0)
        distancia_brazos = st.number_input("Distancia al eje (m)", value=0.25, min_value=0.1)
    else:
        masa_brazos = 0.0
        distancia_brazos = 0.0

# Parámetros biomecánicos
st.subheader("Parámetros biomecánicos")
brazo_palanca = st.number_input("Brazo de palanca del músculo (m)", value=0.05, min_value=0.01)
g = 9.81  # gravedad

# Definición de ángulos según la progresión con opción de personalización
st.subheader("Configuración de ángulos")
if ejercicio == "Front Lever":
    if progresion == "Tuck Front Lever":
        angulo_tronco = 90  # Horizontal (0 grados)
        angulo_piernas = 45  # Perpendicular (90 grados)
        angulo_brazos = 0  # Horizontal (0 grados)
    elif progresion == "Advanced Tuck Front Lever":
        angulo_tronco = 90  # Horizontal (0 grados)
        angulo_piernas = 0  # 45 grados
        angulo_brazos = 0  # Horizontal (0 grados)
    else:  # Full Front Lever
        angulo_tronco = 90  # Horizontal (0 grados)
        angulo_piernas = 90  # Horizontal (0 grados)
        angulo_brazos = 0  # Horizontal (0 grados)
else:  # V-sit
    if progresion == "Tuck L-sit":
        angulo_tronco = 0  # Vertical (90 grados)
        angulo_piernas = 90  # Horizontal (90 grados)
        angulo_brazos = 0  # Horizontal (0 grados)
    elif progresion == "L-sit":
        angulo_tronco = 0  # Vertical (90 grados)
        angulo_piernas = 90  # Horizontal (0 grados)
        angulo_brazos = 0  # Horizontal (0 grados)
    else:  # Full V-sit
        angulo_tronco = 70  # 45 grados hacia atrás
        angulo_piernas = 45  # 45 grados hacia arriba
        angulo_brazos = 0  # Horizontal (0 grados)

# Mostrar los ángulos predefinidos
col1, col2, col3 = st.columns(3)
with col1:
    st.write(f"Ángulo del tronco: {angulo_tronco}°")
with col2:
    st.write(f"Ángulo de las piernas: {angulo_piernas}°")
with col3:
    st.write(f"Ángulo de los brazos: {angulo_brazos}°")

# Conversión de ángulos a radianes
angulo_tronco_rad = np.radians(angulo_tronco)
angulo_piernas_rad = np.radians(angulo_piernas)
angulo_brazos_rad = np.radians(angulo_brazos)

# Cálculos de fuerzas y torques
# Paso 1: Cálculo del peso de cada segmento
peso_tronco = masa_tronco * g if incluir_tronco else 0
peso_piernas = masa_piernas * g if incluir_piernas else 0
peso_brazos = masa_brazos * g if incluir_brazos else 0
peso_total = peso_tronco + peso_piernas + peso_brazos

# Paso 2: Cálculo del torque de cada segmento
torque_tronco = peso_tronco * distancia_tronco * np.sin(np.radians(angulo_tronco)) if incluir_tronco else 0
torque_piernas = peso_piernas * distancia_piernas * np.sin(np.radians(angulo_piernas)) if incluir_piernas else 0
torque_brazos = peso_brazos * distancia_brazos * np.sin(np.radians(angulo_brazos)) if incluir_brazos else 0
torque_total = torque_tronco + torque_piernas + torque_brazos

# Paso 3: Fuerza muscular requerida
fuerza_muscular = torque_total / brazo_palanca if torque_total != 0 else 0

# Resultados
st.subheader("Resultados")
col1, col2 = st.columns(2)

with col1:
    if incluir_tronco:
        st.write(f"Peso tronco: {peso_tronco:.2f} N")
    if incluir_piernas:
        st.write(f"Peso piernas: {peso_piernas:.2f} N")
    if incluir_brazos:
        st.write(f"Peso brazos: {peso_brazos:.2f} N")
    st.write(f"Peso total: {peso_total:.2f} N")

with col2:
    if incluir_tronco:
        st.write(f"Torque tronco: {torque_tronco:.2f} Nm")
    if incluir_piernas:
        st.write(f"Torque piernas: {torque_piernas:.2f} Nm")
    if incluir_brazos:
        st.write(f"Torque brazos: {torque_brazos:.2f} Nm")
    st.write(f"Torque total: {torque_total:.2f} Nm")

st.write(f"Fuerza muscular requerida: {fuerza_muscular:.2f} N")

# Explicación de los cálculos
st.subheader("Explicación de los cálculos")
st.write("""
El análisis se realiza en tres etapas principales, considerando solo los segmentos corporales que has seleccionado incluir:

1. **Cálculo del peso de cada segmento** (W = m × g)
   - Peso del segmento = masa del segmento × gravedad (9.81 m/s²)
   - Ejemplo: Peso del tronco = masa del tronco × 9.81 N
   - Los segmentos no seleccionados no contribuyen al peso total

2. **Cálculo del torque para cada segmento** (τ = W × d × sin(θ))
   - Torque del segmento = peso del segmento × distancia al eje × sin(ángulo)
   - El ángulo se mide desde la horizontal:
     - 0° = segmento horizontal
     - 90° = segmento vertical apuntando hacia arriba
     - -90° = segmento vertical apuntando hacia abajo
   - El factor sin(ángulo) calcula el componente de fuerza perpendicular a la distancia
   - Ejemplo: Torque del tronco = peso tronco × distancia tronco × sin(ángulo tronco)

3. **Fuerza muscular requerida** (F = τ / r)
   - Torque total = suma de torques de todos los segmentos incluidos
   - Fuerza muscular = torque total / brazo de palanca del músculo
   - Esta representa la fuerza mínima que deben generar los músculos para mantener la posición

Esta simulación te permite entender cómo cambia la distribución de fuerzas y torques en diferentes progresiones de movimientos de calistenia según qué segmentos incluyas y sus ángulos específicos.
""")

# Reemplaza la sección de animación existente con este código mejorado
# ----------------------------
# Lógica para la animación anatómica del stickman
# ----------------------------
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches
import tempfile
import numpy as np


def animate(frame, ejercicio, progresion, distances, angles, ax):
    ax.clear()
    frac = min(1.0, frame / (frames - 1) * 2)  # Aceleramos la animación
    L_t, L_p, L_b = distances

    # Colores anatómicos
    color_piel = '#FFD39B'  # Color para la piel
    color_tronco = '#104E8B'  # Azul para el tronco/torso
    color_piernas = '#8B4513'  # Marrón para las piernas
    color_brazo = '#CD5C5C'  # Rojo para el brazo

    if ejercicio == "Front Lever":
        # ÁNGULOS VISUALES para Front Lever
        if progresion == "Tuck Front Lever":
            # Ángulos visuales para Tuck Front Lever
            angulo_t_visual = np.radians(0)  # Tronco horizontal
            angulo_p_visual = np.radians(135)  # Piernas muy flexionadas (45° con tronco)
            angulo_b_visual = np.radians(90)  # Brazos verticales
        elif progresion == "Advanced Tuck Front Lever":
            # Ángulos visuales para Advanced Tuck Front Lever
            angulo_t_visual = np.radians(0)  # Tronco horizontal
            angulo_p_visual = np.radians(90)  # Piernas flexionadas a 90°
            angulo_b_visual = np.radians(90)  # Brazos verticales
        else:  # Full Front Lever
            # Ángulos visuales para Full Front Lever
            angulo_t_visual = np.radians(0)  # Tronco horizontal
            angulo_p_visual = np.radians(0)  # Piernas extendidas alineadas con tronco
            angulo_b_visual = np.radians(90)  # Brazos verticales

        # Interpolación para animar gradualmente el Front Lever
        θ_t = frac * angulo_t_visual
        θ_p = frac * angulo_p_visual
        θ_b = frac * angulo_b_visual

        # Front Lever: punto de agarre en la barra (arriba)
        # La barra estará en la parte superior
        barra_y = 0.8

        # Los hombros son el punto donde se unen brazos y tronco
        hombros_x = 0
        hombros_y = barra_y - L_b  # Distancia desde la barra

        # El tronco se extiende desde los hombros
        tronco_x = hombros_x + L_t * np.cos(θ_t)
        tronco_y = hombros_y + L_t * np.sin(θ_t)

        # Las piernas se extienden desde el final del tronco en el ángulo correcto
        # Calculamos primero la dirección del tronco
        dir_tronco = np.array([np.cos(θ_t), np.sin(θ_t)])

        # Rotamos esta dirección según el ángulo de las piernas relativo al tronco
        cos_p = np.cos(θ_p)
        sin_p = np.sin(θ_p)
        rot_matrix = np.array([[cos_p, -sin_p], [sin_p, cos_p]])
        dir_piernas = np.dot(rot_matrix, dir_tronco)

        # Calculamos el punto final de las piernas
        piernas_x = tronco_x + L_p * dir_piernas[0]
        piernas_y = tronco_y + L_p * dir_piernas[1]

        # Dibujar la barra
        ax.plot([-0.5, 0.5], [barra_y, barra_y], 'k-', lw=6)

        # Dibujar puntos de agarre
        ax.scatter([-0.15, 0.15], [barra_y, barra_y], s=40, color='red')

        # ---- VERSIÓN ANATÓMICA ----

        # Brazo anatómico (solo un brazo visible como una sola sección continua)
        # Para el Front Lever usamos una sola elipse alargada para el brazo
        # Centro del brazo anatómico
        centro_brazo_x = (0.15 + hombros_x) / 2
        centro_brazo_y = (barra_y + hombros_y) / 2

        # Longitud y dirección del brazo
        dx_brazo = hombros_x - 0.15
        dy_brazo = hombros_y - barra_y
        largo_brazo = np.sqrt(dx_brazo ** 2 + dy_brazo ** 2)
        angulo_brazo = np.arctan2(dy_brazo, dx_brazo)

        # Dibujamos el brazo como una única elipse continua
        ancho_brazo = 0.06
        brazo_elipse = patches.Ellipse((centro_brazo_x, centro_brazo_y),
                                       largo_brazo, ancho_brazo,
                                       angle=np.degrees(angulo_brazo),
                                       facecolor=color_brazo, edgecolor='black', linewidth=1)
        ax.add_patch(brazo_elipse)

        # Torso anatómico (desde los hombros hasta la cadera)
        # Calculamos la dirección del tronco
        dx_tronco = tronco_x - hombros_x
        dy_tronco = tronco_y - hombros_y
        angulo_tronco = np.arctan2(dy_tronco, dx_tronco)

        # Dibujamos el tronco como una elipse alargada
        ancho_tronco = 0.12
        largo_tronco = L_t

        # Centro de la elipse (a mitad de camino entre hombros y cadera)
        centro_tronco_x = hombros_x + dx_tronco / 2
        centro_tronco_y = hombros_y + dy_tronco / 2

        # Dibujamos el tronco como una elipse
        tronco_elipse = patches.Ellipse((centro_tronco_x, centro_tronco_y),
                                        largo_tronco, ancho_tronco,
                                        angle=np.degrees(angulo_tronco),
                                        facecolor=color_tronco, edgecolor='black', linewidth=1)
        ax.add_patch(tronco_elipse)

        # Piernas anatómicas (desde la cadera)
        dx_piernas = piernas_x - tronco_x
        dy_piernas = piernas_y - tronco_y
        angulo_piernas = np.arctan2(dy_piernas, dx_piernas)

        # En caso de Tuck Front Lever o Advanced, dibujamos piernas flexionadas
        if progresion == "Tuck Front Lever" or progresion == "Advanced Tuck Front Lever":
            # Punto de la rodilla (punto medio)
            rodilla_x = tronco_x + dx_piernas * 0.4
            rodilla_y = tronco_y + dy_piernas * 0.4

            # Muslos (parte superior de las piernas)
            ancho_muslo = 0.08
            dx_muslo = rodilla_x - tronco_x
            dy_muslo = rodilla_y - tronco_y
            centro_muslo_x = tronco_x + dx_muslo / 2
            centro_muslo_y = tronco_y + dy_muslo / 2
            muslo_elipse = patches.Ellipse((centro_muslo_x, centro_muslo_y),
                                           np.sqrt(dx_muslo ** 2 + dy_muslo ** 2), ancho_muslo,
                                           angle=np.degrees(np.arctan2(dy_muslo, dx_muslo)),
                                           facecolor=color_piernas, edgecolor='black', linewidth=1)
            ax.add_patch(muslo_elipse)

            # Parte inferior de las piernas (gemelos)
            ancho_gemelo = 0.06
            dx_gemelo = piernas_x - rodilla_x
            dy_gemelo = piernas_y - rodilla_y
            centro_gemelo_x = rodilla_x + dx_gemelo / 2
            centro_gemelo_y = rodilla_y + dy_gemelo / 2
            gemelo_elipse = patches.Ellipse((centro_gemelo_x, centro_gemelo_y),
                                            np.sqrt(dx_gemelo ** 2 + dy_gemelo ** 2), ancho_gemelo,
                                            angle=np.degrees(np.arctan2(dy_gemelo, dx_gemelo)),
                                            facecolor=color_piernas, edgecolor='black', linewidth=1)
            ax.add_patch(gemelo_elipse)

            # Rodilla (articulación)
            rodilla = patches.Circle((rodilla_x, rodilla_y), 0.035,
                                     facecolor=color_piel, edgecolor='black', linewidth=1)
            ax.add_patch(rodilla)
        else:
            # Piernas extendidas para Full Front Lever
            ancho_pierna = 0.09
            largo_pierna = L_p
            centro_pierna_x = tronco_x + dx_piernas / 2
            centro_pierna_y = tronco_y + dy_piernas / 2
            pierna_elipse = patches.Ellipse((centro_pierna_x, centro_pierna_y),
                                            largo_pierna, ancho_pierna,
                                            angle=np.degrees(angulo_piernas),
                                            facecolor=color_piernas, edgecolor='black', linewidth=1)
            ax.add_patch(pierna_elipse)

        # Para Front Lever, simplificamos: la cabeza está en posición horizontal
        # Calculamos la posición correcta para la cabeza (a la izquierda de los hombros)
        cabeza_x = hombros_x - 0.15  # Desplazamiento a la izquierda
        cabeza_y = hombros_y  # Misma altura que los hombros

        # Dibujar el cuello como una simple línea horizontal desde los hombros hasta la cabeza
        ancho_cuello = 0.05  # Ancho del cuello
        largo_cuello = 0.08  # Longitud del cuello

        # El cuello está perfectamente horizontal
        cuello = patches.Ellipse(((hombros_x + cabeza_x) / 2, hombros_y),
                                 largo_cuello, ancho_cuello,
                                 angle=0,  # Ángulo horizontal fijo (0 grados)
                                 facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(cuello)

        # Cabeza anatómica (elipse) - ahora a la izquierda de los hombros, perfectamente horizontal
        cabeza = patches.Ellipse((cabeza_x, cabeza_y), 0.15, 0.18,
                                 facecolor=color_piel, edgecolor='black', linewidth=1,
                                 angle=0)  # Ángulo horizontal fijo (0 grados)
        ax.add_patch(cabeza)

        # Hombros (articulaciones)
        hombro = patches.Circle((hombros_x, hombros_y), 0.04,
                                facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(hombro)

        # Manos (extremo del brazo)
        mano = patches.Circle((0.15, barra_y), 0.03,
                              facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(mano)

        # Pies (extremo de la pierna)
        pie = patches.Ellipse((piernas_x, piernas_y), 0.12, 0.05,
                              angle=np.degrees(angulo_piernas),
                              facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(pie)

    else:  # Para L-sit y V-sit
        # Punto de apoyo en el suelo
        suelo_y = -0.5

        # Vista lateral: solo mostramos un lado del cuerpo
        mano_y = suelo_y

        # Definimos primero la posición de la cadera/base del tronco
        cadera_x = 0
        cadera_y = suelo_y + 0.3  # Elevada del suelo

        # Definimos la posición de los hombros (punto medio del tronco)
        hombros_x = cadera_x
        hombros_y = cadera_y + L_t * 0.5  # A mitad de camino hacia la cabeza

        # El tronco se extiende desde la cadera hacia arriba
        tronco_x = cadera_x
        tronco_y = cadera_y + L_t  # Longitud total del tronco

        # Las piernas se extienden desde la cadera
        piernas_x = cadera_x + L_p
        piernas_y = cadera_y  # Horizontales desde la cadera

        # Para la variante Tuck, ajustamos piernas si es necesario
        if progresion == "Tuck L-sit":
            # En Tuck las piernas están ligeramente elevadas
            piernas_x = cadera_x + L_p * 0.7
            piernas_y = cadera_y + L_p * 0.3
        elif progresion == "Full V-sit":
            # En V-sit, ajustamos ángulos de tronco y piernas
            tronco_x = cadera_x - L_t * 0.4
            tronco_y = cadera_y + L_t * 0.8
            piernas_x = cadera_x + L_p * 0.6
            piernas_y = cadera_y + L_p * 0.4

        # Dibujar suelo
        ax.plot([-0.8, 0.8], [suelo_y, suelo_y], 'k-', lw=2)

        # Dibujamos el tronco anatómico primero
        dx_tronco = tronco_x - cadera_x
        dy_tronco = tronco_y - cadera_y
        largo_tronco = np.sqrt(dx_tronco ** 2 + dy_tronco ** 2)
        angulo_tronco = np.arctan2(dy_tronco, dx_tronco)

        # Centro del tronco anatómico
        centro_tronco_x = (cadera_x + tronco_x) / 2
        centro_tronco_y = (cadera_y + tronco_y) / 2

        # Dibujamos el tronco como una elipse
        ancho_tronco = 0.12
        tronco_elipse = patches.Ellipse((centro_tronco_x, centro_tronco_y),
                                        largo_tronco, ancho_tronco,
                                        angle=np.degrees(angulo_tronco),
                                        facecolor=color_tronco, edgecolor='black', linewidth=1)
        ax.add_patch(tronco_elipse)

        # CORRECCIÓN: Para V-sit, calculamos un punto más centrado en el torso
        if progresion == "Full V-sit":
            # Calculamos la posición del hombro a lo largo del torso (centro del torso)
            # Factor 0.5 significa que está a mitad de camino entre cadera y fin del torso
            hombro_factor = 0.5

            # Posición del hombro en el centro del torso
            hombros_x = cadera_x + dx_tronco * hombro_factor
            hombros_y = cadera_y + dy_tronco * hombro_factor
        else:
            # Para L-sit y Tuck L-sit, mantenemos el cálculo original
            hombros_x = cadera_x
            hombros_y = cadera_y + L_t * 0.5

        # Definimos la posición de la mano (punto de apoyo) para que esté directamente debajo del hombro
        # Esto garantiza que el brazo sea completamente vertical
        mano_x = hombros_x

        # El punto de origen del brazo es el hombro
        brazo_origen_x = hombros_x
        brazo_origen_y = hombros_y

        # Centro del brazo anatómico (punto medio entre origen y mano)
        centro_brazo_x = hombros_x  # Mismo X para que sea vertical
        centro_brazo_y = (brazo_origen_y + mano_y) / 2

        # Longitud y dirección del brazo
        dx_brazo = 0  # No hay desplazamiento horizontal (brazo vertical)
        dy_brazo = mano_y - brazo_origen_y  # Desplazamiento vertical
        largo_brazo = abs(dy_brazo)  # Longitud absoluta
        angulo_brazo = -np.pi / 2  # -90 grados (apuntando hacia abajo)

        # Piernas anatómicas
        dx_piernas = piernas_x - cadera_x
        dy_piernas = piernas_y - cadera_y
        largo_piernas = np.sqrt(dx_piernas ** 2 + dy_piernas ** 2)
        angulo_piernas = np.arctan2(dy_piernas, dx_piernas)

        # En Tuck L-sit, dibujamos piernas flexionadas
        if progresion == "Tuck L-sit":
            # Punto de la rodilla (punto medio)
            rodilla_x = cadera_x + dx_piernas * 0.4
            rodilla_y = cadera_y + dy_piernas * 0.4

            # Muslos (parte superior de las piernas)
            ancho_muslo = 0.08
            dx_muslo = rodilla_x - cadera_x
            dy_muslo = rodilla_y - cadera_y
            centro_muslo_x = cadera_x + dx_muslo / 2
            centro_muslo_y = cadera_y + dy_muslo / 2
            largo_muslo = np.sqrt(dx_muslo ** 2 + dy_muslo ** 2)
            muslo_elipse = patches.Ellipse((centro_muslo_x, centro_muslo_y),
                                           largo_muslo, ancho_muslo,
                                           angle=np.degrees(np.arctan2(dy_muslo, dx_muslo)),
                                           facecolor=color_piernas, edgecolor='black', linewidth=1)
            ax.add_patch(muslo_elipse)

            # Parte inferior de las piernas (gemelos)
            ancho_gemelo = 0.06
            dx_gemelo = piernas_x - rodilla_x
            dy_gemelo = piernas_y - rodilla_y
            centro_gemelo_x = rodilla_x + dx_gemelo / 2
            centro_gemelo_y = rodilla_y + dy_gemelo / 2
            largo_gemelo = np.sqrt(dx_gemelo ** 2 + dy_gemelo ** 2)
            gemelo_elipse = patches.Ellipse((centro_gemelo_x, centro_gemelo_y),
                                            largo_gemelo, ancho_gemelo,
                                            angle=np.degrees(np.arctan2(dy_gemelo, dx_gemelo)),
                                            facecolor=color_piernas, edgecolor='black', linewidth=1)
            ax.add_patch(gemelo_elipse)

            # Rodilla (articulación)
            rodilla = patches.Circle((rodilla_x, rodilla_y), 0.035,
                                     facecolor=color_piel, edgecolor='black', linewidth=1)
            ax.add_patch(rodilla)
        else:
            # Piernas extendidas para L-sit y V-sit
            ancho_pierna = 0.09
            centro_pierna_x = cadera_x + dx_piernas / 2
            centro_pierna_y = cadera_y + dy_piernas / 2
            pierna_elipse = patches.Ellipse((centro_pierna_x, centro_pierna_y),
                                            largo_piernas, ancho_pierna,
                                            angle=np.degrees(angulo_piernas),
                                            facecolor=color_piernas, edgecolor='black', linewidth=1)
            ax.add_patch(pierna_elipse)

        # Cuello anatómico - añadiendo separación entre hombros y cabeza
        # Calcular la dirección del cuello basado en la dirección del torso
        dx_tronco = tronco_x - cadera_x
        dy_tronco = tronco_y - cadera_y
        direccion_tronco = np.array([dx_tronco, dy_tronco])
        direccion_tronco = direccion_tronco / np.linalg.norm(direccion_tronco)  # normalizar vector

        longitud_cuello = 0.08

        # Posición del cuello (siguiendo la dirección del tronco)
        cuello_x = tronco_x + direccion_tronco[0] * longitud_cuello
        cuello_y = tronco_y + direccion_tronco[1] * longitud_cuello

        # Dibujar el cuello
        ancho_cuello = 0.05

        # Encontrar ángulo para el cuello
        angulo_cuello = np.arctan2(direccion_tronco[1], direccion_tronco[0])

        # Dibujar cuello como elipse pequeña
        cuello = patches.Ellipse((tronco_x + direccion_tronco[0] * longitud_cuello / 2,
                                  tronco_y + direccion_tronco[1] * longitud_cuello / 2),
                                 longitud_cuello, ancho_cuello,
                                 angle=np.degrees(angulo_cuello),
                                 facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(cuello)

        # Cabeza anatómica (elipse) - ahora en el extremo del cuello
        cabeza = patches.Ellipse((cuello_x, cuello_y), 0.15, 0.18,
                                 facecolor=color_piel, edgecolor='black', linewidth=1,
                                 angle=np.degrees(angulo_cuello))  # Misma orientación que el tronco
        ax.add_patch(cabeza)

        # IMPORTANTE: Ahora dibujamos el brazo DESPUÉS del torso para que aparezca encima
        # Dibujamos el brazo como una elipse
        ancho_brazo = 0.06
        brazo_elipse = patches.Ellipse((centro_brazo_x, centro_brazo_y),
                                       largo_brazo, ancho_brazo,
                                       angle=np.degrees(angulo_brazo),
                                       facecolor=color_brazo, edgecolor='black', linewidth=1)
        ax.add_patch(brazo_elipse)

        # Hombros (articulación)
        hombro = patches.Circle((hombros_x, hombros_y), 0.04,
                                facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(hombro)

        # Cadera (articulación)
        cadera = patches.Circle((cadera_x, cadera_y), 0.04,
                                facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(cadera)

        # Dibujar mano (punto de apoyo)
        mano = patches.Circle((mano_x, mano_y), 0.03,
                              facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(mano)

        # Pies (extremo de la pierna)
        pie_angulo = angulo_piernas
        pie = patches.Ellipse((piernas_x, piernas_y), 0.12, 0.05,
                              angle=np.degrees(pie_angulo),
                              facecolor=color_piel, edgecolor='black', linewidth=1)
        ax.add_patch(pie)

    # ELIMINADOS: Todo el código de textos para ángulos y leyendas

    # Configuración del gráfico - AMPLIAMOS LOS LÍMITES
    ax.set_aspect('equal')
    ax.set_xlim(-1.5, 1.5)  # Límites más amplios en X
    ax.set_ylim(-1.5, 1.5)  # Límites más amplios en Y
    ax.axis('off')

    # ELIMINADO: Título de la animación
    # ELIMINADO: Texto de explicación del ejercicio


# Preparación de la animación
distances = (distancia_tronco, distancia_piernas, distancia_brazos)
angles = (angulo_tronco_rad, angulo_piernas_rad, angulo_brazos_rad)
frames = 60

fig, ax = plt.subplots(figsize=(8, 8))  # Mayor tamaño para mejor visualización
plt.subplots_adjust(left=0, right=1, bottom=0, top=1)  # Eliminar márgenes

# Eliminar título del gráfico y cualquier otro texto
plt.tick_params(axis='both', which='both', bottom=False, top=False,
                labelbottom=False, right=False, left=False, labelleft=False)
plt.box(False)

ani = animation.FuncAnimation(
    fig, animate,
    fargs=(ejercicio, progresion, distances, angles, ax),
    frames=frames,
    interval=50
)

# Guardar GIF en archivo temporal y mostrar
with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
    ani.save(tmp.name, writer='pillow', fps=20, dpi=100)  # Mayor DPI
    tmp_path = tmp.name

with open(tmp_path, 'rb') as f:
    gif_bytes = f.read()

st.subheader("Animación Anatómica")
st.image(gif_bytes, use_container_width=True)