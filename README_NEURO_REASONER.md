# NEURO-REASONER AI v1.0

## Sistema Experimental de Inteligencia Artificial con Capacidad de Razonamiento

### 📖 Descripción

NEURO-REASONER AI es un sistema experimental de inteligencia artificial diseñado para simular procesos de razonamiento similares a los humanos. Implementa múltiples estrategias de razonamiento lógico y cuenta con capacidad de aprendizaje adaptativo.

### 🎯 Características Principales

- **Múltiples Tipos de Razonamiento:**
  - Deductivo (Modus Ponens, Modus Tollens, Silogismo Hipotético)
  - Inductivo (Generalización de patrones)
  - Abductivo (Búsqueda de la mejor explicación)
  - Analógico (Razonamiento por similitud)
  - Causal (Relaciones causa-efecto)

- **Base de Conocimiento Semántica:**
  - Red de conceptos interrelacionados
  - Propiedades y relaciones entre nodos
  - Sistema de confianza dinámico
  - Timestamps para seguimiento temporal

- **Motor de Inferencia:**
  - Reglas de inferencia personalizables
  - Evaluación de premisas
  - Cadenas de razonamiento trazables
  - Ponderación de confianza

- **Sistema de Aprendizaje:**
  - Adquisición de nuevos conceptos
  - Aprendizaje de reglas de inferencia
  - Ajuste adaptativo de parámetros
  - Retroalimentación positiva/negativa

- **Trazabilidad Completa:**
  - Historial de pensamientos
  - Cadena de razonamiento documentada
  - Niveles de confianza en cada paso
  - Perspectivas alternativas

### 🚀 Instalación y Uso

No requiere dependencias externas. Solo Python 3.6+.

```bash
python3 neuro_reasoner_ai.py
```

### 📋 Ejemplo de Uso Programático

```python
from neuro_reasoner_ai import NeuralReasoner

# Crear instancia de la IA
ai = NeuralReasoner(name="MiAsistente")

# Realizar razonamiento sobre una consulta
resultado = ai.reason("¿Qué es la lógica?")

# Imprimir respuesta
print(f"Respuesta: {resultado['answer']}")
print(f"Confianza: {resultado['confidence']:.2%}")

# Aprender nuevo conocimiento
ai.learn({
    "concept": "inteligencia_artificial",
    "properties": {
        "type": "field",
        "category": "computer_science",
        "related": ["machine_learning", "reasoning"]
    },
    "confidence": 0.95
})

# Obtener estado del sistema
estado = ai.get_status()
print(estado)

# Exportar conocimiento
json_export = ai.export_knowledge()
```

### 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────┐
│              NEURO-REASONER AI                      │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │   Análisis  │  │  Recuperación│  │  Inferencia│ │
│  │   de Query  │→ │  de Conoci.  │→ │  de Reglas │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
│         ↓                ↓                 ↓        │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │  Evaluación │  │  Síntesis de │  │  Respuesta │ │
│  │  de Conclus.│→ │  Respuesta   │→ │  Final     │ │
│  └─────────────┘  └──────────────┘  └────────────┘ │
├─────────────────────────────────────────────────────┤
│           Base de Conocimiento Semántica            │
│  ┌──────────────────────────────────────────────┐  │
│  │  Nodos • Relaciones • Confianza • Tiempo    │  │
│  └──────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────┤
│              Módulo de Aprendizaje                  │
│  ┌──────────────────────────────────────────────┐  │
│  │  Nuevo Conocimiento • Reglas • Feedback     │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### 🧪 Pruebas Incluidas

El script incluye 5 pruebas de razonamiento automático:

1. **Definición conceptual** - "¿Qué es el razonamiento lógico?"
2. **Silogismo clásico** - "Si todos los humanos son mortales..."
3. **Razonamiento causal** - "¿Por qué existe la causa y efecto?"
4. **Análisis relacional** - "Analiza la relación entre conocimiento y verdad"
5. **Pregunta procedimental** - "¿Cómo se produce el aprendizaje...?"

### 📊 Métricas del Sistema

- **Nodos de conocimiento iniciales:** 10 conceptos fundamentales
- **Reglas de inferencia:** 5 reglas lógicas básicas
- **Niveles de confianza:** 6 niveles (de muy bajo a cierto)
- **Umbral de decisión:** 0.6 (configurable)
- **Tasa de aprendizaje:** 0.1 (adaptativa)

### 🔧 Personalización

Puedes extender el sistema añadiendo:

1. **Nuevos conceptos a la base de conocimiento:**
```python
ai.knowledge_base["nuevo_concepto"] = KnowledgeNode(
    concept="nuevo_concepto",
    properties={"type": "custom", "category": "mi_categoria"},
    confidence=0.8
)
```

2. **Nuevas reglas de inferencia:**
```python
from neuro_reasoner_ai import InferenceRule, ReasoningType, ConfidenceLevel

ai.inference_rules.append(InferenceRule(
    id="mi_regla",
    premise=["premisa1", "premisa2"],
    conclusion="conclusión",
    confidence=ConfidenceLevel.HIGH.value,
    rule_type=ReasoningType.DEDUCTIVE
))
```

3. **Ajuste de parámetros:**
```python
ai.learning_rate = 0.15  # Más rápido
ai.decision_threshold = 0.5  # Menos exigente
```

### 📝 Estructura de Datos

#### KnowledgeNode
- `concept`: Nombre del concepto
- `properties`: Diccionario de propiedades
- `relations`: Lista de tuplas (tipo_relación, objetivo)
- `confidence`: Nivel de confianza (0.0-1.0)
- `source`: Origen del conocimiento
- `timestamp`: Marca temporal

#### InferenceRule
- `id`: Identificador único
- `premise`: Lista de premisas
- `conclusion`: Conclusión derivada
- `confidence`: Confianza en la regla
- `rule_type`: Tipo de razonamiento

#### Thought
- `content`: Contenido del pensamiento
- `thought_type`: Tipo (analysis, retrieval, inference, etc.)
- `confidence`: Confianza en este pensamiento
- `dependencies`: Dependencias de otros pensamientos
- `timestamp`: Marca temporal

### 🎓 Casos de Uso Experimentales

1. **Sistemas tutores inteligentes** - Explicar conceptos con razonamiento trazable
2. **Diagnóstico asistido** - Razonamiento abductivo para hipótesis
3. **Análisis jurídico** - Aplicación de reglas lógicas a casos
4. **Investigación científica** - Generación de hipótesis inductivas
5. **Asistentes de decisión** - Evaluación de alternativas con confianza

### ⚠️ Limitaciones

Este es un sistema **experimental** con las siguientes limitaciones:

- No utiliza redes neuronales profundas reales
- El conocimiento inicial es limitado
- Las inferencias dependen de la calidad de las reglas definidas
- No tiene acceso a información externa en tiempo real
- La comprensión del lenguaje natural es básica

### 📄 Licencia

Código experimental de dominio público. Úsalo, modifícalo y mejóralo libremente.

### 🤝 Contribuciones

Este proyecto está abierto a mejoras y extensiones. Algunas ideas:

- [ ] Integración con modelos de lenguaje grandes (LLMs)
- [ ] Persistencia de conocimiento en base de datos
- [ ] Interfaz gráfica web
- [ ] Soporte para múltiples idiomas
- [ ] Razónamiento probabilístico bayesiano
- [ ] Aprendizaje por refuerzo
- [ ] Visualización de la red semántica

---

**Autor:** Asistente de IA  
**Versión:** 1.0  
**Estado:** Experimental  
**Fecha:** 2024
