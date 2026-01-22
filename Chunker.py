from typing import Optional, List
import math

class TextChunker:
    """Splits text into chunks with configurable size and overlap."""
    
    def __init__(self, max_chars = 4000, overlap_rate = 0.1) -> None:
        """        
        Args:
            max_chars: Maximum characters per chunk (default: 4000)
            overlap_rate: Fraction of previous chunk to include in next chunk (default: 0.1)
            
        Raises:
            ChunkingError: If overlap_rate is not between 0 and 1
        """
        if not 0 < overlap_rate < 1:
            raise ChunkingError("Overlap rate must be between 0 and 1")

        self.max_chars = max_chars
        self.overlap_chars = math.floor(max_chars * overlap_rate)
        
    def _split_paragraph(self, text: str) -> List[str]:
        """Split text into individual paragraphs.
        
        Args:
            text: Text to split
            
        Returns:
            List of paragraphs with normalized spacing
        """
        # Split text by newlines
        paragraphs = text.split("\n")

        # Remove empty paragraphs and add spacing between them
        return [p.strip() + "\n\n" for p in paragraphs if p.strip()]
    
    def _make_chunk(self, index: int, text: str) -> dict:
        """Create a chunk dictionary with metadata.
        
        Args:
            index: Chunk number/index
            text: Text content of the chunk
            
        Returns:
            Dictionary with chunk index, text, and character count
        """
        return {"chunk index": index,
                "text": text.strip(),
                "characters count": len(text)} 
     
    def chunk(self, text: str) -> Optional[List[dict]]:
        """Split text into chunks with overlapping sections.
        
        Args:
            text: Text to chunk
            
        Returns:
            List of chunk dictionaries, or None if text is empty
        """
        if not text:
            return None
        
        # Split text into paragraphs
        paragraphs = self._split_paragraph(text)
        chunks: List[dict] = []
        current_chunk, chunk_idx = "", 0
        
        # Process each paragraph
        for p in paragraphs:
            # Check if adding this paragraph would exceed max size
            if len(current_chunk) + len(p) <= self.max_chars:
                # Paragraph fits - add it to current chunk
                current_chunk += p
            else:
                # Paragraph doesn't fit - save current chunk and start a new one
                if current_chunk.strip():
                    chunks.append(self._make_chunk(chunk_idx, current_chunk))
                    chunk_idx += 1
                
                # Extract overlap from end of previous chunk for context continuity
                overlap = current_chunk[-self.overlap_chars:] if self.overlap_chars > 0 else ""
                # Start new chunk with overlap + current paragraph
                current_chunk = overlap + p
        
        # Add the final chunk if it contains content
        if current_chunk.strip():
            chunks.append(self._make_chunk(chunk_idx, current_chunk))
        
        return chunks


class ChunkingError(Exception):
    """Exception raised for errors during text chunking operations."""
    pass