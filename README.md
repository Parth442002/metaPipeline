# metaPipline
### Audio/Video Processing Pipeline

![Local Image](https://github.com/Parth442002/metaPipeline/blob/main/images/docs.png)


## Introduction💡
In this project, I employed Python with FastAPI for the backend, leveraging PostgreSQL for data storage, Docker for containerization, and AWS S3 for permanent file storage. The web service, designed for video processing, utilizes Celery for handling asynchronous large tasks and integrates a Redis database. The efficient architecture ensures concurrent request handling, making the service robust and scalable. Check out the GitHub repository for the code and detailed instructions on running the service.


## How it works
![Local Image](https://github.com/Parth442002/metaPipeline/blob/main/images/diagram.png)

This system leverages a modern tech stack to optimize file processing. The project uses FastAPI to efficiently handle incoming file requests. The use of Celery, an asynchronous task queue, allows for the parallel processing of large tasks, preventing server slowdowns. PostgreSQL, a robust relational database, manages metadata seamlessly, providing a structured and scalable solution. Docker ensures easy deployment and scalability by containerizing the application. AWS S3 serves as a reliable and scalable cloud storage solution for the final processed files, minimizing the risk of data loss. Overall, this tech stack ensures not only effective file processing but also scalability, reliability, and resource optimization.

## Performance
Our video processing service is engineered for top-notch performance and scalability, leveraging key AWS services to optimize resource usage and ensure efficient handling of multiple concurrent requests. The architecture comprises AWS RDS for storing metadata about processed videos, providing quick retrieval and management of information. Permanent file storage is handled by AWS S3, offering scalable and durable storage with easy accessibility. The FastAPI server, Celery worker, and Redis server run on AWS EC2 instances, benefiting from the flexibility and scalability of the cloud. Auto-scaling capabilities are implemented to adapt to varying workloads, optimizing resource usage and minimizing response times. Celery is employed for handling large and time-intensive tasks asynchronously, preventing server bottlenecks and enhancing overall responsiveness. Containerization with Docker ensures consistency across environments, reducing memory footprint and startup times. Memory management strategies, including regular cleanup of temporary files and efficient database connection usage, contribute to stable and consistent performance. This high-performance architecture guarantees a seamless user experience while efficiently handling diverse workloads.



## Tech Stack 🔨
1. Python
2. FastApi
3. Postgres
4. AWS S3
5. Celery
6. Redis
7. SqlAlchemy
8. Docker

![Local Image](https://github.com/Parth442002/metaPipeline/blob/main/images/postman.png)

## Project Setup
### Running Without Docker Compose

1. **Clone the project repository:**
    ```bash
    git clone https://github.com/your-username/your-project.git
    ```
2. **Navigate to the project directory:**
    ```bash
    cd your-project
    ```
3. **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
4. **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```
5. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6. **Run the FastAPI server with automatic reload:**
    ```bash
    uvicorn main:app --reload
    ```
7. **In a new terminal, run the Celery worker:**
    ```bash
    celery -A main.celery worker --loglevel=info
    ```
8. **In another terminal, start the Redis server:**
    ```bash
    redis-server
    ```
### Running With Docker Compose
1. **Build the Docker images:**
    ```bash
    docker-compose build
    ```
2. **Start the services using Docker Compose:**
    ```bash
    docker-compose up
    ```
3. **Add the necessary .env file:**
This will launch the FastAPI server, Celery worker, and Redis server in separate containers. You can access the services at the specified ports.

Note: Ensure that Docker and Docker Compose are installed on your system before running the commands.

### ⚠️ Check sample.env for refenrece.

[Api Documentation](https://documenter.getpostman.com/view/14037595/2s9YXk3LcQ) | [AWS Deployment](http://ec2-13-235-70-182.ap-south-1.compute.amazonaws.com:8000/docs)
