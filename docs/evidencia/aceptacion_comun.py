"""Suite común posterior a ambas entregas; ejecutar en Docker --network none.

MIRA_ENFOQUE selecciona un adaptador de firma/vocabulario, nunca de lógica.
PYTHONPATH debe apuntar exclusivamente al src de la entrega evaluada.
"""
import copy
import os
from pathlib import Path
import socket

import pytest
import mira

# Procedencia obligatoria para evitar evaluar accidentalmente otro checkout.
_MODULO = Path(mira.__file__).resolve()
_SRC_ESPERADO = Path(os.environ["MIRA_SOURCE_ROOT"]).resolve()
assert _MODULO.is_relative_to(_SRC_ESPERADO), f"Módulo ajeno: {_MODULO} fuera de {_SRC_ESPERADO}"
print(f"MIRA_MODULO_VERIFICADO={_MODULO}")


MINIMOS = {"DOC_AUT": 70, "BIO_ROSTRO": 75, "CRUCE_MONTO": 60, "CRUCE_FECHA": 60}
FRAUDES = ("FRA_EDICION", "FRA_MEMORIA", "FRA_SINTETICO")
OPCIONALES = ("DOC_ARIT", "DOC_LEG", "DOC_IDIOMA", "META_FECHA", "META_DISP", "BIO_VIDA")
VOCABULARIO = {
    "fraude_activo": "FRAUDE_ACTIVO", "puntaje_bajo_R": "PUNTAJE_BAJO_R",
    "senal_faltante": "SENAL_FALTANTE", "minimo_incumplido": "MINIMO_INCUMPLIDO",
    "puntaje_desde_A": "PUNTAJE_EN_APROBACION", "puntaje_entre_R_A": "PUNTAJE_EN_REVISION",
}


def datos(puntaje=85):
    return {"organizacion": "X", "puntaje": puntaje,
            "senales": {**MINIMOS, **dict.fromkeys(FRAUDES, False)}}


def configuraciones(r=60, a=85):
    return {"X": {"id": "config-X", "version": "1", "R": r, "A": a}}


def evaluar(caso, configs=None):
    configs = configuraciones() if configs is None else configs
    originales = copy.deepcopy((caso, configs))
    enfoque = os.environ["MIRA_ENFOQUE"]
    if enfoque == "multi":
        resultado = mira.evaluar_caso(caso, configs)
    elif enfoque == "baseline":
        resultado = mira.evaluar(caso["organizacion"], caso, configs)
    else:
        raise ValueError("MIRA_ENFOQUE debe ser multi o baseline")
    assert (caso, configs) == originales, "La API modificó los argumentos"
    resultado = copy.deepcopy(resultado)
    if "decision" in resultado:
        resultado["decision"] = resultado["decision"].upper()
        if enfoque == "baseline":
            for motivo in resultado["motivos"] + [resultado["motivo_principal"]]:
                motivo["codigo"] = VOCABULARIO[motivo["codigo"]]
        assert resultado["puntaje"] == caso["puntaje"]
        assert resultado["motivo_principal"] == resultado["motivos"][0]
        assert resultado["configuracion"] == configs[caso["organizacion"]]
    return resultado


def m(codigo, senal=None):
    return {"codigo": codigo, **({"senal": senal} if senal else {})}


def error(resultado, tipo="entrada"):
    assert "decision" not in resultado
    assert "motivo_principal" not in resultado
    assert resultado["error"]["tipo"] == tipo
    assert resultado["error"]["codigo"]
    assert resultado["error"]["campo"]


@pytest.mark.parametrize("puntaje", [79, 80, 84, 85, 86])
def test_ca01(puntaje):
    out = evaluar(datos(puntaje))
    assert out["decision"] == ("REVISION_ASISTIDA" if puntaje < 85 else "APROBACION_AUTOMATICA")


def test_ca02():
    configs = configuraciones()
    configs["Y"] = {"id": "config-Y", "version": "2", "R": 60, "A": 90}
    caso = datos(87)
    assert evaluar(caso, configs)["decision"] == "APROBACION_AUTOMATICA"
    caso["organizacion"] = "Y"
    assert evaluar(caso, configs)["decision"] == "REVISION_ASISTIDA"


