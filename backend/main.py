from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx
from supabase import create_client, Client

app = FastAPI()

EDEN_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGQ1MjhiMWYtMzE2OC00YTlkLWJlM2UtNDVhZTc5ZTZlNWI2IiwidHlwZSI6ImFwaV90b2tlbiJ9.Nt67Clk5spKmZEIOGjTbY4F74bsQqqsBop63DnfhFSs"
EDEN_API_URL = "https://api.edenai.run/v2/text/generation"
SUPABASE_URL = "https://cpghkbegmhsxejtgkjfm.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNwZ2hrYmVnbWhzeGVqdGdramZtIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTY2MzE3NzUsImV4cCI6MjAzMjIwNzc3NX0.J05h8llKZXN1EP8AFMUAJBXkRxmPyJoGv6Q2eOQtSno"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

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

class InsertData(BaseModel):
    positioning: str
    features: str
    tone: str
    length: str
    output: str

class RegenerateRequest(BaseModel):
    complete_text: str
    selected_text: str
    length_modification: str

def call_eden_ai(prompt: str) -> str:
    headers = {
        "Authorization": f"Bearer {EDEN_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "providers": ["openai"],
        "text": prompt,
        "temperature": 0.5,
        "max_tokens": 400
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
REGENERATE_PROMPT = """
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

REGENERATE_PROMPT = """
You are a copywriter. Your task is to modify ONLY the selected portion of the complete text provided below.

Here are the instructions you must follow:
1. Do not change any part of the complete text except for the selected portion.
2. Modify the selected portion as requested.
3. Replace the selected portion in the complete text with your modified version.
4. Provide the entire complete text with the modified portion included.

<COMPLETE TEXT>
{complete_text}
</COMPLETE TEXT>

<SELECTED PORTION>
{selected_text}
</SELECTED_PORTION>

The selected portion should be made {length_modification}. 

Here are the specific instructions for the modification:
- If the request is to make it "longer," expand the selected portion with more details while fitting it naturally into the complete text.
- If the request is to make it "shorter," condense the selected portion, keeping the key message but using fewer words.

Remember, your task is to regenerate the selected portion and return the entire text with this modification. Do not change any other part of the complete text.

Generate and return the complete text containing the modification, without providing any other information or sentences.
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

@app.post("/insert")
async def insert_data(data: InsertData):
    try:
        response = supabase.table('marketing_copy').insert({
            "positioning": data.positioning,
            "features": data.features,
            "tone": data.tone,
            "length": data.length,
            "output": data.output
        }).execute()
        
        if response.error:
            raise HTTPException(status_code=500, detail=response.error.message)
        
        return {"message": "Data inserted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/regenerate")
async def regenerate(data: RegenerateRequest):
    prompt = REGENERATE_PROMPT.format(
        complete_text=data.complete_text,
        selected_text=data.selected_text,
        length_modification=data.length_modification
    )
    try:
        regenerated_copy = call_eden_ai(prompt)
        return {"regenerated_copy": regenerated_copy}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)