from docling_core.readers.pdf_reader import PDFReader
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

            # Read PDF pages using docling-core
            pages = self.reader.read_pdf(file_path)

            markdown_lines = []
            page_count = len(pages)

            for page in pages:
                # Render PDF page to image
                img = page.render()

                # OCR using RapidOCR
                ocr_result, _ = self.ocr(img)

                # Extract text from OCR output
                text = " ".join([item[1] for item in ocr_result])

                markdown_lines.append(text)

            # Combine all text into Markdown-like output
            markdown_text = "\n\n".join(markdown_lines)

            # Quality score logic preserved
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
            text_length = len(text)
            if text_length > 100:
                return 0.9
            elif text_length > 50:
                return 0.7
            else:
                return 0.5
        except Exception:
            return 0.8

    async def batch_extract(self, file_paths: list[str]) -> list[Dict[str, Any]]:
        return [await self.extract_text_from_document(fp) for fp in file_paths]


ocr_service = OCRService()
