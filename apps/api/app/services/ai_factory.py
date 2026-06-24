from app.models import AIProvider
from app.services.gemini_service import GeminiService
from app.services.ollama_service import OllamaService


class AIFactory:
    @staticmethod
    def create(provider, settings):

        if provider == AIProvider.OLLAMA:
            return OllamaService(settings)

        return GeminiService(settings)
