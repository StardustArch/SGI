from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from app.services.classification import classify_text
from app.services.anonymization import anonymize_text

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Service - Sistema de Denúncias",
    description="Microserviço de IA para classificação e anonimização de denúncias",
    version="1.0.0"
)

class AnalysisRequest(BaseModel):
    text: str
    language: str = "pt"

class AnalysisResponse(BaseModel):
    category: str
    confidence: float
    summary: str
    redacted_text: str

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "ai-service",
        "version": "1.0.0"
    }

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    """
    Analisa texto da denúncia: classifica e anonimiza
    """
    try:
        logger.info(f"Analisando texto de {len(request.text)} caracteres")
        
        # Classificar texto
        classification_result = classify_text(request.text)
        
        # Anonimizar texto (remover PII)
        anonymization_result = anonymize_text(request.text)
        
        return AnalysisResponse(
            category=classification_result["category"],
            confidence=classification_result["confidence"],
            summary=classification_result["summary"],
            redacted_text=anonymization_result["redacted_text"]
        )
        
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno na análise: {str(e)}")

@app.get("/")
async def root():
    return {"message": "AI Service - Sistema de Denúncias Anônimas"}