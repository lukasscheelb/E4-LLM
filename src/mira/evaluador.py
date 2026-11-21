"""Reglas aprobadas de MIRA E4, sin cálculo de puntaje ni servicios externos."""

_MINIMOS = {"DOC_AUT": 70, "BIO_ROSTRO": 75, "CRUCE_MONTO": 60, "CRUCE_FECHA": 60}
_OPCIONALES = frozenset({"DOC_ARIT", "DOC_LEG", "DOC_IDIOMA", "META_FECHA", "META_DISP", "BIO_VIDA"})
_FRAUDES = ("FRA_EDICION", "FRA_MEMORIA", "FRA_SINTETICO")
_NUMERICAS = frozenset(_MINIMOS) | _OPCIONALES
_CODIGOS = _NUMERICAS | frozenset(_FRAUDES)


def _error(tipo: str, codigo: str, campo: str, mensaje: str) -> dict:
    return {"ok": False, "error": {"tipo": tipo, "codigo": codigo, "campo": campo, "mensaje": mensaje}}


def _entero_en_rango(valor: object) -> bool:
    return type(valor) is int and 0 <= valor <= 100


def _texto(valor: object) -> bool:
    return isinstance(valor, str) and bool(valor.strip())


def evaluar_caso(caso: dict, configuraciones: dict) -> dict:
    """Valida y evalúa un caso sin modificarlo ni modificar configuraciones.

    Fraude se representa con bool estricto y todos sus indicadores son explícitos.
    Las señales numéricas aceptan int estricto 0..100; omitir una de las cuatro
    obligatorias es una alerta de negocio. Otros errores no producen decisión.
    """
    if not isinstance(caso, dict):
        return _error("entrada", "ESTRUCTURA_INVALIDA", "caso", "El caso debe ser un diccionario.")
    if not isinstance(configuraciones, dict):
        return _error("configuracion", "ESTRUCTURA_INVALIDA", "configuraciones", "Las configuraciones deben ser un diccionario.")
    organizacion = caso.get("organizacion")
    if not _texto(organizacion):
        return _error("entrada", "ORGANIZACION_INVALIDA", "organizacion", "La organización debe ser una cadena no vacía.")
    if organizacion not in configuraciones:
        return _error("configuracion", "CONFIGURACION_AUSENTE", "configuraciones", "No existe configuración para la organización.")
    config = configuraciones[organizacion]
    if not isinstance(config, dict):
        return _error("configuracion", "CONFIGURACION_INVALIDA", "configuracion", "La configuración debe ser un diccionario.")
    for campo in ("id", "version"):
        if not _texto(config.get(campo)):
            return _error("configuracion", "CONFIGURACION_INVALIDA", campo, "Se requiere una cadena no vacía.")
    r, a = config.get("R"), config.get("A")
    if not (_entero_en_rango(r) and _entero_en_rango(a) and r < a):
        return _error("configuracion", "UMBRALES_INVALIDOS", "umbrales", "Se requieren umbrales enteros con 0 <= R < A <= 100.")
    puntaje = caso.get("puntaje")
    if not _entero_en_rango(puntaje):
        return _error("entrada", "PUNTAJE_INVALIDO", "puntaje", "El puntaje debe ser un entero entre 0 y 100.")
    senales = caso.get("senales")
    if not isinstance(senales, dict):
        return _error("entrada", "ESTRUCTURA_INVALIDA", "senales", "Las señales deben ser un diccionario.")
    if any(not isinstance(codigo, str) for codigo in senales):
        return _error("entrada", "SENAL_DESCONOCIDA", "senales", "Los códigos de señal deben ser cadenas catalogadas.")
    for codigo in sorted(senales):
        if codigo not in _CODIGOS:
            return _error("entrada", "SENAL_DESCONOCIDA", codigo, "El código de señal no está admitido.")
        valor = senales[codigo]
        valido = type(valor) is bool if codigo in _FRAUDES else _entero_en_rango(valor)
        if not valido:
            return _error("entrada", "VALOR_SENAL_INVALIDO", codigo, "La señal requiere booleano de fraude o entero numérico entre 0 y 100, según su código.")
    for codigo in _FRAUDES:
        if codigo not in senales:
            return _error("entrada", "INDICADOR_OMITIDO", codigo, "Cada indicador de fraude debe recibirse explícitamente.")

    motivos = [{"codigo": "FRAUDE_ACTIVO", "senal": codigo} for codigo in _FRAUDES if senales[codigo]]
    if puntaje < r:
        motivos.append({"codigo": "PUNTAJE_BAJO_R"})
    faltantes = sorted(codigo for codigo in _MINIMOS if codigo not in senales)
    incumplidas = sorted(codigo for codigo, minimo in _MINIMOS.items() if codigo in senales and senales[codigo] < minimo)
    motivos.extend({"codigo": "SENAL_FALTANTE", "senal": codigo} for codigo in faltantes)
    motivos.extend({"codigo": "MINIMO_INCUMPLIDO", "senal": codigo} for codigo in incumplidas)
    if puntaje >= r:
        motivos.append({"codigo": "PUNTAJE_EN_REVISION" if puntaje < a else "PUNTAJE_EN_APROBACION"})
    if any(senales[codigo] for codigo in _FRAUDES) or puntaje < r:
        decision = "ESCALAMIENTO_SUPERVISOR"
    elif faltantes or incumplidas or puntaje < a:
        decision = "REVISION_ASISTIDA"
    else:
        decision = "APROBACION_AUTOMATICA"

    desglose = {}
    for codigo in sorted(_MINIMOS):
        presente = codigo in senales
        desglose[codigo] = {
            "estado": "presente" if presente else "ausente",
            "valor": senales.get(codigo),
            "minimo": _MINIMOS[codigo],
            "cumple": senales[codigo] >= _MINIMOS[codigo] if presente else None,
        }
    for codigo in sorted(_OPCIONALES & senales.keys()):
        desglose[codigo] = {"estado": "presente", "valor": senales[codigo]}
    for codigo in _FRAUDES:
        desglose[codigo] = {"estado": "activo" if senales[codigo] else "inactivo", "valor": senales[codigo]}
    return {
        "ok": True,
        "decision": decision,
        "motivo_principal": dict(motivos[0]),
        "motivos": motivos,
        "puntaje": puntaje,
        "desglose": desglose,
        "configuracion": {"id": config["id"], "version": config["version"], "R": r, "A": a},
    }
