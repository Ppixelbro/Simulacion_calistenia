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

# ----------------------------
# Lógica para la animación del stickman 
# ----------------------------
import matplotlib.pyplot as plt
from matplotlib import animation
import tempfile

def animate(frame, ejercicio, progresion, distances, angles, ax):
    ax.clear()
    frac = min(1.0, frame / (frames - 1) * 2)  # Aceleramos la animación
    L_t, L_p, L_b = distances
    
    # Usamos los ángulos originales para cálculos
    angulo_t_original = angles[0]
    angulo_p_original = angles[1]
    angulo_b_original = angles[2]
    
    # Para la animación, definimos ángulos visuales específicos sin modificar los originales
    # Estos ángulos son solo para la visualización y no afectan los cálculos
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
    
    # VISUALIZACIÓN del Front Lever
    if ejercicio == "Front Lever":
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
        # En Front Lever, el ángulo de las piernas es relativo al tronco
        
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
        
        # Dibujar brazos (desde los puntos de agarre hasta los hombros)
        ax.plot([-0.15, hombros_x], [barra_y, hombros_y], 'r-', lw=3)
        ax.plot([0.15, hombros_x], [barra_y, hombros_y], 'r-', lw=3)
        
        # Dibujar tronco (desde los hombros hasta la cadera)
        ax.plot([hombros_x, tronco_x], [hombros_y, tronco_y], 'b-', lw=6)
        
        # Dibujar piernas (desde la cadera)
        ax.plot([tronco_x, piernas_x], [tronco_y, piernas_y], 'g-', lw=4)
        
        # Dibujar cabeza (en los hombros)
        cabeza = plt.Circle((hombros_x, hombros_y), 0.1, fill=True, edgecolor='black', facecolor='lightgray')
        ax.add_patch(cabeza)
        
    else:  # Para L-sit y V-sit (no animados gradualmente)
        # No usamos frac para interpolar posiciones ya que mostramos posición estática
        
        # Punto de apoyo en el suelo
        suelo_y = -0.5
        
        # Vista lateral: solo mostramos un lado del cuerpo
        mano_x = 0.1  # Ligeramente desplazado para vista lateral
        mano_y = suelo_y
        
        # Definimos primero la posición de la cadera/base del tronco
        cadera_x = 0
        cadera_y = suelo_y + 0.3  # Elevada del suelo
        
        # Definimos la posición de los hombros (punto medio del tronco)
        # Los hombros están entre la cadera y la cabeza (mitad superior del tronco)
        hombros_x = cadera_x
        hombros_y = cadera_y + L_t * 0.5  # A mitad de camino hacia la cabeza
        
        # El tronco se extiende desde la cadera hacia arriba
        tronco_x = cadera_x
        tronco_y = cadera_y + L_t  # Longitud total del tronco
        
        # Las piernas se extienden desde la cadera hacia adelante
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
        
        # Ajustar posición del brazo según el tipo de ejercicio
        if progresion == "Full V-sit":
            # Para V-sit, el brazo sale directamente del tronco a mitad de camino
            # Calculamos un punto en el tronco para el origen del brazo
            brazo_origen_x = cadera_x - L_t * 0.2  # Punto en el tronco inclinado
            brazo_origen_y = cadera_y + L_t * 0.4  # A mitad del tronco aproximadamente
            
            # Corregir dirección del brazo para V-sit (hacia atrás, no hacia adelante)
            mano_x_v_sit = -0.3  # Mano más atrás para el V-sit
            
            # Dibujar brazo desde un punto del tronco hacia el suelo (dirección corregida)
            ax.plot([brazo_origen_x, mano_x_v_sit], [brazo_origen_y, mano_y], 'r-', lw=3)
            # Actualizar punto de mano para dibujarlo correctamente
            mano_x = mano_x_v_sit
        else:
            # Para L-sit y Tuck L-sit, corregir dirección (brazo hacia atrás)
            mano_x_corregido = -0.2  # Mano detrás del hombro, no delante
            
            # Dibujar brazo desde los hombros hacia atrás
            ax.plot([hombros_x, mano_x_corregido], [hombros_y, mano_y], 'r-', lw=3)
            # Actualizar punto de mano para dibujarlo correctamente
            mano_x = mano_x_corregido
        
        # Dibujar mano (punto de apoyo)
        ax.scatter(mano_x, mano_y, s=40, color='red')
        
        # Dibujar tronco completo (desde la cadera hasta la cabeza)
        ax.plot([cadera_x, tronco_x], [cadera_y, tronco_y], 'b-', lw=6)
        
        # Dibujar piernas (desde la cadera)
        ax.plot([cadera_x, piernas_x], [cadera_y, piernas_y], 'g-', lw=4)
        
        # Dibujar cabeza (en la parte superior del tronco)
        cabeza = plt.Circle((tronco_x, tronco_y), 0.1, fill=True, edgecolor='black', facecolor='lightgray')
        ax.add_patch(cabeza)

    # Mostrar los ángulos originales usados para cálculos (para verificación)
    ax.text(-0.95, 0.9, f"Ángulos usados para cálculos:", fontsize=7)
    ax.text(-0.95, 0.85, f"Tronco: {np.degrees(angulo_t_original):.0f}°", fontsize=7)
    ax.text(-0.95, 0.8, f"Piernas: {np.degrees(angulo_p_original):.0f}°", fontsize=7)
    ax.text(-0.95, 0.75, f"Brazos: {np.degrees(angulo_b_original):.0f}°", fontsize=7)
    
    # Configuración del gráfico
    ax.set_aspect('equal')
    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)
    ax.axis('off')
    
    # Leyenda
    ax.text(-0.95, -0.95, "Azul: Tronco", color='blue', fontsize=8)
    ax.text(-0.95, -0.9, "Verde: Piernas", color='green', fontsize=8)
    ax.text(-0.95, -0.85, "Rojo: Brazos", color='red', fontsize=8)
    
    # Título de la animación
    ax.set_title(f"{ejercicio}: {progresion}", fontsize=12)
    
    # Añadir explicación del ejercicio
    if ejercicio == "V-sit" and progresion == "L-sit":
        ax.text(-0.95, 0.6, "L-sit: ejercicio donde el cuerpo", fontsize=7)
        ax.text(-0.95, 0.55, "forma una 'L' con el tronco vertical", fontsize=7)
        ax.text(-0.95, 0.5, "y las piernas extendidas horizontalmente", fontsize=7)

# Preparación de la animación
distances = (distancia_tronco, distancia_piernas, distancia_brazos)
angles = (angulo_tronco_rad, angulo_piernas_rad, angulo_brazos_rad)
frames = 60

fig, ax = plt.subplots(figsize=(6, 6))
ani = animation.FuncAnimation(
    fig, animate,
    fargs=(ejercicio, progresion, distances, angles, ax),
    frames=frames,
    interval=50
)

# Guardar GIF en archivo temporal y mostrar
with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as tmp:
    ani.save(tmp.name, writer='pillow', fps=20)
    tmp_path = tmp.name

with open(tmp_path, 'rb') as f:
    gif_bytes = f.read()

st.subheader("Animación del Stickman")
st.image(gif_bytes, use_container_width=True)
