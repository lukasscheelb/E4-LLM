"""Evaluación determinista de entradas JSON compatibles.

Contrato: evaluar(organizacion, caso, configuraciones).
caso = {"puntaje": int, "senales": {codigo: int | bool}}.
configuraciones = {organizacion: {"id": str, "version": str, "R": int, "A": int}}.
Fraudes: bool estricto (True activo, False inactivo); enteros rechazan bool.
La ausencia de las cuatro numéricas obligatorias es una alerta de negocio.
"""
from collections.abc import Mapping

MINIMOS = {"DOC_AUT": 70, "BIO_ROSTRO": 75, "CRUCE_MONTO": 60, "CRUCE_FECHA": 60}
OPCIONALES = frozenset({"DOC_ARIT", "DOC_LEG", "DOC_IDIOMA", "META_FECHA", "META_DISP", "BIO_VIDA"})
FRAUDES = ("FRA_EDICION", "FRA_MEMORIA", "FRA_SINTETICO")


def _entero(valor):
    return type(valor) is int and 0 <= valor <= 100


def _error(tipo, campo, codigo):
    return {"error": {"tipo": tipo, "campo": campo, "codigo": codigo}}


def evaluar(organizacion, caso, configuraciones):
    """Devuelve evaluación o error estructurado; nunca modifica sus argumentos.

    Configuración se valida primero. Ante varios errores se devuelve el primero:
    estructura, puntaje, señales desconocidas, fraude y numéricas (orden léxico).
    Campos adicionales de caso/configuración se ignoran; códigos de señal no.
    """
    if not isinstance(organizacion, str) or not organizacion.strip():
        return _error("entrada", "organizacion", "identificador_invalido")
    if not isinstance(configuraciones, Mapping):
        return _error("configuracion", "configuraciones", "estructura_invalida")
    config = configuraciones.get(organizacion)
    if not isinstance(config, Mapping):
        return _error("configuracion", "organizacion", "configuracion_ausente_o_invalida")
    for campo in ("id", "version"):
        if not isinstance(config.get(campo), str) or not config[campo].strip():
            return _error("configuracion", campo, "identificador_invalido")
    r, a = config.get("R"), config.get("A")
    if not _entero(r) or not _entero(a) or not r < a:
        return _error("configuracion", "umbrales", "umbrales_invalidos")
    if not isinstance(caso, Mapping):
        return _error("entrada", "caso", "estructura_invalida")
    puntaje = caso.get("puntaje")
    if not _entero(puntaje):
        return _error("entrada", "puntaje", "entero_0_100_requerido")
    senales = caso.get("senales")
    if not isinstance(senales, Mapping):
        return _error("entrada", "senales", "estructura_invalida")
    catalogo = set(MINIMOS) | OPCIONALES | set(FRAUDES)
    if any(codigo not in catalogo for codigo in senales):
        return _error("entrada", "senales", "codigo_desconocido")
    for codigo in FRAUDES:
        if codigo not in senales:
            return _error("entrada", codigo, "fraude_omitido")
        if type(senales[codigo]) is not bool:
            return _error("entrada", codigo, "booleano_requerido")
    for codigo in sorted(set(MINIMOS) | OPCIONALES):
        if codigo in senales and not _entero(senales[codigo]):
            return _error("entrada", codigo, "entero_0_100_requerido")

    motivos = []
    desglose = {}

    def motivo(codigo, senal=None):
        dato = {"codigo": codigo}
        if senal is not None:
            dato["senal"] = senal
        motivos.append(dato)

    for codigo in FRAUDES:
        desglose[codigo] = {"valor": senales[codigo], "estado": "activo" if senales[codigo] else "inactivo"}
        if senales[codigo]:
            motivo("fraude_activo", codigo)
    if puntaje < r:
        motivo("puntaje_bajo_R")
    faltantes = sorted(set(MINIMOS) - set(senales))
    bajos = sorted(c for c, minimo in MINIMOS.items() if c in senales and senales[c] < minimo)
    for codigo in faltantes:
        motivo("senal_faltante", codigo)
    for codigo in bajos:
        motivo("minimo_incumplido", codigo)
    for codigo, minimo in sorted(MINIMOS.items()):
        if codigo not in senales:
            desglose[codigo] = {"estado": "ausente", "minimo": minimo}
        else:
            desglose[codigo] = {"estado": "presente", "valor": senales[codigo], "minimo": minimo, "cumple": senales[codigo] >= minimo}
    for codigo in sorted(OPCIONALES & set(senales)):
        desglose[codigo] = {"estado": "presente", "valor": senales[codigo]}
    if puntaje >= r:
        motivo("puntaje_desde_A" if puntaje >= a else "puntaje_entre_R_A")
    if any(senales[c] for c in FRAUDES) or puntaje < r:
        decision = "escalamiento_supervisor"
    elif faltantes or bajos or puntaje < a:
        decision = "revision_asistida"
    else:
        decision = "aprobacion_automatica"
    return {
        "organizacion": organizacion,
        "decision": decision,
        "motivo_principal": dict(motivos[0]),
        "motivos": motivos,
        "puntaje": puntaje,
        "desglose": desglose,
        "configuracion": {campo: config[campo] for campo in ("id", "version", "R", "A")},
    }
