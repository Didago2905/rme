# RME WebSafe Specification v1

## Estado

**Versión:** 1.0 (Draft)

Este documento define el estándar WebSafe utilizado por RME para producir archivos compatibles con Streaming App.

No representa las capacidades generales de los navegadores ni de FFmpeg.

Representa el contrato interno entre RME y Streaming App.

---

# Filosofía

El objetivo de RME no es únicamente convertir archivos.

Su objetivo es construir una biblioteca multimedia consistente.

Cada archivo generado debe cumplir reglas técnicas y editoriales para ofrecer una experiencia uniforme dentro del ecosistema R.I.T.M.O.

---

# Reglas Técnicas

## Contenedor

Obligatorio

- MP4

No compatibles

- MKV
- AVI
- MOV
- TS
- WebM

---

## Video

Codec

- H.264 (AVC)

Profile

- High

Pixel Format

- yuv420p

Scan Type

- Progressive

Resolución

Actualmente sin restricciones.

Streaming App deberá soportar:

- 480p
- 720p
- 1080p
- 4K (futuro)

---

## Audio

Codec

- AAC-LC

Canales

Permitidos

- Stereo
- 5.1

Sample Rate

Sin restricción por el momento.

Se aceptan:

- 44100 Hz
- 48000 Hz

---

## Subtítulos

Compatibles.

La política editorial decidirá cuáles conservar.

---

# Reglas Editoriales

Estas reglas no existen por compatibilidad.

Existen para mantener una biblioteca limpia y consistente.

---

## Audio

Conservar

- Español (preferentemente Latino)
- Idioma original

Eliminar

- Comentarios del director
- Audio descriptivo
- Doblajes no deseados

La pista predeterminada deberá ser Español cuando exista.

Si no existe Español:

La pista predeterminada será el idioma original.

---

## Subtítulos

Conservar

- Español
- Inglés

Eliminar

- Resto de idiomas

Casos especiales (pendiente)

- Signs & Songs
- Forced
- SDH

---

# Validation Engine

El Validation Engine evaluará únicamente si un archivo cumple esta especificación.

No realizará conversiones.

No modificará metadata.

No cambiará pistas.

Su única responsabilidad será generar un ValidationResult.

---

# Conversion Planner

El Conversion Planner utilizará el ValidationResult para construir un plan de conversión.

Ejemplos

- Cambiar contenedor
- Cambiar codec
- Reordenar pistas
- Cambiar pista por defecto
- Eliminar idiomas
- Eliminar subtítulos
- Convertir subtítulos

---

# Streaming App

Streaming App no debe decidir qué pista reproducir.

Debe asumir que todos los archivos producidos por RME cumplen esta especificación.

Esto simplifica el reproductor y mantiene una experiencia consistente.

---

# Casos Especiales (Pendientes)

Anime

- Signs & Songs
- Forced

Películas

- Forced subtitles

Series

- Español Latino
- Español España

Documentales

- Múltiples narraciones

Estos casos serán incorporados conforme se analicen nuevos archivos de referencia.

---

# Archivos de Referencia

Actualmente el estándar se basa en el análisis de:

Frieren S01E01 WEBSAFE NVENC.mp4

Características principales

Container

MP4

Video

H264 High

yuv420p

1920x1080

Audio

AAC LC

Español

Japonés

Subtítulos

Inglés

Este archivo constituye el primer Golden Sample del estándar WebSafe.