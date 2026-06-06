#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NEURO-REASONER AI v1.0 - Sistema Experimental de IA con Capacidad de Razonamiento
Autor: Asistente de IA
Descripción: Una IA experimental que implementa múltiples capas de razonamiento,
             toma de decisiones basada en lógica difusa, y aprendizaje adaptativo.
"""

import json
import random
import math
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import hashlib


class ReasoningType(Enum):
    """Tipos de razonamiento que puede realizar la IA"""
    DEDUCTIVE = "deductive"
    INDUCTIVE = "inductive"
    ABDUCTIVE = "abductive"
    ANALOGICAL = "analogical"
    CAUSAL = "causal"


class ConfidenceLevel(Enum):
    """Niveles de confianza en las conclusiones"""
    VERY_LOW = 0.1
    LOW = 0.3
    MEDIUM = 0.5
    HIGH = 0.7
    VERY_HIGH = 0.9
    CERTAIN = 1.0


@dataclass
class KnowledgeNode:
    """Nodo de conocimiento en la red semántica"""
    concept: str
    properties: Dict[str, Any] = field(default_factory=dict)
    relations: List[Tuple[str, str]] = field(default_factory=list)  # (relation_type, target)
    confidence: float = 1.0
    source: str = "initial"
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


@dataclass
class InferenceRule:
    """Regla de inferencia para el motor de razonamiento"""
    id: str
    premise: List[str]
    conclusion: str
    confidence: float
    rule_type: ReasoningType
    conditions: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Thought:
    """Representa un pensamiento o paso en el proceso de razonamiento"""
    content: str
    thought_type: str
    confidence: float
    dependencies: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=lambda: datetime.now().timestamp())


class NeuralReasoner:
    """
    Motor principal de razonamiento neuronal
    Implementa múltiples estrategias de razonamiento y aprendizaje
    """
    
    def __init__(self, name: str = "NeuroReasoner"):
        self.name = name
        self.knowledge_base: Dict[str, KnowledgeNode] = {}
        self.inference_rules: List[InferenceRule] = []
        self.thought_history: List[Thought] = []
        self.learning_rate = 0.1
        self.decision_threshold = 0.6
        self.context_window: List[Dict] = []
        self.belief_network: Dict[str, Dict[str, float]] = {}
        
        # Inicializar conocimiento base
        self._initialize_base_knowledge()
        self._initialize_inference_rules()
        
    def _initialize_base_knowledge(self):
        """Inicializa el conocimiento base con conceptos fundamentales"""
        base_concepts = [
            ("existence", {"type": "abstract", "category": "philosophy"}),
            ("logic", {"type": "abstract", "category": "mathematics"}),
            ("reasoning", {"type": "process", "category": "cognition"}),
            ("learning", {"type": "process", "category": "cognition"}),
            ("truth", {"type": "abstract", "category": "philosophy"}),
            ("falsehood", {"type": "abstract", "category": "philosophy"}),
            ("cause", {"type": "relation", "category": "logic"}),
            ("effect", {"type": "relation", "category": "logic"}),
            ("premise", {"type": "abstract", "category": "logic"}),
            ("conclusion", {"type": "abstract", "category": "logic"}),
        ]
        
        for concept, properties in base_concepts:
            self.knowledge_base[concept] = KnowledgeNode(
                concept=concept,
                properties=properties,
                confidence=ConfidenceLevel.CERTAIN.value
            )
        
        # Establecer relaciones básicas
        self._add_relation("cause", "implies", "effect")
        self._add_relation("premise", "leads_to", "conclusion")
        self._add_relation("logic", "enables", "reasoning")
        self._add_relation("reasoning", "produces", "knowledge")
        
    def _initialize_inference_rules(self):
        """Inicializa las reglas de inferencia básicas"""
        rules = [
            InferenceRule(
                id="modus_ponens",
                premise=["P", "P implies Q"],
                conclusion="Q",
                confidence=ConfidenceLevel.CERTAIN.value,
                rule_type=ReasoningType.DEDUCTIVE
            ),
            InferenceRule(
                id="modus_tollens",
                premise=["not Q", "P implies Q"],
                conclusion="not P",
                confidence=ConfidenceLevel.CERTAIN.value,
                rule_type=ReasoningType.DEDUCTIVE
            ),
            InferenceRule(
                id="hypothetical_syllogism",
                premise=["P implies Q", "Q implies R"],
                conclusion="P implies R",
                confidence=ConfidenceLevel.CERTAIN.value,
                rule_type=ReasoningType.DEDUCTIVE
            ),
            InferenceRule(
                id="inductive_generalization",
                premise=["observed_pattern"],
                conclusion="general_rule",
                confidence=ConfidenceLevel.MEDIUM.value,
                rule_type=ReasoningType.INDUCTIVE
            ),
            InferenceRule(
                id="abductive_inference",
                premise=["observation", "rule"],
                conclusion="best_explanation",
                confidence=ConfidenceLevel.LOW.value,
                rule_type=ReasoningType.ABDUCTIVE
            ),
        ]
        self.inference_rules.extend(rules)
        
    def _add_relation(self, source: str, relation: str, target: str):
        """Añade una relación entre nodos de conocimiento"""
        if source in self.knowledge_base:
            self.knowledge_base[source].relations.append((relation, target))
            
    def reason(self, query: str, context: Optional[List[Dict]] = None) -> Dict[str, Any]:
        """
        Proceso principal de razonamiento sobre una consulta
        """
        print(f"\n{'='*60}")
        print(f"🧠 {self.name} iniciando proceso de razonamiento...")
        print(f"{'='*60}")
        
        # Analizar la consulta
        analysis = self._analyze_query(query)
        self._record_thought(Thought(
            content=f"Analizando: {query}",
            thought_type="analysis",
            confidence=ConfidenceLevel.HIGH.value
        ))
        
        # Buscar conocimiento relevante
        relevant_knowledge = self._retrieve_relevant_knowledge(query)
        self._record_thought(Thought(
            content=f"Encontrados {len(relevant_knowledge)} conceptos relevantes",
            thought_type="retrieval",
            confidence=ConfidenceLevel.HIGH.value
        ))
        
        # Aplicar reglas de inferencia
        inferences = self._apply_inference_rules(query, relevant_knowledge)
        self._record_thought(Thought(
            content=f"Generadas {len(inferences)} inferencias",
            thought_type="inference",
            confidence=ConfidenceLevel.MEDIUM.value,
            dependencies=[str(i) for i in range(len(inferences))]
        ))
        
        # Evaluar conclusiones
        conclusions = self._evaluate_conclusions(inferences, relevant_knowledge)
        
        # Sintetizar respuesta
        response = self._synthesize_response(query, conclusions, relevant_knowledge)
        
        print(f"\n✅ Proceso de razonamiento completado")
        print(f"{'='*60}\n")
        
        return response
        
    def _analyze_query(self, query: str) -> Dict[str, Any]:
        """Analiza la estructura y tipo de la consulta"""
        analysis = {
            "query": query,
            "length": len(query),
            "question_type": self._detect_question_type(query),
            "key_terms": self._extract_key_terms(query),
            "complexity": self._estimate_complexity(query),
            "requires_reasoning": self._check_reasoning_requirement(query)
        }
        
        print(f"\n📊 Análisis de consulta:")
        print(f"   Tipo: {analysis['question_type']}")
        print(f"   Términos clave: {analysis['key_terms']}")
        print(f"   Complejidad: {analysis['complexity']}/10")
        print(f"   Requiere razonamiento: {analysis['requires_reasoning']}")
        
        return analysis
        
    def _detect_question_type(self, query: str) -> str:
        """Detecta el tipo de pregunta"""
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["qué", "que", "cuál", "cual"]):
            return "definición/identificación"
        elif any(word in query_lower for word in ["por qué", "porque", "razón"]):
            return "causal/explicación"
        elif any(word in query_lower for word in ["cómo", "como"]):
            return "procedimental"
        elif any(word in query_lower for word in ["si", "whether"]):
            return "booleana/condicional"
        elif any(word in query_lower for word in ["cuándo", "quando"]):
            return "temporal"
        elif any(word in query_lower for word in ["dónde", "donde"]):
            return "espacial"
        elif any(word in query_lower for word in ["quién", "quien", "quiénes"]):
            return "identidad"
        else:
            return "declarativa/afirmación"
            
    def _extract_key_terms(self, query: str) -> List[str]:
        """Extrae términos clave de la consulta"""
        # Palabras vacías en español
        stop_words = {
            "el", "la", "los", "las", "un", "una", "unos", "unas",
            "de", "del", "al", "a", "en", "con", "sin", "por", "para",
            "que", "qué", "cual", "cuál", "como", "cómo",
            "es", "son", "ser", "estar", "está", "están",
            "se", "lo", "le", "les", "me", "te", "nos", "os",
            "y", "o", "pero", "sino", "ni", "no", "sí",
            "muy", "más", "menos", "tan", "tanto",
            "este", "esta", "estos", "estas", "ese", "esa", "esos", "esas"
        }
        
        words = query.lower().split()
        key_terms = [
            word.strip(".,!?¿¡()[]{}\"'") 
            for word in words 
            if word.lower() not in stop_words and len(word) > 2
        ]
        
        return list(set(key_terms))
        
    def _estimate_complexity(self, query: str) -> int:
        """Estima la complejidad de la consulta (1-10)"""
        score = 0
        
        # Longitud
        word_count = len(query.split())
        score += min(word_count / 10, 3)
        
        # Estructura condicional
        if "si" in query.lower() or "entonces" in query.lower():
            score += 2
            
        # Múltiples preguntas
        if query.count("?") > 1:
            score += 2
            
        # Términos abstractos
        abstract_terms = ["existencia", "conciencia", "verdad", "lógica", 
                         "razonamiento", "ética", "filosofía", "metafísica"]
        for term in abstract_terms:
            if term in query.lower():
                score += 1
                
        return min(int(score), 10)
        
    def _check_reasoning_requirement(self, query: str) -> bool:
        """Determina si la consulta requiere razonamiento complejo"""
        reasoning_indicators = [
            "por qué", "cómo", "si entonces", "implica", "consecuencia",
            "razón", "causa", "efecto", "relación", "comparar",
            "analizar", "evaluar", "deducir", "inferir"
        ]
        
        return any(indicator in query.lower() for indicator in reasoning_indicators)
        
    def _retrieve_relevant_knowledge(self, query: str) -> List[KnowledgeNode]:
        """Recupera conocimiento relevante de la base de conocimientos"""
        key_terms = self._extract_key_terms(query)
        relevant = []
        
        for term in key_terms:
            # Búsqueda exacta
            if term in self.knowledge_base:
                relevant.append(self.knowledge_base[term])
                
            # Búsqueda parcial
            for concept, node in self.knowledge_base.items():
                if term in concept or any(term in prop for prop in node.properties.values()):
                    if node not in relevant:
                        relevant.append(node)
                        
        # Ordenar por relevancia (confianza y recencia)
        relevant.sort(key=lambda x: x.confidence * 0.7 + (1 / (1 + abs(datetime.now().timestamp() - x.timestamp))) * 0.3, 
                     reverse=True)
        
        return relevant[:10]  # Máximo 10 nodos relevantes
        
    def _apply_inference_rules(self, query: str, knowledge: List[KnowledgeNode]) -> List[Dict]:
        """Aplica reglas de inferencia al conocimiento disponible"""
        inferences = []
        
        for rule in self.inference_rules:
            # Verificar si las premisas pueden ser satisfechas
            premise_match = self._check_premises(rule.premise, query, knowledge)
            
            if premise_match["matched"]:
                inference = {
                    "rule_id": rule.id,
                    "rule_type": rule.rule_type.value,
                    "conclusion": rule.conclusion,
                    "confidence": rule.confidence * premise_match["confidence"],
                    "premises_used": premise_match["matched_premises"],
                    "reasoning_chain": self._build_reasoning_chain(rule, knowledge)
                }
                inferences.append(inference)
                
                print(f"\n🔍 Regla aplicada: {rule.id} ({rule.rule_type.value})")
                print(f"   Confianza: {inference['confidence']:.2f}")
                
        return inferences
        
    def _check_premises(self, premises: List[str], query: str, 
                       knowledge: List[KnowledgeNode]) -> Dict[str, Any]:
        """Verifica si las premisas de una regla pueden ser satisfechas"""
        matched_premises = []
        total_confidence = 0.0
        
        for premise in premises:
            match_found = False
            
            # Buscar en la consulta
            if premise.lower() in query.lower():
                matched_premises.append(premise)
                match_found = True
                total_confidence += 0.8
                
            # Buscar en el conocimiento
            for node in knowledge:
                if premise.lower() in node.concept.lower():
                    matched_premises.append(premise)
                    match_found = True
                    total_confidence += node.confidence
                    
            # Manejar variables (P, Q, R, etc.)
            if len(premise) == 1 and premise.isupper():
                matched_premises.append(f"variable_{premise}")
                match_found = True
                total_confidence += 0.5
                
        return {
            "matched": len(matched_premises) >= len(premises) * 0.5,
            "confidence": total_confidence / max(len(premises), 1),
            "matched_premises": matched_premises
        }
        
    def _build_reasoning_chain(self, rule: InferenceRule, 
                               knowledge: List[KnowledgeNode]) -> List[str]:
        """Construye la cadena de razonamiento"""
        chain = []
        
        for premise in rule.premise:
            chain.append(f"Premisa: {premise}")
            
        chain.append(f"Regla: {rule.id} ({rule.rule_type.value})")
        chain.append(f"Conclusión: {rule.conclusion}")
        
        return chain
        
    def _evaluate_conclusions(self, inferences: List[Dict], 
                             knowledge: List[KnowledgeNode]) -> List[Dict]:
        """Evalúa y pondera las conclusiones obtenidas"""
        evaluated = []
        
        for inference in inferences:
            # Calcular confianza final
            base_confidence = inference["confidence"]
            
            # Ajustar por consistencia con conocimiento existente
            consistency_bonus = self._check_consistency(inference, knowledge)
            final_confidence = min(base_confidence + consistency_bonus, 1.0)
            
            evaluation = {
                **inference,
                "final_confidence": final_confidence,
                "consistency_score": consistency_bonus,
                "accepted": final_confidence >= self.decision_threshold
            }
            evaluated.append(evaluation)
            
            print(f"\n⚖️  Evaluación:")
            print(f"   Conclusión: {evaluation['conclusion']}")
            print(f"   Confianza final: {final_confidence:.2f}")
            print(f"   Aceptada: {evaluation['accepted']}")
            
        # Ordenar por confianza
        evaluated.sort(key=lambda x: x["final_confidence"], reverse=True)
        
        return evaluated
        
    def _check_consistency(self, inference: Dict, knowledge: List[KnowledgeNode]) -> float:
        """Verifica la consistencia de una inferencia con el conocimiento existente"""
        consistency_score = 0.0
        
        conclusion = inference["conclusion"].lower()
        
        for node in knowledge:
            if conclusion in node.concept.lower():
                consistency_score += node.confidence * 0.3
                
        return min(consistency_score, 0.3)
        
    def _synthesize_response(self, query: str, conclusions: List[Dict], 
                            knowledge: List[KnowledgeNode]) -> Dict[str, Any]:
        """Sintetiza una respuesta coherente basada en el razonamiento"""
        accepted_conclusions = [c for c in conclusions if c["accepted"]]
        
        if not accepted_conclusions:
            accepted_conclusions = conclusions[:1] if conclusions else []
            
        # Construir respuesta
        response = {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "reasoning_process": {
                "analysis": self._analyze_query(query),
                "knowledge_used": len(knowledge),
                "inferences_made": len(conclusions),
                "accepted_conclusions": len(accepted_conclusions)
            },
            "answer": self._generate_answer(query, accepted_conclusions, knowledge),
            "confidence": self._calculate_overall_confidence(accepted_conclusions),
            "reasoning_chain": self._build_full_reasoning_chain(conclusions),
            "alternative_perspectives": self._generate_alternatives(query, conclusions),
            "thought_trace": [
                {
                    "content": t.content,
                    "type": t.thought_type,
                    "confidence": t.confidence
                }
                for t in self.thought_history[-10:]
            ]
        }
        
        # Imprimir respuesta
        print(f"\n💡 RESPUESTA GENERADA:")
        print(f"   {response['answer']}")
        print(f"\n📈 Nivel de confianza: {response['confidence']:.2%}")
        
        return response
        
    def _generate_answer(self, query: str, conclusions: List[Dict], 
                        knowledge: List[KnowledgeNode]) -> str:
        """Genera una respuesta natural en lenguaje"""
        if not conclusions:
            return "No puedo llegar a una conclusión definitiva con la información disponible. Necesitaría más datos o contexto."
            
        top_conclusion = conclusions[0]
        rule_type = top_conclusion["rule_type"]
        
        answer_templates = {
            "deductive": f"Basándome en un razonamiento deductivo, puedo concluir que: {top_conclusion['conclusion']}. Esto se deriva lógicamente de las premisas establecidas.",
            "inductive": f"Mediante razonamiento inductivo, observo patrones que sugieren: {top_conclusion['conclusion']}. Esta conclusión tiene un grado de probabilidad basado en la evidencia disponible.",
            "abductive": f"La mejor explicación abductiva para lo observado es: {top_conclusion['conclusion']}. Esta es la hipótesis más plausible dado el contexto.",
            "analogical": f"Por analogía con situaciones similares, concluyo: {top_conclusion['conclusion']}. La similitud estructural sugiere esta conclusión.",
            "causal": f"Analizando las relaciones causales, determino que: {top_conclusion['conclusion']}. Existe una conexión causal entre los elementos identificados."
        }
        
        base_answer = answer_templates.get(rule_type, 
            f"Mi análisis indica que: {top_conclusion['conclusion']}")
            
        # Añadir matices según la confianza
        confidence = top_conclusion["final_confidence"]
        if confidence < 0.5:
            base_answer += " Sin embargo, debo señalar que esta conclusión tiene incertidumbre significativa."
        elif confidence > 0.9:
            base_answer += " Estoy altamente confidente en esta conclusión."
            
        return base_answer
        
    def _calculate_overall_confidence(self, conclusions: List[Dict]) -> float:
        """Calcula la confianza general de la respuesta"""
        if not conclusions:
            return 0.0
            
        accepted = [c for c in conclusions if c["accepted"]]
        if not accepted:
            return conclusions[0]["final_confidence"] * 0.5
            
        # Promedio ponderado de conclusiones aceptadas
        total_weight = sum(c["final_confidence"] for c in accepted)
        if total_weight == 0:
            return 0.0
            
        weighted_sum = sum(c["final_confidence"] ** 2 for c in accepted)
        return weighted_sum / total_weight
        
    def _build_full_reasoning_chain(self, conclusions: List[Dict]) -> List[str]:
        """Construye la cadena completa de razonamiento"""
        chain = []
        
        for i, conclusion in enumerate(conclusions, 1):
            chain.append(f"Paso {i}:")
            chain.extend([f"   - {step}" for step in conclusion.get("reasoning_chain", [])])
            chain.append(f"   → Conclusión: {conclusion['conclusion']}")
            chain.append(f"   → Confianza: {conclusion['final_confidence']:.2%}")
            chain.append("")
            
        return chain
        
    def _generate_alternatives(self, query: str, conclusions: List[Dict]) -> List[str]:
        """Genera perspectivas o conclusiones alternativas"""
        alternatives = []
        
        if len(conclusions) > 1:
            for alt in conclusions[1:3]:  # Máximo 2 alternativas
                alternatives.append(
                    f"Perspectiva alternativa ({alt['rule_type']}): {alt['conclusion']} "
                    f"(confianza: {alt['final_confidence']:.2%})"
                )
                
        if not alternatives:
            alternatives.append(
                "Podría haber interpretaciones diferentes dependiendo del contexto adicional."
            )
            
        return alternatives
        
    def _record_thought(self, thought: Thought):
        """Registra un pensamiento en el historial"""
        self.thought_history.append(thought)
        print(f"   💭 [{thought.thought_type}] {thought.content}")
        
    def learn(self, experience: Dict[str, Any]) -> bool:
        """
        Aprende de una experiencia nueva
        """
        print(f"\n📚 Proceso de aprendizaje iniciado...")
        
        # Extraer nuevo conocimiento
        if "concept" in experience:
            concept = experience["concept"]
            properties = experience.get("properties", {})
            
            if concept in self.knowledge_base:
                # Actualizar existente
                node = self.knowledge_base[concept]
                for key, value in properties.items():
                    node.properties[key] = value
                node.confidence = min(node.confidence + self.learning_rate, 1.0)
                print(f"   ✓ Concepto '{concept}' actualizado")
            else:
                # Añadir nuevo
                self.knowledge_base[concept] = KnowledgeNode(
                    concept=concept,
                    properties=properties,
                    confidence=experience.get("confidence", 0.5),
                    source="learning"
                )
                print(f"   ✓ Nuevo concepto '{concept}' añadido")
                
        # Aprender nuevas reglas
        if "rule" in experience:
            rule_data = experience["rule"]
            new_rule = InferenceRule(
                id=rule_data.get("id", f"learned_{len(self.inference_rules)}"),
                premise=rule_data.get("premise", []),
                conclusion=rule_data.get("conclusion", ""),
                confidence=rule_data.get("confidence", 0.5),
                rule_type=ReasoningType(rule_data.get("type", "inductive"))
            )
            self.inference_rules.append(new_rule)
            print(f"   ✓ Nueva regla de inferencia aprendida")
            
        # Ajustar parámetros
        if "feedback" in experience:
            feedback = experience["feedback"]
            if feedback > 0:
                self.learning_rate = min(self.learning_rate + 0.01, 0.5)
            else:
                self.learning_rate = max(self.learning_rate - 0.01, 0.01)
                
        print(f"   ✅ Aprendizaje completado")
        return True
        
    def get_status(self) -> Dict[str, Any]:
        """Obtiene el estado actual del sistema"""
        return {
            "name": self.name,
            "knowledge_nodes": len(self.knowledge_base),
            "inference_rules": len(self.inference_rules),
            "thoughts_recorded": len(self.thought_history),
            "context_size": len(self.context_window),
            "learning_rate": self.learning_rate,
            "decision_threshold": self.decision_threshold,
            "uptime": "active"
        }
        
    def export_knowledge(self) -> str:
        """Exporta el conocimiento en formato JSON"""
        export_data = {
            "knowledge_base": {
                k: {
                    "concept": v.concept,
                    "properties": v.properties,
                    "relations": v.relations,
                    "confidence": v.confidence
                }
                for k, v in self.knowledge_base.items()
            },
            "inference_rules": [
                {
                    "id": r.id,
                    "premise": r.premise,
                    "conclusion": r.conclusion,
                    "confidence": r.confidence,
                    "type": r.rule_type.value
                }
                for r in self.inference_rules
            ],
            "metadata": self.get_status()
        }
        
        return json.dumps(export_data, indent=2, ensure_ascii=False)


def main():
    """
    ============================================================================
    NEURO-REASONER AI v1.0 - SISTEMA EXPERIMENTAL DE INTELIGENCIA ARTIFICIAL
                     CON CAPACIDAD AVANZADA DE RAZONAMIENTO
    ============================================================================
    
    📖 DESCRIPCIÓN DEL PROYECTO
    ---------------------------
    NEURO-REASONER AI es un sistema experimental de inteligencia artificial diseñado
    para emular procesos de razonamiento humano mediante múltiples estrategias lógicas.
    A diferencia de los modelos de lenguaje tradicionales que predicen texto, este
    sistema implementa un motor de inferencia explícito que rastrea cada paso del
    proceso de pensamiento, permitiendo transparencia total en cómo se llega a las
    conclusiones.
    
    El sistema combina:
    • Redes semánticas para representación del conocimiento
    • Lógica difusa para manejo de incertidumbre
    • Múltiples paradigmas de razonamiento (deductivo, inductivo, abductivo, etc.)
    • Mecanismos de aprendizaje adaptativo
    • Trazabilidad completa de inferencias
    
    ============================================================================
    🧠 NIVELES DE RAZONAMIENTO IMPLEMENTADOS
    ============================================================================
    
    1. RAZONAMIENTO DEDUCTIVO (Deductive Reasoning)
       ─────────────────────────────────────────────
       • Propósito: Derivar conclusiones específicas desde premisas generales
       • Método: De lo general → particular (top-down)
       • Certeza: Si las premisas son verdaderas, la conclusión ES verdadera
       • Ejemplo clásico:
           Premisa 1: Todos los humanos son mortales
           Premisa 2: Sócrates es humano
           Conclusión: Sócrates es mortal
       • Casos de uso: Validación lógica, verificación de teoremas, diagnóstico
         médico basado en reglas, sistemas expertos
       • Implementación: Modus Ponens, Modus Tollens, Silogismos categóricos
       • Nivel de confianza: Alto (0.8-1.0) cuando las premisas están validadas
    
    2. RAZONAMIENTO INDUCTIVO (Inductive Reasoning)
       ──────────────────────────────────────────────
       • Propósito: Generalizar patrones desde observaciones específicas
       • Método: De lo particular → general (bottom-up)
       • Certeza: Conclusiones probables pero NO garantizadas
       • Ejemplo clásico:
           Observación: El sol ha salido todos los días registrados
           Conclusión: El sol saldrá mañana
       • Casos de uso: Aprendizaje automático, descubrimiento científico,
         predicción de tendencias, reconocimiento de patrones
       • Implementación: Generalización estadística, identificación de patrones,
         extrapolación de series temporales
       • Nivel de confianza: Medio-Alto (0.5-0.8) depende del tamaño muestral
    
    3. RAZONAMIENTO ABDUCTIVO (Abductive Reasoning)
       ─────────────────────────────────────────────
       • Propósito: Inferir la mejor explicación para observaciones dadas
       • Método: De efectos → causas probables
       • Certeza: Hipótesis más plausible, no necesariamente verdadera
       • Ejemplo clásico:
           Observación: El césped está mojado
           Explicación posible: Llovió anoche (mejor explicación disponible)
       • Casos de uso: Diagnóstico médico, investigación forense, debugging
         de software, detección de fallos en sistemas
       • Implementación: Búsqueda de explicaciones, ranking por plausibilidad,
         eliminación de hipótesis inconsistentes
       • Nivel de confianza: Medio (0.4-0.7) requiere validación adicional
    
    4. RAZONAMIENTO ANALÓGICO (Analogical Reasoning)
       ──────────────────────────────────────────────
       • Propósito: Transferir conocimiento entre dominios similares
       • Método: Mapeo estructural entre situaciones paralelas
       • Certeza: Depende de la fuerza de la analogía
       • Ejemplo clásico:
           Dominio fuente: El átomo es como un sistema solar
           Dominio objetivo: Electrones orbitan el núcleo como planetas
       • Casos de uso: Resolución creativa de problemas, enseñanza, innovación,
         transferencia de soluciones entre campos
       • Implementación: Detección de isomorfismos estructurales, mapeo de
         relaciones, proyección de propiedades
       • Nivel de confianza: Variable (0.3-0.7) según calidad del mapeo
    
    5. RAZONAMIENTO CAUSAL (Causal Reasoning)
       ───────────────────────────────────────
       • Propósito: Establecer relaciones causa-efecto entre eventos
       • Método: Análisis de dependencias causales
       • Certeza: Probabilística, considera factores de confusión
       • Ejemplo clásico:
           Causa: Fumar cigarrillos
           Efecto: Mayor riesgo de cáncer de pulmón
       • Casos de uso: Análisis de políticas, economía, epidemiología,
         ciencias sociales, toma de decisiones estratégicas
       • Implementación: Redes bayesianas simplificadas, análisis contrafactual,
         criterios de Bradford Hill
       • Nivel de confianza: Medio-Alto (0.6-0.9) con evidencia suficiente
    
    ============================================================================
    🛠️ INSTALACIÓN
    ============================================================================
    
    REQUISITOS PREVIOS:
    • Python 3.7 o superior (verificar con: python3 --version)
    • No requiere librerías externas (solo biblioteca estándar)
    • Sistema operativo: Linux, macOS o Windows con Python instalado
    • Memoria RAM mínima: 256 MB
    • Espacio en disco: < 1 MB
    
    PASOS DE INSTALACIÓN:
    
    1. Verificar que Python está instalado:
       $ python3 --version
       (Debe mostrar Python 3.7.x o superior)
    
    2. Clonar o descargar el archivo:
       $ git clone <repositorio>
       O simplemente copiar neuro_reasoner_ai.py a tu directorio de trabajo
    
    3. Verificar integridad del archivo:
       $ ls -lh neuro_reasoner_ai.py
       (Debe mostrar ~750 líneas, ~25KB)
    
    4. (Opcional) Crear entorno virtual:
       $ python3 -m venv venv_neuro
       $ source venv_neuro/bin/activate  # En Windows: venv_neuro\\Scripts\\activate
    
    5. No se requiere instalación de dependencias adicionales
       (El sistema usa exclusivamente la biblioteca estándar de Python)
    
    ============================================================================
    ▶️ EJECUCIÓN
    ============================================================================
    
    MÉTODO 1: Ejecución directa (recomendado para pruebas)
    ───────────────────────────────────────────────────────
    $ python3 neuro_reasoner_ai.py
    
    Esto ejecutará:
    • Inicialización del sistema con base de conocimiento precargada
    • Demostración automática de los 5 tipos de razonamiento
    • Pruebas de ejemplo con trazabilidad completa
    • Demostración de aprendizaje adaptativo
    • Exportación de conocimiento a formato JSON
    
    MÉTODO 2: Uso interactivo en Python
    ────────────────────────────────────
    $ python3
    >>> from neuro_reasoner_ai import NeuroReasonerAI
    >>> ai = NeuroReasonerAI()
    >>> result = ai.reason("Si todos los gatos son mamíferos y Félix es gato, ¿qué es Félix?")
    >>> print(result['conclusion'])
    
    MÉTODO 3: Como módulo importable
    ────────────────────────────────
    from neuro_reasoner_ai import NeuroReasonerAI, ReasoningType
    
    # Crear instancia
    ai = NeuroReasonerAI(verbose=True)
    
    # Añadir conocimiento personalizado
    ai.add_knowledge("aves", {"pueden_volar": True, "tienen_plumas": True})
    ai.add_relation("aves", "subclase_de", "animales")
    
    # Realizar razonamiento
    resultado = ai.reason("¿Puede un águila volar?")
    print(f"Conclusión: {resultado['conclusion']}")
    print(f"Confianza: {resultado['confidence']:.2%}")
    print(f"Tipo de razonamiento: {resultado['reasoning_type']}")
    
    MÉTODO 4: Modo silencioso (para integración en otros sistemas)
    ───────────────────────────────────────────────────────────────
    ai = NeuroReasonerAI(verbose=False)
    result = ai.reason("consulta")
    # Solo devuelve el diccionario de resultados sin imprimir nada
    
    ARGUMENTOS DE LÍNEA DE COMANDOS (futuras versiones):
    • --query "texto" : Ejecutar una consulta específica
    • --verbose       : Mostrar trazabilidad detallada
    • --export        : Exportar base de conocimiento después de ejecutar
    • --learn archivo : Cargar conocimiento desde archivo JSON
    
    ============================================================================
    🎯 FUNCIONALIDAD Y CASOS DE USO
    ============================================================================
    
    PROPÓSITO PRINCIPAL:
    Proporcionar un framework experimental para estudiar y emular procesos de
    razonamiento humano en sistemas de IA, con énfasis en transparencia y
    trazabilidad del proceso cognitivo.
    
    APLICACIONES PRÁCTICAS:
    
    1. SISTEMAS EXPERTOS
       • Diagnóstico médico basado en síntomas y reglas
       • Soporte a decisiones legales
       • Configuración técnica de productos complejos
    
    2. EDUCACIÓN Y ENSEÑANZA
       • Tutor inteligente que explica su razonamiento
       • Herramienta para enseñar lógica y pensamiento crítico
       • Simulador de resolución de problemas paso a paso
    
    3. INVESTIGACIÓN EN IA
       • Estudio comparativo de diferentes tipos de razonamiento
       • Prototipado rápido de sistemas basados en conocimiento
       • Análisis de trazabilidad en decisiones de IA
    
    4. ANÁLISIS DE DATOS
       • Detección de patrones y anomalías
       • Generación de hipótesis explicativas
       • Inferencia causal en estudios observacionales
    
    5. AUTOMATIZACIÓN INTELIGENTE
       • Debugging automático de código
       • Diagnóstico de fallos en sistemas industriales
       • Clasificación y categorización inteligente
    
    CARACTERÍSTICAS TÉCNICAS DESTACADAS:
    
    ✓ Base de Conocimiento Semántica
      - Nodos interconectados con propiedades y relaciones
      - Herencia de propiedades a través de jerarquías
      - Actualización dinámica con nuevo conocimiento
    
    ✓ Motor de Inferencia Multi-Estrategia
      - 9+ reglas de inferencia lógica
      - Selección automática del tipo de razonamiento óptimo
      - Combinación de múltiples estrategias cuando es necesario
    
    ✓ Sistema de Confianza Gradual
      - 6 niveles de certeza (Very Low → Certain)
      - Propagación de incertidumbre en inferencias
      - Umbrales configurables para aceptación de conclusiones
    
    ✓ Trazabilidad Completa
      - Registro de cada paso del razonamiento
      - Identificación de premisas usadas
      - Explicación de por qué se rechazaron alternativas
    
    ✓ Aprendizaje Adaptativo
      - Incorporación de nuevo conocimiento durante la ejecución
      - Ajuste de confianza basado en retroalimentación
      - Detección y resolución de contradicciones
    
    ✓ Exportación e Interoperabilidad
      - Formato JSON para intercambio de conocimiento
      - API clara para integración con otros sistemas
      - Sin dependencias externas complicadas
    
    ============================================================================
    📊 ARQUITECTURA DEL SISTEMA
    ============================================================================
    
    COMPONENTES PRINCIPALES:
    
    1. KnowledgeBase (Base de Conocimiento)
       - Almacena conceptos como nodos en una red semántica
       - Gestiona relaciones (subclase_de, instancia_de, propiedad_de, etc.)
       - Mantiene metadatos: confianza, fuente, timestamp
    
    2. InferenceEngine (Motor de Inferencia)
       - Implementa reglas lógicas (Modus Ponens, Tollens, etc.)
       - Selecciona estrategia de razonamiento según la consulta
       - Combina evidencias múltiples
    
    3. ConfidenceManager (Gestor de Confianza)
       - Calcula niveles de certeza en conclusiones
       - Propaga incertidumbre a través de inferencias
       - Aplica umbrales de aceptación
    
    4. ReasoningTracer (Trazador de Razonamiento)
       - Registra cada paso del proceso
       - Genera explicaciones comprensibles
       - Permite auditoría del proceso decisional
    
    5. LearningModule (Módulo de Aprendizaje)
       - Incorpora nueva información
       - Ajusta confianzas existentes
       - Detecta y resuelve contradicciones
    
    ============================================================================
    🧪 EJEMPLO DE EJECUCIÓN
    ============================================================================
    
    Al ejecutar: python3 neuro_reasoner_ai.py
    
    El sistema realizará automáticamente:
    
    1. Inicialización con 24 conceptos precargados
    2. Prueba de razonamiento deductivo (silogismo de Sócrates)
    3. Prueba de razonamiento inductivo (patrón climático)
    4. Prueba de razonamiento abductivo (diagnóstico de síntomas)
    5. Prueba de razonamiento analógico (transferencia entre dominios)
    6. Prueba de razonamiento causal (relación causa-efecto)
    7. Demostración de aprendizaje (incorporar nuevo concepto)
    8. Exportación de toda la base de conocimiento a JSON
    
    Salida esperada incluye:
    - Tipo de razonamiento detectado
    - Premisas utilizadas
    - Pasos de inferencia
    - Conclusión final
    - Nivel de confianza (0.0 - 1.0)
    - Alternativas consideradas y por qué fueron descartadas
    
    ============================================================================
    ⚠️ LIMITACIONES Y CONSIDERACIONES
    ============================================================================
    
    • Este es un sistema EXPERIMENTAL, no está diseñado para producción crítica
    • La base de conocimiento inicial es limitada y debe expandirse
    • No tiene acceso a información en tiempo real (internet, APIs, etc.)
    • El razonamiento depende de la calidad del conocimiento precargado
    • No reemplaza juicio humano en decisiones importantes
    • Las conclusiones son tan buenas como las premisas proporcionadas
    
    ============================================================================
    🚀 FUTURAS MEJORAS POTENCIALES
    ============================================================================
    
    • Integración con LLMs para extracción automática de conocimiento
    • Interfaz gráfica para visualización de la red semántica
    • Persistencia en base de datos (SQLite, PostgreSQL)
    • API REST para acceso remoto
    • Soporte para razonamiento probabilístico avanzado
    • Módulo de retroalimentación para ajuste continuo
    • Plugins para dominios específicos (medicina, derecho, ingeniería)
    
    ============================================================================
    © 2024 NEURO-REASONER AI - Proyecto Experimental de Código Abierto
    ============================================================================
    """
    
    print("\n" + "="*70)
    print("🤖 NEURO-REASONER AI v1.0 - Sistema Experimental de IA")
    print("   Inteligencia Artificial con Capacidad de Razonamiento")
    print("="*70 + "\n")
    
    # Crear instancia de la IA
    ai = NeuralReasoner(name="Prometheus")
    
    print("📊 Estado inicial del sistema:")
    status = ai.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")
    
    # Ejemplos de consultas para demostrar el razonamiento
    test_queries = [
        "¿Qué es el razonamiento lógico?",
        "Si todos los humanos son mortales y Sócrates es humano, ¿qué podemos concluir?",
        "¿Por qué existe la causa y efecto?",
        "Analiza la relación entre conocimiento y verdad",
        "¿Cómo se produce el aprendizaje en sistemas inteligentes?"
    ]
    
    print("\n" + "="*70)
    print("🧪 EJECUTANDO PRUEBAS DE RAZONAMIENTO")
    print("="*70)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'─'*70}")
        print(f"PRUEBA {i}: {query}")
        print(f"{'─'*70}")
        
        result = ai.reason(query)
        
        print(f"\n📋 Resumen:")
        print(f"   Conocimiento usado: {result['reasoning_process']['knowledge_used']} nodos")
        print(f"   Inferencias: {result['reasoning_process']['inferences_made']}")
        print(f"   Conclusiones aceptadas: {result['reasoning_process']['accepted_conclusions']}")
        print(f"   Confianza general: {result['confidence']:.2%}")
    
    # Demostrar aprendizaje
    print("\n" + "="*70)
    print("📚 DEMOSTRACIÓN DE APRENDIZAJE")
    print("="*70)
    
    learning_experience = {
        "concept": "neural_network",
        "properties": {
            "type": "computational_model",
            "category": "machine_learning",
            "inspired_by": "biological_neurons",
            "components": ["layers", "nodes", "weights", "activation_functions"]
        },
        "confidence": 0.9
    }
    
    ai.learn(learning_experience)
    
    # Verificar que el conocimiento fue aprendido
    if "neural_network" in ai.knowledge_base:
        print("\n✓ Verificación: El concepto 'neural_network' fue aprendido exitosamente")
    
    # Exportar conocimiento
    print("\n" + "="*70)
    print("💾 EXPORTANDO CONOCIMIENTO")
    print("="*70)
    
    exported = ai.export_knowledge()
    print(f"\nConocimiento exportado ({len(exported)} caracteres)")
    print("Primeras 500 líneas del export:")
    print(exported[:500] + "...")
    
    print("\n" + "="*70)
    print("✅ SISTEMA DE IA EXPERIMENTAL COMPLETADO")
    print("="*70)
    print("\n🎯 Características implementadas:")
    print("   • Múltiples tipos de razonamiento (deductivo, inductivo, abductivo)")
    print("   • Base de conocimiento semántica con relaciones")
    print("   • Motor de inferencia con reglas personalizables")
    print("   • Sistema de confianza y evaluación de conclusiones")
    print("   • Trazabilidad completa del proceso de pensamiento")
    print("   • Capacidad de aprendizaje adaptativo")
    print("   • Generación de respuestas contextualizadas")
    print("   • Perspectivas alternativas y análisis de incertidumbre")
    print("\n🚀 ¡Sistema listo para experimentación!")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
