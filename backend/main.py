from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI()

EDEN_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGQ1MjhiMWYtMzE2OC00YTlkLWJlM2UtNDVhZTc5ZTZlNWI2IiwidHlwZSI6ImFwaV90b2tlbiJ9.Nt67Clk5spKmZEIOGjTbY4F74bsQqqsBop63DnfhFSs"
EDEN_API_URL = "https://api.edenai.run/v2/text/generation"

class GenerateRequest(BaseModel):
    brand_positioning: str
    features: list
    tone: str
    length: int

    def __init__(self, **data):
        if not data.get('brand_positioning'):
            raise ValueError('Brand positioning cannot be empty')
        if not data.get('features'):
            raise ValueError('Features cannot be empty')
        if not data.get('tone'):
            raise ValueError('Tone cannot be empty')
        if data.get('length', 0) <= 0:
            raise ValueError('Length must be a positive integer')
        super().__init__(**data)

def call_eden_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {EDEN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "providers": ["openai"],
        "text": prompt,
        "temperature": 0.5,
        "max_tokens": 100
    }
    
    with httpx.Client(timeout=10.0) as client:
        try:
            response = client.post(EDEN_API_URL, headers=headers, json=data)
            response.raise_for_status()
            response_json = response.json()
            generated_text = response_json.get('openai', {}).get('generated_text', '')
            return generated_text.strip()
        except (httpx.HTTPStatusError, KeyError, IndexError) as e:
            raise HTTPException(status_code=500, detail=str(e))

REFERENCE_PROMPT = """
You are a copywriter at a marketing agency working on a brochure for a real estate developer.
Generate a narrative flow for the real estate brochure keeping in mind the brand positioning and features of the property.

<BRAND POSITIONING>
{brand_positioning}
</BRAND POSITIONING>

<FEATURES>
{features}
</FEATURES>

Keep the tone of the narrative {tone}.
Also make sure that the length of the copy is {length} sentences.
"""

@app.post("/generate")
async def generate(request: GenerateRequest):
    prompt = REFERENCE_PROMPT.format(
        brand_positioning=request.brand_positioning,
        features='\n'.join(request.features),
        tone=request.tone,
        length=request.length
    )
    try:
        generated_copy = call_eden_ai(prompt)
        return {"generated_copy": generated_copy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
