from docling_core.pdf import PDFReader
from rapidocr import RapidOCR
from pathlib import Path
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class OCRService:
    def __init__(self):
        self.reader = PDFReader()
        self.ocr = RapidOCR()

    async def extract_text_from_document(self, file_path: str) -> Dict[str, Any]:
        try:
            logger.info(f"Starting OCR extraction for: {file_path}")

            path = Path(file_path)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Read PDF pages
            pages = self.reader.read_pdf(file_path)

            markdown_lines = []
            page_count = len(pages)

            for page in pages:
                # Render page to image
                img = page.render()

                # OCR the image
                ocr_result, _ = self.ocr(img)

                # Extract text only
                text = " ".join([word[1] for word in ocr_result])

                # Add to markdown lines
                markdown_lines.append(text)

            # Join all pages into one markdown-like text
            markdown_text = "\n\n".join(markdown_lines)

            # Quality score logic unchanged
            quality_score = self._calculate_quality_score(markdown_text)

            return {
                "success": True,
                "raw_text": markdown_text,
                "page_count": page_count,
                "confidence": quality_score,
                "file_path": file_path
            }

        except Exception as e:
            logger.error(f"OCR extraction failed for {file_path}: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "raw_text": "",
                "confidence": 0.0,
                "file_path": file_path
            }

    def _calculate_quality_score(self, text: str) -> float:
        try:
            # Keep SAME LOGIC as your Docling version
            text_length = len(text)
            if text_length > 100:
                return 0.9
            elif text_length > 50:
                return 0.7
            else:
                return 0.5

        except Exception as e:
            logger.warning(f"Could not calculate quality score: {e}")
            return 0.8

    async def batch_extract(self, file_paths: list[str]) -> list[Dict[str, Any]]:
        results = []
        for file_path in file_paths:
            result = await self.extract_text_from_document(file_path)
            results.append(result)
        return results


ocr_service = OCRService()
