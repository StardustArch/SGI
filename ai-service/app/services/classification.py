import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def classify_text(text: str) -> Dict[str, Any]:
    """
    Classifica o texto da denúncia em categorias
    """
    # Categorias pré-definidas
    categories = {
        "ASSEDIO": "Assédio Moral/Sexual",
        "DISCRIMINACAO": "Discriminação", 
        "CORRUPCAO": "Corrupção",
        "ASSEDIO_MORAL": "Assédio Moral",
        "OUTROS": "Outros"
    }
    
    # Palavras-chave para cada categoria
    keywords = {
        "ASSEDIO": ["assedio", "assédio", "sexual", "moral", "cantada", "perseguição", "assediar", "constrangimento"],
        "DISCRIMINACAO": ["discriminação", "racismo", "preconceito", "homofobia", "xenofobia", "mulher", "negro", "gay"],
        "CORRUPCAO": ["corrupção", "propina", "desvio", "superfaturamento", "fraude", "suborno", "dinheiro", "público"],
        "ASSEDIO_MORAL": ["humilhação", "assedio moral", "pressão", "assédio", "perseguição", "chefe", "chefia", "patrão"]
    }
    
    text_lower = text.lower()
    
    # Calcular scores por palavras-chave
    scores = {}
    for category, words in keywords.items():
        score = sum(1 for word in words if word in text_lower)
        scores[category] = score
    
    # Determinar categoria com maior score
    if scores:
        best_category = max(scores, key=scores.get)
        confidence = min(scores[best_category] / 5.0, 1.0)  # Normalizar para 0-1
    else:
        best_category = "OUTROS"
        confidence = 0.1
    
    # Gerar resumo automático
    words = text.split()
    summary = " ".join(words[:20]) + ("..." if len(words) > 20 else "")
    
    logger.info(f"Texto classificado como: {best_category} (confiança: {confidence:.2f})")
    
    return {
        "category": best_category,
        "confidence": confidence,
        "summary": summary
    }