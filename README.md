# reservation-system

## Project Setup Instructions

**Prerequisites:**

* Docker: [Install Docker](https://docs.docker.com/engine/install/)
* `docker-compose` (install with `pip install docker-compose`)

**Steps:**

3. **Start Docker Services (Background Mode)**
   ```bash
   docker-compose up -d

2. **Navigate to backend**
   ```bash
   cd backend

3. **Activate Virtual Environment**
    ```bash
    source venv/bin/activate

4. **Install Backend Dependencies**
    ```bash
    pip install -r backend/requirements.txt

5. **Create Alembic Revision**
    ```bash
    alembic revision --autogenerate -m "Create schema and insert test data"

6. **Apply Alembic Migration**
    ```bash
    alembic upgrade head

7. **Start server**
    ```bash
    python app/main.py

### Troubleshooting NoModuleFindError:
```export PYTHONPATH=/path/to/your/project