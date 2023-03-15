# Challenge Surplus
Developed on Ubuntu 22.04 using Python 3.10 and FastAPI framework.

## **Installation**

### Normal Installation

To run the project, follow these steps:

1. Clone this repository:
``` bash
git clone https://github.com/codechrl/challenge-surplus.git
```
2. Install the required packages: 
``` bash
pip install -r requirements.txt
```
3. Start the app: 
``` bash
uvicorn main:app --reload
```

### Docker Installation

To run the project using Docker, follow these steps:

1. Clone this repository: 
``` bash
git clone https://github.com/codechrl/challenge-surplus.git
```

2. Build the Docker image: 
docker build -t project .

3. Run the Docker container: 
docker run -p 8000:8000 project

The above command will run the project inside a Docker container and expose it on port 8000.

## Usage

Once the app is running, you can access the Swagger UI API at `http://localhost:8000/api/docs`.

Also you can access the OpenAPI Redoc at `http://localhost:8000/api/redoc`