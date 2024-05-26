# Marketing Copy Generation Backend

This repository contains the backend code for generating marketing copy using Supabase and Eden AI.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/marketing-copy-backend.git
cd marketing-copy-backend
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables

Create a .env file in the root directory of the project and add the following environment variables:

```dotenv
SUPABASE_URL=https://your-supabase-url.supabase.co
SUPABASE_KEY=your_supabase_key_here
EDEN_API_KEY=your_eden_api_key_here
EDEN_API_URL=https://api.edenai.run/v2/text/generation
```

### 4. Run the Server

```bash
uvicorn main
--host 0.0.0.0 --port 8000
```

### Technologies Used

    FastAPI
    Supabase (Database)
    Eden AI (Text Generation API)
    Python 3.7+
    EOF
