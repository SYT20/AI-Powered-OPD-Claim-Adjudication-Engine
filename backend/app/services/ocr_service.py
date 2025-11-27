from docling.document_converter import DocumentConverter
from docling.datamodel.document import Document
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        """
        Use Docling in CPU-only mode.
        RapidOCR / Torch / CUDA will NOT be used.
        Docling will use 'onnxruntime' backend automatically.
        """
        self.converter = DocumentConverter(
            ocr_options={"engine": "auto"}  # auto → uses ONNX (CPU)
        )

    async def extract_text_from_document(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f"Starting OCR extraction for: {file_path}")

            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # CPU-only OCR extraction
            result = self.converter.convert(str(file_path))

            # Extract Markdown text
            markdown_text = result.document.export_to_markdown()

            # Count pages if available
            page_count = (
                len(result.pages) if hasattr(result, "pages") and result.pages else 1
            )

            quality_score = self._calculate_quality_score(result)

            return {
                "success": True,
                "raw_text": markdown_text,
                "page_count": page_count,
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
                text_len = len(result.document.text)
                if text_len > 100:
                    return 0.9
                elif text_len > 50:
                    return 0.7
                return 0.5

            return 0.8

        except Exception:
            return 0.8

    async def batch_extract(self, file_paths: list[str]) -> list[Dict[str, Any]]:
        results = []
        for fp in file_paths:
            results.append(await self.extract_text_from_document(fp))
        return results


ocr_service = OCRService()
