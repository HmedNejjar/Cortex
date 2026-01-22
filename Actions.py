from typing import List
from LLM import run, collect_stream
import json

PROMPTS_FILE = "prompts.json"

with open(PROMPTS_FILE, 'r') as f:
    prompts = json.load(f)

summary_prompt = prompts["summary_prompt"]["content"]
merge_prompt = prompts["merge_prompt"]["content"]
questions_prompt = prompts["questions_prompt"]["content"]

def summarize_chunk(text: str) -> str:
    """Summarize a single text chunk using the LLM.
    
    Args:
        text: The text chunk to summarize
        
    Returns:
        Summary text from the LLM
        
    Raises:
        ActionError: If text is empty or LLM returns empty summary
    """
    if not text.strip():
        raise ActionError("Cannot summarize empty chunk")
    
    # Send text to LLM with summary prompt
    result = run(summary_prompt, text)
    # Collect full response from streaming chunks
    chunk_summary = collect_stream(result)
    
    # Validate LLM produced non-empty output
    if not chunk_summary.strip():
        raise ActionError("Empty summary returned for chunk")
    
    # Return cleaned summary
    return chunk_summary.strip()

def merge_summaries(summaries: List[str]):
    """Merge multiple chunk summaries into a single comprehensive summary.
    
    Args:
        summaries: List of individual chunk summaries to merge
        
    Returns:
        Tuple of (streaming_response, merged_summary_text)
        
    Raises:
        ActionError: If no summaries provided or merge produces empty output
    """
    if not summaries:
        raise ActionError("No summaries provided for merging")
    
    # Combine all summaries with spacing for context
    joined = "\n\n".join(summaries)
    
    # Send combined summaries to LLM with merge prompt
    result = run(merge_prompt, joined)    
    # Return streaming response
    return result

def generate_questions(summary: str):
    """Generate questions from a summary text.
    
    Args:
        summary: The summary text to generate questions from
        
    Returns:
        Tuple of (streaming_response, questions_text)
        Questions are separated by newlines in the returned string
        
    Raises:
        ActionError: If summary is empty or question generation returns empty
    """
    if not summary.strip():
        raise ActionError("Cannot generate questions from empty summary")
    
    # Send summary to LLM with questions prompt
    result = run(questions_prompt, summary)
    # Collect full response from streaming chunks

    # Return streaming response
    return result

def print_stream(result):
    """Print streaming response chunks in real-time.
    
    Iterates through a streaming response and prints each chunk immediately
    as it arrives, providing real-time output feedback.
    
    Args:
        result: Streaming response object from ollama.chat()
    Returns:
        The complete collected text
    """
    full_text: str  = ""
    # Iterate through each chunk in the streaming response
    for chunk in result:
        # Print chunk content without newline, flush immediately for real-time display
        print(chunk["message"]["content"], end='', flush=True)
        full_text += chunk["message"]["content"]
    print()
    return full_text.strip()
    


class ActionError(Exception):
    """Exception raised for errors during action processing.
    
    This includes validation errors (empty inputs), LLM failures,
    or when expected outputs are not returned from operations.
    """
    pass