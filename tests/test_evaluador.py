"""Suite propia: cada nombre CA corresponde a historia aprobada."""
from copy import deepcopy
import pytest
from mira import evaluar
from mira.evaluador import MINIMOS, FRAUDES, OPCIONALES

AP = "aprobacion_automatica"
RE = "revision_asistida"
SU = "escalamiento_supervisor"


def datos(puntaje=85):
    return {"puntaje": puntaje, "senales": {**MINIMOS, **dict.fromkeys(FRAUDES, False)}}


def configs(r=60, a=85):
    return {"X": {"id": "config-X", "version": "v1", "R": r, "A": a}}


def resultado(caso=None, configuraciones=None, org="X"):
    return evaluar(org, datos() if caso is None else caso, configs() if configuraciones is None else configuraciones)


def error(res, tipo="entrada"):
    assert set(res) == {"error"}
    assert res["error"]["tipo"] == tipo
    assert res["error"]["codigo"]
    assert res["error"]["campo"]


@pytest.mark.parametrize("puntaje,decision", [(79,RE),(80,RE),(84,RE),(85,AP),(86,AP)])
def test_ca01(puntaje, decision):
    assert resultado(datos(puntaje))["decision"] == decision


def test_ca02():
    cs = configs()
    cs["Y"] = {"id":"config-Y", "version":"v3", "R":60, "A":90}
    for org, decision in [("X",AP),("Y",RE)]:
        res = resultado(datos(87), cs, org)
        assert res["decision"] == decision
        assert res["configuracion"] == cs[org]
        assert res["organizacion"] == org


@pytest.mark.parametrize("puntaje,decision", [(59,SU),(60,RE),(61,RE)])
def test_ca03(puntaje, decision):
    assert resultado(datos(puntaje))["decision"] == decision


@pytest.mark.parametrize("codigo,minimo", MINIMOS.items())
@pytest.mark.parametrize("delta", [-1,0,1])
def test_ca04(codigo, minimo, delta):
    caso = datos()
    caso["senales"][codigo] = minimo + delta
    res = resultado(caso)
    assert res["decision"] == (RE if delta < 0 else AP)
    assert res["desglose"][codigo] == {"estado":"presente", "valor":minimo+delta, "minimo":minimo, "cumple":delta>=0}
    if delta < 0:
        assert res["motivo_principal"] == {"codigo":"minimo_incumplido", "senal":codigo}


@pytest.mark.parametrize("puntaje", [59,85])
@pytest.mark.parametrize("activo", [True,False])
def test_ca05(puntaje, activo):
    caso = datos(puntaje)
    caso["senales"]["FRA_MEMORIA"] = activo
    res = resultado(caso)
    assert res["puntaje"] == puntaje
    assert res["decision"] == (SU if activo or puntaje < 60 else AP)
    assert res["motivo_principal"]["codigo"] == ("fraude_activo" if activo else "puntaje_bajo_R" if puntaje < 60 else "puntaje_desde_A")


def test_ca06():
    caso = datos()
    del caso["senales"]["CRUCE_FECHA"]
    res = resultado(caso)
    assert res["decision"] == RE
    assert res["motivos"] == [{"codigo":"senal_faltante", "senal":"CRUCE_FECHA"}, {"codigo":"puntaje_desde_A"}]
    assert res["desglose"]["CRUCE_FECHA"] == {"estado":"ausente", "minimo":60}


def test_ca07():
    caso = datos(59)
    caso["senales"].update(FRA_EDICION=True, FRA_SINTETICO=True, DOC_AUT=69)
    del caso["senales"]["BIO_ROSTRO"]
    res = resultado(caso)
    assert res["decision"] == SU
    assert res["motivos"] == [
        {"codigo":"fraude_activo", "senal":"FRA_EDICION"},
        {"codigo":"fraude_activo", "senal":"FRA_SINTETICO"},
        {"codigo":"puntaje_bajo_R"},
        {"codigo":"senal_faltante", "senal":"BIO_ROSTRO"},
        {"codigo":"minimo_incumplido", "senal":"DOC_AUT"}]
    assert res["motivo_principal"] == res["motivos"][0]


@pytest.mark.parametrize("par", [None,(60,60),(85,60),(-1,85),(60,101),(60.5,85)])
def test_ca08(par):
    cs = {} if par is None else configs(*par)
    cs["Y"] = {"id":"Y", "version":"1", "R":60,"A":85}
    error(resultado(configuraciones=cs), "configuracion")
    assert resultado(configuraciones=cs, org="Y")["decision"] == AP


def test_ca09():
    caso = datos(90)
    caso["senales"]["DOC_AUT"] = 69
    res = resultado(caso)
    assert res["decision"] == RE
    assert res["puntaje"] == 90
    assert res["motivo_principal"] == {"codigo":"minimo_incumplido", "senal":"DOC_AUT"}
    assert res["motivos"][-1] == {"codigo":"puntaje_desde_A"}
    assert res["configuracion"] == configs()["X"]
    assert set(res["desglose"]) == set(MINIMOS) | set(FRAUDES)


