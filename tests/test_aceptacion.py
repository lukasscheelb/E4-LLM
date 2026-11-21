"""Expectativas de negocio aprobadas, parametrizadas por variante de CA."""
import pytest

from mira import evaluar_caso

APROBACION = "APROBACION_AUTOMATICA"
REVISION = "REVISION_ASISTIDA"
ESCALAMIENTO = "ESCALAMIENTO_SUPERVISOR"


def comprobar_error(resultado, tipo):
    assert resultado["ok"] is False
    assert resultado["error"]["tipo"] == tipo
    assert set(resultado) == {"ok", "error"}
    assert all(resultado["error"][campo] for campo in ("codigo", "campo", "mensaje"))


@pytest.mark.parametrize("puntaje,decision", [(79,REVISION),(80,REVISION),(84,REVISION),(85,APROBACION),(86,APROBACION)], ids=["CA01-79","CA01-80","CA01-84","CA01-85","CA01-86"])
def test_ca01_banda_aprobacion(caso, configuraciones, puntaje, decision):
    caso["puntaje"] = puntaje
    assert evaluar_caso(caso, configuraciones)["decision"] == decision


def test_ca02_aislamiento(caso, configuraciones):
    configuraciones["Y"] = {"id":"config-Y","version":"2","R":60,"A":90}
    caso["puntaje"] = 87
    x = evaluar_caso(caso, configuraciones)
    caso["organizacion"] = "Y"
    y = evaluar_caso(caso, configuraciones)
    assert (x["decision"],y["decision"]) == (APROBACION,REVISION)
    assert x["configuracion"] == configuraciones["X"]
    assert y["configuracion"] == configuraciones["Y"]


@pytest.mark.parametrize("puntaje,decision", [(59,ESCALAMIENTO),(60,REVISION),(61,REVISION)], ids=["CA03-59","CA03-60","CA03-61"])
def test_ca03_frontera_revision(caso, configuraciones, puntaje, decision):
    caso["puntaje"] = puntaje
    assert evaluar_caso(caso, configuraciones)["decision"] == decision


MINIMOS = [("DOC_AUT",70),("BIO_ROSTRO",75),("CRUCE_MONTO",60),("CRUCE_FECHA",60)]
VARIANTES_MINIMOS = [(codigo,minimo,valor) for codigo,minimo in MINIMOS for valor in (minimo-1,minimo,minimo+1)]


@pytest.mark.parametrize("codigo,minimo,valor", VARIANTES_MINIMOS, ids=[f"CA04-{c}-{v}" for c,m,v in VARIANTES_MINIMOS])
def test_ca04_minimos(caso, configuraciones, codigo, minimo, valor):
    caso["senales"][codigo] = valor
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == (REVISION if valor < minimo else APROBACION)
    assert resultado["desglose"][codigo] == {"estado":"presente","valor":valor,"minimo":minimo,"cumple":valor>=minimo}
    if valor < minimo:
        assert resultado["motivo_principal"] == {"codigo":"MINIMO_INCUMPLIDO","senal":codigo}


@pytest.mark.parametrize("puntaje,activo", [(59,False),(59,True),(85,False),(85,True)], ids=["CA05-59-inactivo","CA05-59-activo","CA05-85-inactivo","CA05-85-activo"])
def test_ca05_fraude(caso, configuraciones, puntaje, activo):
    caso["puntaje"] = puntaje
    caso["senales"]["FRA_MEMORIA"] = activo
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == (ESCALAMIENTO if activo or puntaje==59 else APROBACION)
    assert resultado["puntaje"] == puntaje
    principal = {"codigo":"FRAUDE_ACTIVO","senal":"FRA_MEMORIA"} if activo else {"codigo":"PUNTAJE_BAJO_R" if puntaje==59 else "PUNTAJE_EN_APROBACION"}
    assert resultado["motivo_principal"] == principal


def test_ca06_ausencia(caso, configuraciones):
    del caso["senales"]["CRUCE_FECHA"]
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == REVISION
    assert resultado["motivos"] == [{"codigo":"SENAL_FALTANTE","senal":"CRUCE_FECHA"},{"codigo":"PUNTAJE_EN_APROBACION"}]
    assert resultado["motivo_principal"] == resultado["motivos"][0]
    assert resultado["desglose"]["CRUCE_FECHA"] == {"estado":"ausente","valor":None,"minimo":60,"cumple":None}


def test_ca07_colision(caso, configuraciones):
    caso["puntaje"] = 59
    caso["senales"].update(FRA_EDICION=True,FRA_SINTETICO=True,DOC_AUT=69)
    del caso["senales"]["BIO_ROSTRO"]
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == ESCALAMIENTO
    assert resultado["motivos"] == [
        {"codigo":"FRAUDE_ACTIVO","senal":"FRA_EDICION"},
        {"codigo":"FRAUDE_ACTIVO","senal":"FRA_SINTETICO"},
        {"codigo":"PUNTAJE_BAJO_R"},
        {"codigo":"SENAL_FALTANTE","senal":"BIO_ROSTRO"},
        {"codigo":"MINIMO_INCUMPLIDO","senal":"DOC_AUT"},
    ]
    assert resultado["motivo_principal"] == resultado["motivos"][0]