@pytest.mark.parametrize("puntaje", [59, 60, 61])
def test_ca03(puntaje):
    assert evaluar(datos(puntaje))["decision"] == ("ESCALAMIENTO_SUPERVISOR" if puntaje < 60 else "REVISION_ASISTIDA")


@pytest.mark.parametrize("senal,minimo", MINIMOS.items())
@pytest.mark.parametrize("delta", [-1, 0, 1])
def test_ca04(senal, minimo, delta):
    caso = datos()
    caso["senales"][senal] = minimo + delta
    out = evaluar(caso)
    assert out["decision"] == ("REVISION_ASISTIDA" if delta < 0 else "APROBACION_AUTOMATICA")
    assert out["desglose"][senal] == {"estado": "presente", "valor": minimo + delta, "minimo": minimo, "cumple": delta >= 0}
    if delta < 0:
        assert out["motivos"] == [m("MINIMO_INCUMPLIDO", senal), m("PUNTAJE_EN_APROBACION")]


@pytest.mark.parametrize("puntaje", [59, 85])
@pytest.mark.parametrize("activo", [False, True])
def test_ca05(puntaje, activo):
    caso = datos(puntaje)
    caso["senales"]["FRA_MEMORIA"] = activo
    out = evaluar(caso)
    assert out["decision"] == ("ESCALAMIENTO_SUPERVISOR" if activo or puntaje < 60 else "APROBACION_AUTOMATICA")
    if activo:
        assert out["motivo_principal"] == m("FRAUDE_ACTIVO", "FRA_MEMORIA")
    elif puntaje < 60:
        assert out["motivo_principal"] == m("PUNTAJE_BAJO_R")


def test_ca06():
    caso = datos()
    del caso["senales"]["CRUCE_FECHA"]
    out = evaluar(caso)
    assert out["decision"] == "REVISION_ASISTIDA"
    assert out["motivos"] == [m("SENAL_FALTANTE", "CRUCE_FECHA"), m("PUNTAJE_EN_APROBACION")]
    assert out["desglose"]["CRUCE_FECHA"]["estado"] == "ausente"


def test_ca07():
    caso = datos(59)
    caso["senales"].update(FRA_EDICION=True, FRA_SINTETICO=True, DOC_AUT=69)
    del caso["senales"]["BIO_ROSTRO"]
    out = evaluar(caso)
    assert out["decision"] == "ESCALAMIENTO_SUPERVISOR"
    assert out["motivos"] == [m("FRAUDE_ACTIVO", "FRA_EDICION"), m("FRAUDE_ACTIVO", "FRA_SINTETICO"), m("PUNTAJE_BAJO_R"), m("SENAL_FALTANTE", "BIO_ROSTRO"), m("MINIMO_INCUMPLIDO", "DOC_AUT")]


@pytest.mark.parametrize("par", [None, (60, 60), (85, 60), (-1, 85), (60, 101), (60.5, 85)])
def test_ca08(par):
    configs = {"Y": {"id": "Y", "version": "1", "R": 60, "A": 85}}
    if par is not None:
        configs.update(configuraciones(*par))
    error(evaluar(datos(), configs), "configuracion")


def test_ca09():
    caso = datos(90)
    caso["senales"]["DOC_AUT"] = 69
    out = evaluar(caso)
    assert out["decision"] == "REVISION_ASISTIDA"
    assert out["motivos"] == [m("MINIMO_INCUMPLIDO", "DOC_AUT"), m("PUNTAJE_EN_APROBACION")]
    assert set(out["desglose"]) == set(MINIMOS) | set(FRAUDES)
    for senal, minimo in MINIMOS.items():
        assert out["desglose"][senal]["minimo"] == minimo
        assert out["desglose"][senal]["valor"] == caso["senales"][senal]
    for senal in FRAUDES:
        assert out["desglose"][senal] == {"estado": "inactivo", "valor": False}


