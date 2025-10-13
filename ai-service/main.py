from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from app.services.classification import classify_text
from app.services.anonymization import anonymize_text

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AI Service Moçambique - Sistema de Denúncias",
    description="Microserviço de IA com sentence-transformers para classificação de denúncias",
    version="2.0.0"
)

class AnalysisRequest(BaseModel):
    text: str
    language: str = "pt"

class AnalysisResponse(BaseModel):
    category: str
    confidence: float
    summary: str
    redacted_text: str
    analysis_details: dict = {}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "ai-service-mozambique",
        "version": "2.0.0",
        "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    }

@app.post("/analyze")
async def analyze_text(request: AnalysisRequest):
    """
    Analisa texto da denúncia usando sentence-transformers
    """
    try:
        logger.info(f"📝 Analisando texto de {len(request.text)} caracteres")
        
        # Classificar texto com sentence-transformers
        classification_result = classify_text(request.text)
        logger.info(f"✅ Classificação: {classification_result['category']} "
                   f"(confiança: {classification_result['confidence']})")
        
        # Anonimizar texto
        anonymization_result = anonymize_text(request.text)
        
        # Preparar resposta
        analysis_details = {
            "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            "all_scores": classification_result.get("all_scores", {}),
            "entities_removed": anonymization_result.get("entities_removed", [])
        }
        
        return AnalysisResponse(
            category=classification_result["category"],
            confidence=classification_result["confidence"],
            summary=classification_result["summary"],
            redacted_text=anonymization_result["redacted_text"],
            analysis_details=analysis_details
        )
        
    except Exception as e:
        logger.error(f"❌ Erro na análise: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno na análise: {str(e)}")

@app.get("/")
async def root():
    return {"message": "AI Service Moçambique - Sistema de Denúncias com Sentence Transformers"}

@app.on_event("startup")
async def startup_event():
    """Inicializar o modelo durante o startup"""
    logger.info("🚀 Iniciando AI Service Moçambique...")
    # O modelo já é carregado automaticamente quando o módulo é importado