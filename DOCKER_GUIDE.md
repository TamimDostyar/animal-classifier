# Docker Guide for ML Image Classifier

## Prerequisites
- Docker
- Docker Compose

## Getting Started

1. **Build and start the containers**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - Web interface: http://localhost:8000

3. **Run migrations (first time setup)**:
   ```bash
   docker-compose exec web python manage.py migrate
   ```

4. **Create a superuser for the Django admin**:
   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

5. **Download the dataset**:
   ```bash
   docker-compose exec web python download_data.py
   ```

## Common Commands

- **Stop containers**:
  ```bash
  docker-compose down
  ```

- **View logs**:
  ```bash
  docker-compose logs -f
  ```

- **Run Django management commands**:
  ```bash
  docker-compose exec web python manage.py <command>
  ```

- **Access PostgreSQL database**:
  ```bash
  docker-compose exec db psql -U postgres -d postgres
  ```

## Notes

- The database data is persisted in a Docker volume named `postgres_data`
- Local files are mounted to the container, so changes made locally will be reflected in the container
- ML models and notebooks are accessible from within the container 