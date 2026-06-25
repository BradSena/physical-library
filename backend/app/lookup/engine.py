from app.lookup.consensus import choose_best
from app.lookup.models import RecognitionProvider, SearchResult


class RecognitionEngine:
    def __init__(self, providers: list[RecognitionProvider]):
        self.providers = providers

    async def lookup(self, barcode: str) -> dict:
        results: list[SearchResult] = []

        for provider in self.providers:
            try:
                provider_results = await provider.search(barcode)
                results.extend(provider_results)
            except Exception as exc:
                print(f"[RecognitionEngine] Provider {provider.name} failed: {exc}")

        return choose_best(results)
