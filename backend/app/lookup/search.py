from app.lookup.engine import RecognitionEngine
from app.lookup.providers.dvdfr import DVDfrProvider
from app.lookup.providers.bluray_com import BluRayComProvider


engine = RecognitionEngine(
    providers=[
        DVDfrProvider(),
        BluRayComProvider(),
    ]
)


async def lookup(barcode: str):
    return await engine.lookup(barcode)
