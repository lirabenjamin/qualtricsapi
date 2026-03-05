"""
Graphics Library Mixin
Handles uploading images to the Qualtrics Graphics Library and generating
image HTML for use in question text.
"""

import os
import requests
import tempfile
from typing import Dict, Any, Optional
from urllib.parse import urlparse


class GraphicsMixin:
    """Mixin providing graphics/image upload and management."""

    def _get_library_id(self) -> str:
        """
        Get the user's personal library ID (UR_xxxx).

        Returns:
            The library ID string
        """
        response = requests.get(
            f"{self.base_url}/whoami",
            headers=self.headers,
        )
        if response.status_code != 200:
            raise Exception(f"Failed to get user info: {response.text}")
        return response.json()["result"]["userId"]

    def upload_graphic(
        self,
        image_source: str,
        filename: Optional[str] = None,
        folder: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload an image to the Qualtrics Graphics Library.

        Accepts a local file path or a URL (the image will be downloaded first).

        Args:
            image_source: Local file path OR a public URL to an image.
                          For GitHub, use the raw URL
                          (raw.githubusercontent.com/...).
            filename: Optional display name in the library. Defaults to the
                      basename of the source path/URL.
            folder: Optional folder name inside the library.

        Returns:
            Dictionary with 'id' (graphic ID) and 'url' (Qualtrics-hosted URL).
        """
        library_id = self._get_library_id()

        # Determine if source is a URL or local path
        parsed = urlparse(image_source)
        is_url = parsed.scheme in ("http", "https")

        if is_url:
            # Download to a temp file first
            dl = requests.get(image_source, timeout=30)
            if dl.status_code != 200:
                raise Exception(
                    f"Failed to download image from {image_source}: {dl.status_code}"
                )
            if filename is None:
                filename = os.path.basename(parsed.path) or "image.png"
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(filename)[1])
            tmp.write(dl.content)
            tmp.close()
            local_path = tmp.name
        else:
            local_path = image_source
            if filename is None:
                filename = os.path.basename(local_path)

        # Guess content type
        ext = os.path.splitext(filename)[1].lower()
        content_types = {
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".svg": "image/svg+xml",
            ".webp": "image/webp",
        }
        content_type = content_types.get(ext, "image/png")

        # Upload via multipart form
        upload_headers = {"X-API-TOKEN": self.api_token}
        url = f"{self.base_url}/libraries/{library_id}/graphics"
        params = {}
        if folder:
            params["folder"] = folder

        try:
            with open(local_path, "rb") as f:
                files = {"file": (filename, f, content_type)}
                response = requests.post(
                    url, headers=upload_headers, files=files, params=params
                )
        finally:
            # Clean up temp file if we created one
            if is_url:
                os.unlink(local_path)

        if response.status_code != 200:
            raise Exception(f"Failed to upload graphic: {response.text}")

        result = response.json()["result"]
        graphic_id = result["id"]

        # Build the Qualtrics-hosted URL
        qualtrics_url = (
            f"https://{self.data_center}/ControlPanel/Graphic.php"
            f"?IM={graphic_id}"
        )

        return {"id": graphic_id, "url": qualtrics_url}

    def get_image_html(
        self,
        image_source: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        alt: str = "",
    ) -> str:
        """
        Upload an image and return an <img> HTML tag ready for QuestionText.

        This is a convenience wrapper: uploads the image, then returns
        the HTML string you can embed in any question's text.

        Args:
            image_source: Local file path or public URL to an image.
            width: Optional width in pixels.
            height: Optional height in pixels.
            alt: Alt text for accessibility.

        Returns:
            HTML string like '<img src="https://..." width="400" />'
        """
        result = self.upload_graphic(image_source)
        img_url = result["url"]

        attrs = [f'src="{img_url}"']
        if alt:
            attrs.append(f'alt="{alt}"')
        if width:
            attrs.append(f'width="{width}"')
        if height:
            attrs.append(f'height="{height}"')

        return f"<img {' '.join(attrs)} />"
