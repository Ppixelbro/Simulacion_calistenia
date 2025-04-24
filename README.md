# Calculadora de Fuerzas y Torque en Movimientos de Calistenia

## Descripción

Esta aplicación calcula las fuerzas y torques involucrados en diferentes progresiones de movimientos de calistenia (Front Lever y V-sit). La herramienta divide el cuerpo humano en segmentos para calcular con precisión las interacciones biomecánicas en cada fase del movimiento.

## Características Principales

- Análisis de dos movimientos de calistenia con tres progresiones cada uno:
  - **Front Lever**: Tuck Front Lever, Advanced Tuck Front Lever, Full Front Lever
  - **V-sit**: Tuck L-sit, L-sit, Full V-sit
- Cálculo segmentado por partes del cuerpo (tronco, piernas y brazos)
- Opción para incluir/excluir segmentos específicos en los cálculos
- Cálculo de pesos, torques y fuerza muscular requerida
- Explicación detallada de los principios físicos aplicados

## Requisitos

- Python 3.x (recomendado 3.9 o superior)
- Streamlit (para la interfaz de usuario)
- NumPy (para cálculos matemáticos)

## Instalación

1. Clona o descarga este repositorio en tu máquina local.

2. Instala las dependencias necesarias:

```bash
pip install -r requirements.txt
```

## Uso

1. Inicia la aplicación con Streamlit:

```bash
streamlit run app.py
```

2. En la interfaz de la aplicación:
   - Selecciona el ejercicio de calistenia (Front Lever o V-sit)
   - Elige la progresión que deseas analizar
   - Activa o desactiva los segmentos corporales a incluir en el cálculo
   - Introduce los parámetros de masa y distancia para cada segmento
   - Ajusta el brazo de palanca del músculo

3. La aplicación calculará automáticamente:
   - El peso de cada segmento corporal
   - El torque generado por cada segmento
   - El torque total del sistema
   - La fuerza muscular mínima requerida para mantener la posición

## Fundamentos Físicos

La aplicación se basa en los siguientes principios de física:

1. **Cálculo del peso** (W = m × g):
   - Donde m es la masa en kg y g es la aceleración gravitacional (9.81 m/s²)

2. **Cálculo del torque** (τ = W × d × sin(θ)):
   - Donde W es el peso, d es la distancia al eje de rotación, y θ es el ángulo del segmento respecto a la horizontal

3. **Fuerza muscular requerida** (F = τ / r):
   - Donde τ es el torque total y r es el brazo de palanca del músculo

## Simplificaciones del Modelo

- Se considera el cuerpo humano como un sistema de segmentos rígidos
- Se asume masa uniforme por segmento
- Las articulaciones se modelan sin fricción
- Solo se analizan posiciones estáticas (no dinámicas)
- No se considera la resistencia aerodinámica ni fatiga muscular

## Proyecto Académico

Esta aplicación forma parte de un proyecto académico para el curso de Física I (FIS-01 - FCV1) y se basa en los conceptos de torque, equilibrio estático y biomecánica.

## Archivo requirements.txt

```
streamlit>=1.24.0
numpy>=1.24.3
```
