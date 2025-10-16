import logging
import posixpath
from typing import Optional

import requests

log = logging.getLogger(__name__)

def get_my_profile(token: str) -> dict:
    """Obtiene el perfil del usuario asociado al token usando Microsoft Graph /me."""
    url = "https://graph.microsoft.com/v1.0/me"
    r = requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=60)
    r.raise_for_status()
    data = r.json()
    log.info("Graph /me respondió con displayName=%s", data.get("displayName"))
    return data


def upload_file_to_sharepoint(
    token: str,
    site_id: str,
    drive_id: str,
    folder_path: Optional[str],
    filename: str,
    file_bytes: bytes,
    content_type: str = "text/csv",
) -> dict:
    """
    Sube un archivo a un sitio de SharePoint usando Microsoft Graph.

    Args:
        token: token Bearer válido para Graph.
        site_id: ID del sitio (formato {hostname},{site-id},{web-id}).
        drive_id: ID de la librería/document library destino.
        folder_path: ruta relativa dentro de la librería. Si es None o vacío, se usa la raíz.
        filename: nombre con el que se guardará el archivo.
        file_bytes: contenido del archivo.
        content_type: header Content-Type a enviar.
    """
    base_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}"
    folder_path = (folder_path or "").strip("/")
    path_segments = [segment for segment in [folder_path, filename] if segment]
    item_path = posixpath.join(*path_segments) if path_segments else filename
    url = f"{base_url}/root:/{item_path}:/content"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": content_type,
    }
    response = requests.put(url, headers=headers, data=file_bytes, timeout=120)
    try:
        response.raise_for_status()
    except requests.HTTPError:
        log.error("Falló la carga a SharePoint: %s", response.text)
        raise
    resource = response.json()
    log.info(
        "Archivo cargado en SharePoint: id=%s, name=%s",
        resource.get("id"),
        resource.get("name"),
    )
    return resource
