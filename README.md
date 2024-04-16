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
   ```cd backend

3. **Activate Virtual Environment**
    ```source venv/bin/activate

4. **Install Backend Dependencies**
    ```pip install -r backend/requirements.txt

5. **Create Alembic Revision**
    ```alembic revision --autogenerate -m "Create schema and insert test data"

6. **Apply Alembic Migration**
    ```alembic upgrade head

7. **Start server**
    ```python app/main.py

### Troubleshooting NoModuleFindError:
```export PYTHONPATH=/path/to/your/project