def test_ca10_ejecucion_python_local():
    # Verifica disponibilidad local; aislamiento OS/red se acredita externamente.
    assert resultado()["decision"] == AP


@pytest.mark.parametrize("valor", [None,-1,101,80.5,"85"])
def test_ca11_puntaje(valor):
    caso = datos()
    if valor is None:
        del caso["puntaje"]
    else:
        caso["puntaje"] = valor
    error(resultado(caso))


@pytest.mark.parametrize("codigo,valor", [("FRA_EDICION","desconocido"),("NO_CATALOGADA",50)])
def test_ca11_senal(codigo, valor):
    caso = datos()
    caso["senales"][codigo] = valor
    error(resultado(caso))


@pytest.mark.parametrize("codigo", FRAUDES)
def test_ca12(codigo):
    caso = datos()
    assert resultado(caso)["decision"] == AP
    del caso["senales"][codigo]
    res = resultado(caso)
    error(res)
    assert res["error"]["campo"] == codigo


@pytest.mark.parametrize("codigo", MINIMOS)
def test_ca13(codigo):
    caso = datos()
    caso["senales"][codigo] = "no aplicable"
    error(resultado(caso))


def test_ca14():
    assert resultado()["configuracion"] == configs()["X"]


@pytest.mark.parametrize("puntaje,decision", [(0,RE),(99,RE),(100,AP)])
def test_ca15(puntaje, decision):
    assert resultado(datos(puntaje), configs(0,100))["decision"] == decision


@pytest.mark.parametrize("puntaje,decision,principal", [(59,SU,"puntaje_bajo_R"),(60,RE,"senal_faltante")])
def test_ca16(puntaje, decision, principal):
    caso = datos(puntaje)
    caso["senales"]["DOC_AUT"] = 69
    del caso["senales"]["CRUCE_FECHA"]
    res = resultado(caso)
    assert res["decision"] == decision
    assert res["motivo_principal"]["codigo"] == principal
    assert {m["codigo"] for m in res["motivos"]} == {"senal_faltante", "minimo_incumplido", "puntaje_bajo_R" if puntaje < 60 else "puntaje_entre_R_A"}


@pytest.mark.parametrize("valor,decision", [(-1,None),(0,RE),(69.5,None),(100,AP),(101,None)])
def test_ca17(valor, decision):
    caso = datos()
    caso["senales"]["DOC_AUT"] = valor
    res = resultado(caso)
    if decision is None:
        error(res)
    else:
        assert res["decision"] == decision


@pytest.mark.parametrize("codigo", sorted(OPCIONALES))
@pytest.mark.parametrize("valor", [0,100,-1,101,0.5,True,None,"100"])
def test_opcionales_aclaracion(codigo, valor):
    caso = datos()
    caso["senales"][codigo] = valor
    res = resultado(caso)
    if type(valor) is int and 0 <= valor <= 100:
        assert res["decision"] == AP
        assert res["puntaje"] == 85
        assert res["motivos"] == resultado()["motivos"]
        assert res["desglose"][codigo] == {"estado":"presente", "valor":valor}
    else:
        error(res)


def test_no_mutacion_ni_aliases():
    caso, cs = datos(), configs()
    originales = deepcopy((caso,cs))
    res = resultado(caso,cs)
    assert (caso,cs) == originales
    res["configuracion"]["R"] = 0
    res["desglose"]["DOC_AUT"]["valor"] = 0
    res["motivo_principal"]["codigo"] = "otro"
    assert (caso,cs) == originales
    assert res["motivos"][0]["codigo"] == "puntaje_desde_A"


@pytest.mark.parametrize("campo,valor", [("id",None),("version",None),("id"," "),("version",1),("R",True),("A","85")])
def test_config_estructura(campo, valor):
    cs = configs()
    cs["X"][campo] = valor
    error(resultado(configuraciones=cs), "configuracion")


@pytest.mark.parametrize("caso", [None,[],{}, {"puntaje":True,"senales":{}}, {"puntaje":85,"senales":[]}])
def test_estructura_entrada(caso):
    error(evaluar("X",caso,configs()))


@pytest.mark.parametrize("codigo,valor", [("DOC_AUT",True),("FRA_EDICION",0),("FRA_MEMORIA",None)])
def test_tipos_estrictos(codigo, valor):
    caso = datos()
    caso["senales"][codigo] = valor
    error(resultado(caso))


def test_orden_lexico_y_omision_opcionales():
    caso = datos()
    caso["senales"] = dict.fromkeys(FRAUDES,False)
    res = resultado(caso)
    assert [m["senal"] for m in res["motivos"][:-1]] == sorted(MINIMOS)
    assert not (set(res["desglose"]) & OPCIONALES)
    caso["senales"].update(dict.fromkeys(MINIMOS,0))
    assert [m["senal"] for m in resultado(caso)["motivos"][:-1]] == sorted(MINIMOS)
