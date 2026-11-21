import pytest


@pytest.fixture
def caso():
    return {"organizacion": "X", "puntaje": 85, "senales": {
        "DOC_AUT": 70, "BIO_ROSTRO": 75, "CRUCE_MONTO": 60, "CRUCE_FECHA": 60,
        "FRA_EDICION": False, "FRA_MEMORIA": False, "FRA_SINTETICO": False,
    }}


@pytest.fixture
def configuraciones():
    return {"X": {"id": "config-X", "version": "1", "R": 60, "A": 85}}
