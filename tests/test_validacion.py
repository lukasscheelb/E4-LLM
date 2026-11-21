"""Variantes derivadas de RF y del contrato técnico aprobado, sin servicios."""
from copy import deepcopy

import pytest

from mira import evaluar_caso

FRAUDES = ["FRA_EDICION", "FRA_MEMORIA", "FRA_SINTETICO"]
OBLIGATORIAS = ["DOC_AUT", "BIO_ROSTRO", "CRUCE_MONTO", "CRUCE_FECHA"]
OPCIONALES = ["DOC_ARIT", "DOC_LEG", "DOC_IDIOMA", "META_FECHA", "META_DISP", "BIO_VIDA"]


@pytest.mark.parametrize("campo", ["puntaje", "DOC_AUT", "R", "A"])
@pytest.mark.parametrize("valor", [True, False, None, "85", 85.0])
def test_enteros_estrictos(caso, configuraciones, campo, valor):
    if campo == "puntaje":
        caso[campo] = valor
    elif campo in ("R", "A"):
        configuraciones["X"][campo] = valor
    else:
        caso["senales"][campo] = valor
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["ok"] is False
    assert "decision" not in resultado


@pytest.mark.parametrize("codigo", FRAUDES)
def test_cada_fraude_activo(caso, configuraciones, codigo):
    caso["senales"][codigo] = True
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == "ESCALAMIENTO_SUPERVISOR"
    assert resultado["motivo_principal"] == {"codigo":"FRAUDE_ACTIVO","senal":codigo}


@pytest.mark.parametrize("valor", [0,1,"activo",None])
def test_fraude_booleano_estricto(caso, configuraciones, valor):
    caso["senales"]["FRA_EDICION"] = valor
    assert evaluar_caso(caso, configuraciones)["error"]["codigo"] == "VALOR_SENAL_INVALIDO"


@pytest.mark.parametrize("codigo", OBLIGATORIAS)
def test_cada_senal_omitida(caso, configuraciones, codigo):
    del caso["senales"][codigo]
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == "REVISION_ASISTIDA"
    assert resultado["motivo_principal"] == {"codigo":"SENAL_FALTANTE","senal":codigo}


def test_orden_independiente_de_insercion(caso, configuraciones):
    caso["senales"] = dict(reversed(list(caso["senales"].items())))
    caso["senales"].update(FRA_SINTETICO=True,FRA_EDICION=True)
    del caso["senales"]["DOC_AUT"]
    del caso["senales"]["BIO_ROSTRO"]
    caso["senales"].update(CRUCE_MONTO=0,CRUCE_FECHA=0)
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["motivos"] == [
        {"codigo":"FRAUDE_ACTIVO","senal":"FRA_EDICION"},
        {"codigo":"FRAUDE_ACTIVO","senal":"FRA_SINTETICO"},
        {"codigo":"SENAL_FALTANTE","senal":"BIO_ROSTRO"},
        {"codigo":"SENAL_FALTANTE","senal":"DOC_AUT"},
        {"codigo":"MINIMO_INCUMPLIDO","senal":"CRUCE_FECHA"},
        {"codigo":"MINIMO_INCUMPLIDO","senal":"CRUCE_MONTO"},
        {"codigo":"PUNTAJE_EN_APROBACION"},
    ]


@pytest.mark.parametrize("codigo", OPCIONALES)
@pytest.mark.parametrize("valor", [0,100])
def test_opcionales_no_alteran_ruta(caso, configuraciones, codigo, valor):
    base = evaluar_caso(caso, configuraciones)
    caso["senales"][codigo] = valor
    resultado = evaluar_caso(caso, configuraciones)
    for campo in ("decision","puntaje","motivos","motivo_principal"):
        assert resultado[campo] == base[campo]
    assert resultado["desglose"][codigo] == {"estado":"presente","valor":valor}


@pytest.mark.parametrize("codigo", OPCIONALES)
@pytest.mark.parametrize("valor", [-1,101,0.5,True,None,"no aplicable"])
def test_opcionales_invalidas(caso, configuraciones, codigo, valor):
    caso["senales"][codigo] = valor
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["ok"] is False
    assert "decision" not in resultado


def test_no_muta_entradas_ni_comparte_resultado(caso, configuraciones):
    antes = deepcopy((caso,configuraciones))
    resultado = evaluar_caso(caso, configuraciones)
    assert (caso,configuraciones) == antes
    resultado["configuracion"]["R"] = 0
    resultado["desglose"]["DOC_AUT"]["valor"] = 0
    resultado["motivo_principal"]["codigo"] = "ALTERADO"
    assert (caso,configuraciones) == antes
    assert resultado["motivos"][0]["codigo"] == "PUNTAJE_EN_APROBACION"
    assert evaluar_caso(caso,configuraciones)["decision"] == "APROBACION_AUTOMATICA"


@pytest.mark.parametrize("valor", [None,[],"caso",85])
def test_estructura_caso(caso, configuraciones, valor):
    assert evaluar_caso(valor,configuraciones)["error"]["tipo"] == "entrada"


@pytest.mark.parametrize("valor", [None,[],"config",85])
def test_estructura_configuraciones(caso, valor):
    assert evaluar_caso(caso,valor)["error"]["tipo"] == "configuracion"


@pytest.mark.parametrize("valor", [None,""," ",1,True,[]])
def test_organizacion_invalida(caso, configuraciones, valor):
    caso["organizacion"] = valor
    assert evaluar_caso(caso,configuraciones)["error"]["codigo"] == "ORGANIZACION_INVALIDA"


@pytest.mark.parametrize("valor", [None,[],"config"])
def test_estructura_configuracion(caso, configuraciones, valor):
    configuraciones["X"] = valor
    assert evaluar_caso(caso,configuraciones)["error"]["tipo"] == "configuracion"


@pytest.mark.parametrize("campo", ["id","version"])
@pytest.mark.parametrize("valor", [None,""," ",1])
def test_identificacion_configuracion(caso, configuraciones, campo, valor):
    configuraciones["X"][campo] = valor
    assert evaluar_caso(caso,configuraciones)["error"]["tipo"] == "configuracion"


@pytest.mark.parametrize("valor", [None,[],"senales"])
def test_estructura_senales(caso, configuraciones, valor):
    caso["senales"] = valor
    assert evaluar_caso(caso,configuraciones)["error"]["tipo"] == "entrada"


def test_codigo_no_textual(caso, configuraciones):
    caso["senales"][1] = 80
    assert evaluar_caso(caso,configuraciones)["error"]["codigo"] == "SENAL_DESCONOCIDA"


def test_error_precede_fraude_y_es_determinista(caso, configuraciones):
    caso["senales"]["FRA_EDICION"] = True
    caso["puntaje"] = -1
    del caso["senales"]["FRA_MEMORIA"]
    resultado = evaluar_caso(caso,configuraciones)
    assert resultado["error"]["codigo"] == "PUNTAJE_INVALIDO"
    assert "decision" not in resultado


def test_otra_configuracion_invalida_no_contamina(caso, configuraciones):
    configuraciones["Y"] = None
    assert evaluar_caso(caso,configuraciones)["decision"] == "APROBACION_AUTOMATICA"


def test_configuracion_sin_expediente_y_extras(caso, configuraciones):
    configuraciones["X"]["comentario"] = "ya aprobada externamente"
    assert evaluar_caso(caso,configuraciones)["ok"] is True
