"""API local MIRA. No I/O, servicios ni cálculo de puntaje."""
from .evaluador import evaluar

__all__ = ["evaluar"]
