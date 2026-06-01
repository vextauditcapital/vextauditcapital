import os
import google.generativeai as genai
from agents.config import settings, PROMPTS

class GeminiClient:
    def __init__(self):
        # Configure the Google Generative AI SDK
        self.api_key = os.environ.get("GEMINI_API_KEY") or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        
        # Primary model string as requested: Gemini 3.5 Flash (High)
        self.primary_model = "gemini-3.5-flash"
        # Standard robust fallback model in case of version string changes in API endpoints
        self.fallback_model = "gemini-1.5-flash"

    def generate_response(self, role: str, context: str, user_message: str) -> str:
        """
        Generates an AI response for a specific mailbox agent role.
        """
        system_prompt = PROMPTS.get(role, PROMPTS["support"])
        
        # Construct the complete instruction set
        full_prompt = (
            f"SYSTEM ROLE INSTRUCTIONS:\n{system_prompt}\n\n"
            f"TRANSACTION / THREAD CONTEXT:\n{context}\n\n"
            f"CUSTOMER EMAIL MESSAGE:\n{user_message}\n\n"
            "YOUR RESPONSIBLE RESPONSE (directly write the professional email body, no metadata, no markdown surrounding blocks like ```html):"
        )
        
        try:
            # Attempt to use the requested Gemini 3.5 Flash model
            model = genai.GenerativeModel(self.primary_model)
            response = model.generate_content(
                full_prompt,
                generation_config={"temperature": 0.2, "top_p": 0.95}
            )
            return response.text.strip()
        except Exception as e:
            # Fallback gracefully to stable production flash model to ensure 100% uptime
            try:
                model = genai.GenerativeModel(self.fallback_model)
                response = model.generate_content(
                    full_prompt,
                    generation_config={"temperature": 0.2, "top_p": 0.95}
                )
                return response.text.strip()
            except Exception as fe:
                return (
                    f"Dear Customer,\n\n"
                    f"Thank you for contacting Vext Audit Capital. We have received your query. "
                    f"Our system is currently optimizing service threads, and a specialized representative "
                    f"will follow up with you instantly.\n\n"
                    f"Best regards,\n"
                    f"Vext Audit Capital Operations"
                )

# Instantiate a single shared client
gemini_client = GeminiClient()
