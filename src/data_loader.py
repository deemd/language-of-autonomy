"""
Module for extracting text from PDFs of reports on AI Agentic.

This module provides functions for:
- Extracting text from PDF files
- Cleaning and normalizing extracted text
- Creating metadata for each document
- Saving results in different formats
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

import PyPDF2
import pdfplumber


class PDFTextExtractor:
    """Class to extract text from PDFs with multiple methods."""
    
    def __init__(self, raw_data_path: str = "data/raw", 
                 processed_data_path: str = "data/processed"):
        """
        Initialize the PDF text extractor.
        
        Args:
            raw_data_path: Path to the raw data directory
            processed_data_path: Path to save processed data
        """
        self.raw_path = Path(raw_data_path)
        self.processed_path = Path(processed_data_path)
        
        # Create folders if they don't exist
        self.processed_path.mkdir(parents=True, exist_ok=True)
        (self.processed_path / "texts").mkdir(exist_ok=True)
        (self.processed_path / "metadata").mkdir(exist_ok=True)
        
    def extract_with_pypdf2(self, pdf_path: Path) -> str:
        """
        Extract text with PyPDF2 (base method).
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            print(f"WARNING: Error PyPDF2 for {pdf_path.name}: {e}")
        return text
    
    def extract_with_pdfplumber(self, pdf_path: Path) -> str:
        """
        Extract text with pdfplumber (best quality).
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text
        """
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"WARNING: Error pdfplumber for {pdf_path.name}: {e}")
        return text
    
    def extract_text(self, pdf_path: Path, method: str = "pdfplumber") -> str:
        """
        Extract text from a PDF using the specified method.
        
        Args:
            pdf_path: Path to the PDF file
            method: Extraction method ("pdfplumber" or "pypdf2")
            
        Returns:
            Cleaned extracted text
        """
        if method == "pdfplumber":
            text = self.extract_with_pdfplumber(pdf_path)
            # If pdfplumber fails, try PyPDF2
            if not text.strip():
                print(f"  → Fallback to PyPDF2 for {pdf_path.name}")
                text = self.extract_with_pypdf2(pdf_path)
        else:
            text = self.extract_with_pypdf2(pdf_path)
        
        # Basic cleaning
        text = self.basic_cleaning(text)
        return text
    
    def basic_cleaning(self, text: str) -> str:
        """
        Basic text cleaning.
        
        Args:
            text: Raw text
            
        Returns:
            Cleaned text
        """
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove excessive line breaks
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', text)
        
        return text.strip()
    
    def extract_metadata(self, pdf_path: Path, text: str) -> Dict:
        """
        Extract metadata from a document.
        
        Args:
            pdf_path: Path to the PDF
            text: Extracted text
            
        Returns:
            Dictionary of metadata
        """
        metadata = {
            "filename": pdf_path.name,
            "file_size_mb": round(pdf_path.stat().st_size / (1024 * 1024), 2),
            "extraction_date": datetime.now().isoformat(),
            "char_count": len(text),
            "word_count": len(text.split()),
            "line_count": len(text.split('\n'))
        }
        
        # Try to extract metadata from the PDF
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                metadata["page_count"] = len(pdf_reader.pages)
                
                if pdf_reader.metadata:
                    pdf_meta = pdf_reader.metadata
                    metadata["title"] = pdf_meta.get('/Title', '')
                    metadata["author"] = pdf_meta.get('/Author', '')
                    metadata["subject"] = pdf_meta.get('/Subject', '')
                    metadata["creator"] = pdf_meta.get('/Creator', '')
        except Exception as e:
            print(f"WARNING: Impossible to extract PDF metadata: {e}")
            metadata["page_count"] = 0
        
        # Detect source type from filename
        filename_lower = pdf_path.name.lower()
        if any(x in filename_lower for x in ['mckinsey', 'bain', 'bcg', 'pwc', 'deloitte']):
            metadata["source_type"] = "Consulting"
        elif any(x in filename_lower for x in ['mit', 'standford', 'harvard']):
            metadata["source_type"] = "Academic"
        elif any(x in filename_lower for x in ['google', 'microsoft', 'openai']):
            metadata["source_type"] = "Industry"
        elif any(x in filename_lower for x in ['wef', 'oecd', 'undp', 'iti']):
            metadata["source_type"] = "Policy"
        else:
            metadata["source_type"] = "Unknown"
        
        return metadata
    
    def process_all_pdfs(self) -> Tuple[Dict[str, str], Dict[str, Dict]]:
        """
        Process all PDFs in the raw directory.
        
        Returns:
            Tuple of (text dictionary, metadata dictionary)
        """
        pdf_files = list(self.raw_path.glob("*.pdf"))
        
        if not pdf_files:
            print(f"ERROR: No PDF files found in {self.raw_path}")
            return {}, {}
        
        print(f"📚 {len(pdf_files)} PDF files found\n")
        
        texts = {}
        metadata_dict = {}
        
        for i, pdf_path in enumerate(pdf_files, 1):
            print(f"[{i}/{len(pdf_files)}] Processing: {pdf_path.name}")
            
            # Extract text
            text = self.extract_text(pdf_path)
            
            if not text.strip():
                print(f"WARNING: No text extracted!\n")
                continue
            
            # Create unique ID (filename without extension)
            doc_id = pdf_path.stem
            
            # Extract metadata
            metadata = self.extract_metadata(pdf_path, text)
            
            # Stocker
            texts[doc_id] = text
            metadata_dict[doc_id] = metadata
            
            print(f"  ✔ {metadata['word_count']:,} words extracted")
            print(f"  ✔ {metadata['page_count']} pages | Type: {metadata['source_type']}\n")
        
        return texts, metadata_dict
    
    def save_results(self, texts: Dict[str, str], 
                    metadata_dict: Dict[str, Dict]) -> None:
        """
        Save texts and metadata.
        
        Args:
            texts: Dictionary of extracted texts
            metadata_dict: Dictionary of metadata
        """
        # Save each text individually
        for doc_id, text in texts.items():
            text_path = self.processed_path / "texts" / f"{doc_id}.txt"
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(text)
        
        # Save all metadata in a JSON file
        metadata_path = self.processed_path / "metadata" / "corpus_metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata_dict, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Texts saved to: {self.processed_path / 'texts'}")
        print(f"💾 Metadata saved to: {metadata_path}")
    
    def generate_extraction_report(self, texts: Dict[str, str], 
                                  metadata_dict: Dict[str, Dict]) -> str:
        """
        Generate an extraction report.
        
        Args:
            texts: Dictionary of extracted texts
            metadata_dict: Dictionary of metadata
            
        Returns:
            Formatted report
        """
        total_docs = len(texts)
        total_words = sum(meta['word_count'] for meta in metadata_dict.values())
        total_pages = sum(meta['page_count'] for meta in metadata_dict.values())
        
        # Count by source type
        source_types = {}
        for meta in metadata_dict.values():
            stype = meta['source_type']
            source_types[stype] = source_types.get(stype, 0) + 1
        
        report = f"""
{'='*70}
PDF EXTRACTION REPORT
{'='*70}

GEN STATS
{'─'*70}
Number of documents processed : {total_docs}
Total words                   : {total_words:,}
Total pages                   : {total_pages}
Average words/document        : {total_words//total_docs if total_docs > 0 else 0:,}

SOURCE TYPE DISTRIBUTION
{'─'*70}
"""
        for stype, count in sorted(source_types.items()):
            report += f"{stype:20} : {count} document(s)\n"
        
        report += f"\n{'─'*70}\n"
        report += "✔ DOCUMENT DETAILS\n"
        report += f"{'─'*70}\n\n"
        
        for doc_id, meta in metadata_dict.items():
            report += f"• {meta['filename']}\n"
            report += f"  Words: {meta['word_count']:,} | "
            report += f"Pages: {meta['page_count']} | "
            report += f"Type: {meta['source_type']}\n\n"
        
        report += f"{'='*70}\n"
        
        return report


def main():
    """Main function for standalone execution."""
    print("\nBEGINNING PDF INGESTION\n")
    
    # Initialize the extractor
    extractor = PDFTextExtractor()
    
    # Process all PDFs
    texts, metadata = extractor.process_all_pdfs()
    
    if not texts:
        print("ERROR: No text extracted. Check your PDF files.")
        return
    
    # Save results
    print("\n" + "="*70)
    extractor.save_results(texts, metadata)
    
    # Generate and display report
    print("\n" + "="*70)
    report = extractor.generate_extraction_report(texts, metadata)
    print(report)
    
    # Save report
    report_path = extractor.processed_path / "extraction_report.txt"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"✔ Report saved to: {report_path}\n")


if __name__ == "__main__":
    main()