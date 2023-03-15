# **Challenge Surplus**

Developed on Ubuntu 22.04 using Python 3.10 and FastAPI framework.

## **Installation**

To run the project, follow these steps:

1. Clone this repository:
``` bash
git clone https://github.com/codechrl/challenge-surplus.git
```
2. Navigate to directory and store the .env file
``` bash
cd challenge-surplus
```

3. Install the required packages: 
``` bash
pip install -r requirements.txt
```

4. Start the app: 
``` bash
uvicorn main:app --reload
```

### **Docker Installation**

To run the project using Docker, follow these steps:

1. Clone this repository: 
``` bash
git clone https://github.com/codechrl/challenge-surplus.git
```

2. Navigate to directory and store the .env file
``` bash
cd challenge-surplus
```

3. Build the Docker image: 
``` bash
docker build -t challenge-surplus .
```

4. Run the Docker container: 
``` bash
docker run -p 8000:80 challenge-surplus
```

The above command will run the project inside a Docker container and expose it on port 8000.

## **Usage**

Once the app is running, you can access the Swagger UI API at **`http://localhost:8000/api/docs`**.

Also you can access the OpenAPI Redoc at **`http://localhost:8000/api/redoc`**.