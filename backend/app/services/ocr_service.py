import os
import logging
from pathlib import Path
from typing import Dict, Any

try:
    import onnxruntime  # If installed, great
except ImportError:
    import types
    fake_ort = types.ModuleType("onnxruntime")

    class FakeSession:
        def __init__(self, *args, **kwargs):
            pass

        def run(self, *args, **kwargs):
            return []

    fake_ort.InferenceSession = FakeSession
    import sys

    sys.modules["onnxruntime"] = fake_ort

os.environ["DOCLING_OCR_ENGINE"] = "rapidocr"

from docling.document_converter import DocumentConverter

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        # Default Docling pipeline, now forced to enable RapidOCR
        self.converter = DocumentConverter()

    async def extract_text_from_document(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f"Starting OCR extraction for: {file_path}")

            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Run Docling OCR
            result = self.converter.convert(file_path)

            # Markdown output (same logic as before)
            markdown_text = result.document.export_to_markdown()

            quality_score = self._calculate_quality_score(result)

            return {
                "success": True,
                "raw_text": markdown_text,
                "page_count": len(result.pages) if hasattr(result, "pages") else 1,
                "confidence": quality_score,
                "file_path": file_path,
            }

        except Exception as e:
            logger.error(f"OCR extraction failed for {file_path}: {str(e)}")

            return {
                "success": False,
                "error": str(e),
                "raw_text": "",
                "confidence": 0.0,
                "file_path": file_path,
            }

    def _calculate_quality_score(self, result) -> float:
        try:
            if hasattr(result, "quality_score"):
                return result.quality_score

            if hasattr(result, "document") and hasattr(result.document, "text"):
                text_length = len(result.document.text)
                if text_length > 100:
                    return 0.9
                elif text_length > 50:
                    return 0.7
                else:
                    return 0.5

            return 0.8

        except Exception:
            return 0.8

    async def batch_extract(self, file_paths: list[str]) -> list[Dict[str, Any]]:
        results = []
        for file_path in file_paths:
            results.append(await self.extract_text_from_document(file_path))
        return results


ocr_service = OCRService()