@pytest.mark.parametrize("umbrales", [None,(60,60),(85,60),(-1,85),(60,101),(60.5,85)], ids=["CA08-ausente","CA08-igual","CA08-invertida","CA08-negativo","CA08-mayor100","CA08-fraccionario"])
def test_ca08_configuracion(caso, configuraciones, umbrales):
    configuraciones["Y"] = {"id":"config-Y","version":"1","R":60,"A":85}
    if umbrales is None:
        del configuraciones["X"]
    else:
        configuraciones["X"].update(R=umbrales[0],A=umbrales[1])
    comprobar_error(evaluar_caso(caso, configuraciones), "configuracion")


def test_ca09_resultado(caso, configuraciones):
    caso["puntaje"] = 90
    caso["senales"]["DOC_AUT"] = 69
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["ok"] is True
    assert resultado["decision"] == REVISION
    assert resultado["puntaje"] == 90
    assert resultado["configuracion"] == configuraciones["X"]
    assert resultado["motivos"] == [{"codigo":"MINIMO_INCUMPLIDO","senal":"DOC_AUT"},{"codigo":"PUNTAJE_EN_APROBACION"}]
    assert resultado["motivo_principal"] == resultado["motivos"][0]
    assert set(resultado["desglose"]) == set(caso["senales"])
    assert resultado["desglose"]["DOC_AUT"] == {"estado":"presente","valor":69,"minimo":70,"cumple":False}
    for codigo,minimo in MINIMOS[1:]:
        assert resultado["desglose"][codigo] == {"estado":"presente","valor":minimo,"minimo":minimo,"cumple":True}
    for codigo in ("FRA_EDICION","FRA_MEMORIA","FRA_SINTETICO"):
        assert resultado["desglose"][codigo] == {"estado":"inactivo","valor":False}


# CA-10 es evidencia de entorno/suite, no una prueba unitaria que simule aislamiento OS.
@pytest.mark.parametrize("variante", ["ausente",-1,101,80.5,"85","fraude","desconocida"], ids=["CA11-ausente","CA11-negativo","CA11-mayor100","CA11-fraccionario","CA11-texto","CA11-fraude-invalido","CA11-desconocida"])
def test_ca11_entrada(caso, configuraciones, variante):
    if variante == "ausente":
        del caso["puntaje"]
    elif variante == "fraude":
        caso["senales"]["FRA_EDICION"] = "desconocido"
    elif variante == "desconocida":
        caso["senales"]["NO_CATALOGADA"] = 80
    else:
        caso["puntaje"] = variante
    comprobar_error(evaluar_caso(caso, configuraciones), "entrada")


@pytest.mark.parametrize("omitir", [None,"FRA_EDICION","FRA_MEMORIA","FRA_SINTETICO"], ids=["CA12-completo","CA12-edicion","CA12-memoria","CA12-sintetico"])
def test_ca12_indicadores(caso, configuraciones, omitir):
    if omitir:
        del caso["senales"][omitir]
        comprobar_error(evaluar_caso(caso, configuraciones),"entrada")
    else:
        assert evaluar_caso(caso, configuraciones)["decision"] == APROBACION


@pytest.mark.parametrize("codigo", ["DOC_AUT","BIO_ROSTRO","CRUCE_MONTO","CRUCE_FECHA"], ids=lambda c:f"CA13-{c}")
def test_ca13_no_aplicable(caso, configuraciones, codigo):
    caso["senales"][codigo] = "no aplicable"
    comprobar_error(evaluar_caso(caso, configuraciones),"entrada")


def test_ca14_sin_expediente(caso, configuraciones):
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == APROBACION
    assert resultado["configuracion"] == {"id":"config-X","version":"1","R":60,"A":85}


@pytest.mark.parametrize("puntaje,decision", [(0,REVISION),(99,REVISION),(100,APROBACION)], ids=["CA15-0","CA15-99","CA15-100"])
def test_ca15_extremos(caso, configuraciones, puntaje, decision):
    configuraciones["X"].update(R=0,A=100)
    caso["puntaje"] = puntaje
    assert evaluar_caso(caso, configuraciones)["decision"] == decision


@pytest.mark.parametrize("puntaje", [59,60], ids=["CA16-59","CA16-60"])
def test_ca16_colision_sin_fraude(caso, configuraciones, puntaje):
    caso["puntaje"] = puntaje
    caso["senales"]["DOC_AUT"] = 69
    del caso["senales"]["CRUCE_FECHA"]
    resultado = evaluar_caso(caso, configuraciones)
    assert resultado["decision"] == (ESCALAMIENTO if puntaje==59 else REVISION)
    alertas = [{"codigo":"SENAL_FALTANTE","senal":"CRUCE_FECHA"},{"codigo":"MINIMO_INCUMPLIDO","senal":"DOC_AUT"}]
    esperados = [{"codigo":"PUNTAJE_BAJO_R"}]+alertas if puntaje==59 else alertas+[{"codigo":"PUNTAJE_EN_REVISION"}]
    assert resultado["motivos"] == esperados
    assert resultado["motivo_principal"] == esperados[0]


@pytest.mark.parametrize("valor,decision", [(-1,None),(0,REVISION),(69.5,None),(100,APROBACION),(101,None)], ids=["CA17-negativo","CA17-0","CA17-fraccionario","CA17-100","CA17-mayor100"])
def test_ca17_dominio_senal(caso, configuraciones, valor, decision):
    caso["senales"]["DOC_AUT"] = valor
    resultado = evaluar_caso(caso, configuraciones)
    if decision is None:
        comprobar_error(resultado,"entrada")
    else:
        assert resultado["decision"] == decision