def test_ca10_aislamiento_os():
    assert os.environ.get("MIRA_RED_AISLADA") == "1", "Ejecutar con --network none y evidencia Docker"
    assert set(p.name for p in Path("/sys/class/net").iterdir()) == {"lo"}
    assert len(Path("/proc/net/route").read_text().strip().splitlines()) == 1
    with pytest.raises(OSError):
        with socket.create_connection(("1.1.1.1", 53), timeout=1):
            pass


@pytest.mark.parametrize("variante", ["ausente", -1, 101, 80.5, "85", "fraude", "codigo"])
def test_ca11(variante):
    caso = datos()
    if variante == "ausente":
        del caso["puntaje"]
    elif variante == "fraude":
        caso["senales"]["FRA_EDICION"] = "desconocido"
    elif variante == "codigo":
        caso["senales"]["NO_CATALOGADA"] = 80
    else:
        caso["puntaje"] = variante
    error(evaluar(caso))


@pytest.mark.parametrize("omitido", [None, *FRAUDES])
def test_ca12(omitido):
    caso = datos()
    if omitido:
        del caso["senales"][omitido]
        error(evaluar(caso))
    else:
        assert evaluar(caso)["decision"] == "APROBACION_AUTOMATICA"


@pytest.mark.parametrize("senal", MINIMOS)
def test_ca13(senal):
    caso = datos()
    caso["senales"][senal] = "no aplicable"
    error(evaluar(caso))


def test_ca14():
    out = evaluar(datos(), configuraciones())
    assert out["decision"] == "APROBACION_AUTOMATICA"
    assert out["configuracion"] == configuraciones()["X"]


@pytest.mark.parametrize("puntaje", [0, 99, 100])
def test_ca15(puntaje):
    assert evaluar(datos(puntaje), configuraciones(0, 100))["decision"] == ("APROBACION_AUTOMATICA" if puntaje == 100 else "REVISION_ASISTIDA")


@pytest.mark.parametrize("puntaje", [59, 60])
def test_ca16(puntaje):
    caso = datos(puntaje)
    caso["senales"]["DOC_AUT"] = 69
    del caso["senales"]["CRUCE_FECHA"]
    out = evaluar(caso)
    assert out["decision"] == ("ESCALAMIENTO_SUPERVISOR" if puntaje == 59 else "REVISION_ASISTIDA")
    motivos = [m("SENAL_FALTANTE", "CRUCE_FECHA"), m("MINIMO_INCUMPLIDO", "DOC_AUT")]
    assert out["motivos"] == ([m("PUNTAJE_BAJO_R")] + motivos if puntaje == 59 else motivos + [m("PUNTAJE_EN_REVISION")])


@pytest.mark.parametrize("valor", [-1, 0, 69.5, 100, 101])
def test_ca17(valor):
    caso = datos()
    caso["senales"]["DOC_AUT"] = valor
    out = evaluar(caso)
    if valor in (-1, 69.5, 101):
        error(out)
    else:
        assert out["decision"] == ("REVISION_ASISTIDA" if valor == 0 else "APROBACION_AUTOMATICA")


@pytest.mark.parametrize("senal", OPCIONALES)
@pytest.mark.parametrize("valor", [0, 100, -1, 101, 60.5, True, None])
def test_addendum_opcionales(senal, valor):
    caso = datos()
    original = evaluar(caso)
    assert senal not in original["desglose"]
    caso["senales"][senal] = valor
    out = evaluar(caso)
    if type(valor) is int and 0 <= valor <= 100:
        assert out["decision"] == original["decision"]
        assert out["motivos"] == original["motivos"]
        assert out["puntaje"] == original["puntaje"]
        assert out["desglose"][senal] == {"estado": "presente", "valor": valor}
    else:
        error(out)


@pytest.mark.parametrize("campo", ["puntaje", "R", "A", "DOC_AUT"])
@pytest.mark.parametrize("valor", [True, False, 85.0])
def test_enteros_estrictos(campo, valor):
    caso, configs = datos(), configuraciones()
    if campo in ("R", "A"):
        configs["X"][campo] = valor
    elif campo == "puntaje":
        caso[campo] = valor
    else:
        caso["senales"][campo] = valor
    error(evaluar(caso, configs), "configuracion" if campo in ("R", "A") else "entrada")
