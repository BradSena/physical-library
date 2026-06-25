from app.lookup.engine import RecognitionEngine
from app.lookup.providers.dvdfr import DVDfrProvider


engine = RecognitionEngine(
    providers=[
        DVDfrProvider(),
    ]
)


async def lookup(barcode: str):
    return await engine.lookup(barcode)
