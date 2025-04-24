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