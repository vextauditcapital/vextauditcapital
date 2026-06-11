import os
import logging
from anthropic import Anthropic
from agents.config import settings

logger = logging.getLogger("VextClaudeGatekeeper")

class ClaudeClient:
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        if not self.api_key or self.api_key == "DUMMY_CLAUDE_API_KEY":
            logger.warning("CLAUDE_API_KEY is not configured or using dummy fallback.")
            self.client = None
        else:
            self.client = Anthropic(api_key=self.api_key)
            
        # Hardcoding the requested Fable API model logic
        # In a real environment, you use the exact model string provided by Anthropic docs
        self.model = "claude-fable-5"

    def analyze_statutory_compliance(self, context_data: str, compliance_framework: str) -> str:
        """
        Acts as the Chief Compliance Officer. Takes massive raw data extracted by Antigravity,
        and runs strict statutory reasoning and zero-hallucination checks against it.
        Returns a deterministic JSON payload.
        """
        if not self.client:
            return '{"status": "error", "message": "Claude API key missing"}'

        system_prompt = (
            f"You are the Chief Compliance Officer and Gatekeeper for VextAudit.com.\n"
            f"Your job is to take raw financial ledger data and execute strict statutory reasoning based on the {compliance_framework}.\n"
            f"You must exhibit Zero-Hallucination Guardrails. If data is missing to verify a law, flag it as 'FAILED_MISSING_DATA'.\n"
            f"You MUST output your final analysis ONLY as a valid, parsable JSON object with no markdown wrapping and no other text."
        )

        user_prompt = f"Analyze the following extracted data and return the deterministic JSON audit matrix:\n\n{context_data}"

        try:
            logger.info(f"Dispatching payload to Claude API ({self.model}) for strict statutory review...")
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            for block in response.content:
                if getattr(block, 'type', '') == 'text':
                    return block.text
                elif type(block).__name__ == 'TextBlock':
                    return block.text
            return '{"status": "error", "message": "No text block found in Claude response"}'
        except Exception as e:
            logger.error(f"Claude API execution failed: {e}")
            return '{"status": "error", "message": "Claude API failure"}'

claude_client = ClaudeClient()
