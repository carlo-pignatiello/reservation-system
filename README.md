# reservation-system

## Project Setup Instructions

**Prerequisites:**

* Docker: [Install Docker](https://docs.docker.com/engine/install/)
* `docker-compose` (install with `pip install docker-compose`)

**Steps:**

1. **Clone or Download Project**
    * (Describe how to clone or download your project, specific to your version control system)

2. **Navigate to Project Directory**
    * Open a terminal and use `cd` to navigate to the project directory.

3. **Start Docker Services (Background Mode)**

   ```bash
   docker-compose up -d```

4. **Activate Virtual Environment**
    ```source venv/bin/activate```

5. **Install Backend Dependencies**
    ```pip install -r backend/requirements.txt```

6. **Create Alembic Revision**
    ```alembic revision --autogenerate -m "Create schema and insert test data"```

7. **Apply Alembic Migration**
    ```alembic upgrade head```

### Troubleshooting NoModuleFindError:
```export PYTHONPATH=/path/to/your/project```