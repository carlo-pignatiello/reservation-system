# Reservation-system

This project represents a prototype web-server for managing a reservation system. It is necessary to follow the instructions to configure the environment and start the web-server. The core of the reservation system is represented by compliance with the ACID principles.

## Project Setup Instructions

**Prerequisites:**

* Docker
* `docker-compose`
* python3

**Steps:**

3. **Start Docker Services (Background Mode)**
   ```bash
   $ docker-compose up -d

2. **Navigate to backend**
   ```bash
   $ cd backend

3. **Create and activate Virtual Environment**
    ```bash
    $ python3 -m venv venv
    $ source venv/bin/activate

4. **Install Backend Dependencies**
    ```bash
    $ pip install -r requirements.txt

5. **Apply Alembic Migration**
    ```bash
    $ alembic upgrade head

6. **Start server with python**
    ```bash
    $ export PYTHONPATH="${PYTHONPATH}:/app"
    $ python app/main.py
    or
    $ docker-compose --profile server up --build -d
 7. **Swagger docs**
    Navigate to localhost:4557/docs

 
