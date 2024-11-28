# Genie AI App
It utilizes AI to provide users with the best flight and hotel options tailored to their preferences.


## Steps to Run App in VS Code
1. Create a virtual environment: `python3 -m venv ai-venv`
2. Activate the virtual environment: `source ai-venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run app locally: `fastapi dev` or `fastapi dev app/main.py`
5. Run tests: `pytest`


## Steps to Run App Using Docker
1. Set up docker and configure the path (optional): `export PATH="/Applications/Docker.app/Contents/Resources/bin:$PATH"`
2. Build docker image: `sudo docker build -t genie-ai-app .`
3. Remove existing container (if any): `docker rm genie-ai-container`
4. Run app in a container: `docker run -d --name genie-ai-container -p 5010:5010 genie-ai-app`
5. Stop container: `docker stop genie-ai-container`
6. Check running containers: `docker ps`
7. View logs for a specific process: `docker logs <process-id>`


## Run app from VS Code in debug mode
1. Click on `Run and Debug`
2. Then open `launch.json` and update with below
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "app.main:app",
                "--reload"
            ],
            "jinja": true
        }
    ]
}

## Steps to set up langfuse
1. Install the dependencies
2. Add environment variables in .env
3. Run the application
4. Check the request flow at http://172.30.20.35:3100. After signing in with your credentials under the impressico organization in the genie- project, navigate to Tracing (on the left sidebar) to view the traces.


## Environment(.env) variables
LOG_LEVEL=INFO  
INTEGRATION_BASE_URL=http://172.30.20.35:8080 #Integration micro-service base URL
OPENAI_API_KEY="open-api-key"
LANGFUSE_PUBLIC_KEY="LANGFUSE_PUBLIC_KEY"
LANGFUSE_SECRET_KEY="LANGFUSE_SECRET_KEY"
LANGFUSE_HOST = "http://172.30.20.35:3100"
ENABLED_LANGFUSE_METRICS = false  #true
LANGFUSE_USER_NAME = "your name"


## LangSmith Setup
1. Sign in to the LangSmith - https://www.langchain.com/langsmith
2. Navigate to ‘Setup Tracing’ and Generate an API key
4. Update the project name as needed
5. Copy the following details into the "Configure environment to connect to LangSmith" section:
   - `LANGCHAIN_ENDPOINT="LANGCHAIN_ENDPOINT"`
   - `LANGCHAIN_API_KEY="LANGCHAIN_API_KEY"`
   - `LANGCHAIN_PROJECT="genie-app"`
