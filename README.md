# Create environment

1. Create a GCloud Project and enable the `Cloud Natural Language API` (you'll need to enable Billing for this).
2. Create a GCloud Service Account with enough permissions (ie. `Editor` role) and download the json credentials.
3. Get your GEMINI (or OPENAI) API KEY
4. Create `.env` file with:
```
GOOGLE_APPLICATION_CREDENTIALS=[path to the GCloud json credential]
LANGEXTRACT_API_KEY=[your GEMINI API KEY]
OPENAI_API_KEY=[your OPENAI API KEY]

ARANGO_HOST=[http://localhost:8529]
ARANGO_USER=[root]
ARANGO_PASSWORD=[your_password_here]
ARANGO_DB_NAME=[medical_knowledge]
```

# Create virtual environment

```sh
% python3 -m venv venv
% source venv/bin/activate
```

# Start ArangoDB

```sh
% docker-compose up -d
```

# Install dependencies

```sh
% python3 -m pip install -r requirements.txt
```

# Run the app

This example will use data from: https://huggingface.co/datasets/AGBonnet/augmented-clinical-notes
It will download it locally the first time, then use the local copy.

```sh
% python3 src/main.py [extractor] [sample index]
```

# LangExtract using OpenAI

LangExtract supports OpenAI models (requires optional dependency: `pip install "langextract[openai]"`):

```python
import langextract as lx

result = lx.extract(
    text_or_documents=input_text,
    prompt_description=prompt,
    examples=examples,
    model_id="gpt-4o",  # Automatically selects OpenAI provider
    api_key=os.environ.get('OPENAI_API_KEY'),
    fence_output=True,
    use_schema_constraints=False
```