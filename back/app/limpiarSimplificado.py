import csv
from datetime import datetime
import re

# -------------------------------------------------
# 1. Clasificación por título
# -------------------------------------------------
def clasificar_por_titulo(title):
    if not title:
        return "Otros", "General", "N/A"

    up = title.upper()

    match_id = re.search(r'(\d+)', title)
    ticket_id = match_id.group(1) if match_id else "N/A"

    macro = "Otros"
    micro = "General"

    if "CDC" in up or "CONTROL DE CAMBIOS" in up:
        macro = "Control de Cambios (CDC)"
        if "BDD" in up: micro = "Base de Datos"
        elif "SEGURIDAD" in up: micro = "Seguridad"
        elif "INFRAESTRUCTURA" in up: micro = "Infraestructura"
        else: micro = "General"

    elif "PASO A PRODUCCIÓN" in up:
        macro = "Paso a Producción"
        micro = "App Terceros" if "TERCEROS" in up else "Producción"

    elif "PUBLICACIÓN" in up:
        macro = "Publicación"
        micro = "App Terceros" if "TERCEROS" in up else "Otros"

    elif "ANALISIS FUNCIONAL DEL SERVICIO" in up:
        macro = "Análisis Funcional"
        if "APLICACIONES" in up: micro = "Aplicaciones"
        else: micro = "Otros"

    elif "Solicitud de levantamiento" in up or "SOLICITUD DE LEVANTAMIENTO" in up:
        macro = "Levantamiento"
        micro = "General"

    elif "CUENTA" in up:
        macro = "Gestión de Identidades"
        if "GENÉRICA" in up: micro = "Cuenta Genérica"
        elif "SERVICIO" in up: micro = "Cuenta de Servicio"
        elif "PRIVILEGIADA" in up: micro = "Cuenta Privilegiada"
    
    elif "VPN" in up:
        macro = "Conectividad"
        micro = "VPN"   

    return macro, micro, ticket_id
 

# -------------------------------------------------
# 2. Clasificación por Source
# -------------------------------------------------
CLASIFICACION_SOURCE = {
    "Control De Cambios Infraestructura": "Infraestructura",
    "Infraestructura": "Infraestructura",
    "Producción": "Producción",
    "Registro": "Registro",
    "USFQ Path": "USFQ Path",
}

def clasificar_por_source(texto):
    if not texto:
        return ""
    t = texto.lower()
    for clave, categoria in CLASIFICACION_SOURCE.items():
        if clave.lower() in t:
            return categoria
    if "producción" in t:
        return "Producción"
    if "infraestructura" in t or "cdc" in t:
        return "Infraestructura"
    if "registro" in t:
        return "Registro"
    if "Automatización" in t:
        return "Automatización"
    return "Otro"


# -------------------------------------------------
# 2. Ver a quién se asignó
# -------------------------------------------------

def get_asignacion(texto: str) -> str:
    m = re.search (
        r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{2,})',
        texto
    )
    if m:
        return m.group(1)
    return None

# -------------------------------------------------
# 3. Parseo de fecha 
# -------------------------------------------------
# Graph usa formato ISO 8601 -> 2025-11-07T15:47:37Z
def parsear_fecha_iso(f):
    if not f:
        return None
    try:
        return datetime.fromisoformat(f.replace("Z", "+00:00"))
    except:
        return None


# -------------------------------------------------
# 4. Procesar una fila del CSV
# -------------------------------------------------
def procesar_fila(row):
    title = row.get("title", {})
    details = row.get("description", "") or ""
    #file_field = row.get("file", {})
    status = row.get("state", {})
    source = row.get("owner", {})
    create_at = row.get("createdDateTime", {})
    completedDateTime = row.get("completedDateTime", {})
    approvers = row.get("approvers", {})
    custom = row.get("responsePrompts", {})

    # Clasificaciones
    macro, micro, ticket_id = clasificar_por_titulo(title)
    area = clasificar_por_source(source)
    #area, proyecto = extraer_metadatos_detalles(details)
    asignacion = get_asignacion(details)

    clean_title = f"{macro} | {micro} #{ticket_id}"

    # Fecha
    fecha_create = parsear_fecha_iso(create_at)
    year = fecha_create.year if fecha_create else ""
    month = fecha_create.month if fecha_create else ""
    day = fecha_create.day if fecha_create else ""

    fecha_completed = parsear_fecha_iso(completedDateTime)

    return {
        "Title": title,
        "Clean Title": clean_title,
        "Ticket ID": ticket_id,
        "Details": details,
        #"File": file_field,
        "Status": status,
        "Source": source,
        "Create at": create_at,
        "Completed at": completedDateTime,
        "Year": year,
        "Month": month,
        "Day": day,
        "Sent by": asignacion,
        "Custom responses": custom,
        "Classification Title": macro,
        "Classification Title Micro": micro,
        "Classification Source": area,
    }


# -------------------------------------------------
# 5. CLEAN PRINCIPAL
# -------------------------------------------------
def clean(input_file, output_file):
    filas = []

    with open(input_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            filas.append(procesar_fila(row))

    # Escritura
    with open(output_file, "w", newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "Title", "Clean Title", "Ticket ID", "Details", "Status", "Source",
            "Create at", "Completed at", "Year", "Month", "Day",
            "Sent by", "Custom responses",
            "Classification Title", "Classification Title Micro", "Classification Source"
        ])

        writer.writeheader()
        for r in filas:
            writer.writerow(r)

    print(f"✅ Archivo generado: {output_file}")
    print(f"   Total registros procesados: {len(filas)}")

    return output_file


# -------------------------------------------------
# 6. MAIN PARA SUBPROCESS
# -------------------------------------------------
if __name__ == "__main__":
    import sys
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    clean(input_file, output_file)

    