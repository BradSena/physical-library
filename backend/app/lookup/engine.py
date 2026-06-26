import asyncio

from app.lookup.consensus import choose_best
from app.lookup.models import RecognitionProvider, SearchResult


class RecognitionEngine:
    def __init__(self, providers: list[RecognitionProvider]):
        self.providers = providers

    async def _lookup_provider(
        self,
        provider: RecognitionProvider,
        barcode: str,
    ) -> list[SearchResult]:
        try:
            return await provider.search(barcode)
        except Exception as exc:
            print(f"[RecognitionEngine] Provider {provider.name} failed: {exc}")
            return []

    async def lookup(self, barcode: str) -> dict:
        results: list[SearchResult] = []

        provider_results = await asyncio.gather(
            *[
                self._lookup_provider(provider, barcode)
                for provider in self.providers
            ]
        )

        for result_group in provider_results:
            results.extend(result_group)

        return choose_best(results)
