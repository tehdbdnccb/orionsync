import json
from groq import Groq
from pydantic import BaseModel
from config.settings import get_settings

settings = get_settings()
client = Groq(api_key=settings.groq_api_key)

def transcribe_audio(audio_file_path: str) -> str:
    """
    Transcribes field voice notes using Groq's accelerated Whisper implementation.
    """
    try:
        with open(audio_file_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                # whisper-large-v3-turbo is highly recommended for speed and accuracy
                model="whisper-large-v3-turbo", 
                file=audio_file
            )
        return transcript.text
    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""

def generate_structured_json(prompt: str, schema_class: type[BaseModel]) -> BaseModel:
    """
    Forces the LLM to extract entities matching the provided Pydantic schema exactly
    using Groq's JSON Schema structured outputs.
    """
    completion = client.chat.completions.create(
        # Llama 3.1 70B is excellent for accurate JSON extraction 
        model="llama-3.1-70b-versatile", 
        messages=[
            {
                "role": "system", 
                "content": "You are a logistics and field operations extraction AI. Convert the user's field update into strict JSON."
            },
            {
                "role": "user", 
                "content": prompt
            }
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": schema_class.__name__,
                # Set strict to False for best-effort validation across all Groq models
                "strict": False, 
                # Dynamically generate the JSON schema from the Pydantic class
                "schema": schema_class.model_json_schema()
            }
        }
    )
    
    # Extract the raw JSON string from the response
    json_response_string = completion.choices[0].message.content
    
    # Validate and parse the returned JSON string back into a Python Pydantic object
    return schema_class.model_validate_json(json_response_string)