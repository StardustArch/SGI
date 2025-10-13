import re
import spacy
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

# Tentar carregar modelo do spaCy
try:
    nlp = spacy.load("pt_core_news_sm")
    logger.info("Modelo spaCy pt_core_news_sm carregado com sucesso")
except OSError:
    logger.warning("Modelo spaCy pt_core_news_sm não encontrado. Usando fallback regex.")
    nlp = None

def anonymize_text(text: str) -> Dict[str, Any]:
    """
    Anonimiza texto removendo informações pessoais (PII)
    """
    entities_removed = []
    redacted_text = text
    
    if nlp:
        # Usar spaCy para NER (Named Entity Recognition)
        doc = nlp(text)
        
        for ent in doc.ents:
            if ent.label_ in ["PER", "PERSON", "ORG", "GPE", "LOC"]:
                entities_removed.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
                # Substituir por [REDACTED]
                redacted_text = redacted_text.replace(ent.text, f"[{ent.label_}_REDACTED]")
    else:
        # Fallback: regex básico para emails e telefones
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\(\d{2}\)\s*\d{4,5}-\d{4}|\d{2}\s*\d{4,5}-\d{4}'
        
        # Encontrar e remover emails
        emails = re.findall(email_pattern, text)
        for email in emails:
            entities_removed.append({"text": email, "label": "EMAIL"})
            redacted_text = redacted_text.replace(email, "[EMAIL_REDACTED]")
        
        # Encontrar e remover telefones
        phones = re.findall(phone_pattern, text)
        for phone in phones:
            entities_removed.append({"text": phone, "label": "PHONE"})
            redacted_text = redacted_text.replace(phone, "[PHONE_REDACTED]")
    
    logger.info(f"Anonimização concluída: {len(entities_removed)} entidades removidas")
    
    return {
        "redacted_text": redacted_text,
        "entities_removed": entities_removed
    }