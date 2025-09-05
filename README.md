# Create environment

1. Create a GCloud Project and enable the `Cloud Natural Language API` (you'll need to enable Billing for this).
2. Create a GCloud Service Account with enough permissions (ie. `Editor` role) and download the json credentials.
3. Create `.env` file with:
```
GOOGLE_APPLICATION_CREDENTIALS=[path to the GCloud json credential]
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

```sh
% python3 src/main.py
```