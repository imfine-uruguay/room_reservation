from datetime import UTC, datetime

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"


def utc_now() -> datetime:
    return datetime.now(UTC)


def utc_timestamp(moment: datetime | None = None) -> str:
    moment = moment or utc_now()
    if moment.tzinfo is not None:
        moment = moment.astimezone(UTC)
    return moment.strftime(TIMESTAMP_FORMAT)


def utc_date() -> str:
    return utc_now().strftime(DATE_FORMAT)


def utc_to_local(moment: datetime) -> datetime:
    if moment.tzinfo is None:
        moment = moment.replace(tzinfo=UTC)
    return moment.astimezone()


def local_timestamp(value: datetime | str | None) -> str | None:
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return utc_to_local(value).strftime(TIMESTAMP_FORMAT)

    texto = str(value).strip()
    for formato in (TIMESTAMP_FORMAT, f"{TIMESTAMP_FORMAT}.%f", DATE_FORMAT):
        try:
            dt = datetime.strptime(texto, formato).replace(tzinfo=UTC)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=UTC)
            return utc_to_local(dt).strftime(TIMESTAMP_FORMAT)
        except ValueError:
            continue
    try:
        return utc_to_local(datetime.fromisoformat(texto)).strftime(TIMESTAMP_FORMAT)
    except ValueError:
        return texto


def local_timezone_label(moment: datetime | None = None) -> str:
    """Etiqueta de la zona local del sistema, p. ej. ``'-03 (UTC-03:00)'``."""
    local = (moment or utc_now()).astimezone()
    offset = local.strftime("%z")
    offset_fmt = f"UTC{offset[:3]}:{offset[3:]}" if offset else "UTC"
    nombre = local.tzname()
    return f"{nombre} ({offset_fmt})" if nombre else offset_fmt
