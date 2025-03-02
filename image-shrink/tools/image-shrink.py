from collections.abc import Generator
from typing import Any

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage
from dify_plugin.file.file import File, FileType

import io
from PIL import Image

class ImageShrinkTool(Tool):
    def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
        images: list[File] = tool_parameters.get("images")
        dimension: int = tool_parameters.get("dimension") or 1024
        image_type: str = tool_parameters.get("image_type") or "webp"
        mime_type = f"image/{image_type}"

        try:
            for image in images:
                if image.type != FileType.IMAGE:
                    continue

                image_binary = image.blob
                img = Image.open(io.BytesIO(image_binary))
                img.thumbnail((dimension, dimension), resample=Image.LANCZOS)
                file = io.BytesIO()
                img.save(file, format=image_type)

                yield self.create_blob_message(
                    blob=file.getvalue(),
                    meta={"mime_type": mime_type}
                )
        except Exception as e:
            raise ValueError(f"An error occurred: {str(e)}")
