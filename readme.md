# ML Image Classifier

An advanced animal image classification web application that leverages machine learning to identify various animal species from uploaded images.

## Features

- **Animal Classification**: Accurately identifies 20+ animal species including cats, dogs, butterflies, gorillas, foxes, and more
- **User-friendly Interface**: Clean Django-based web interface for easy image uploads and classification results
- **Containerized Deployment**: Docker and Docker Compose setup for reliable and consistent deployment
- **Database Integration**: Stores classification history and user data in SQLite (development) or PostgreSQL (production)

## Technology Stack

### Machine Learning
- **TensorFlow/Keras**: Core ML framework for model training and inference
- **PyTorch**: Used for advanced model architectures and transfer learning
- **scikit-learn**: For data preprocessing and model evaluation
- **Pandas & NumPy**: For data manipulation and numerical operations
- **Matplotlib**: For data visualization in training notebooks

### Backend
- **Django**: Web application framework
- **Django REST Framework**: API endpoints for classification services
- **PostgreSQL**: Production database (Docker setup)
- **SQLite**: Development database

### DevOps
- **Docker**: Application containerization
- **Docker Compose**: Multi-container orchestration
- **Gunicorn**: WSGI HTTP Server for production

## Getting Started

### With Docker
1. Clone the repository
2. Run `docker-compose up --build`
3. Access the web interface at http://localhost:8000

### Without Docker
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the Django server: `python manage.py runserver`

## Dataset

The project uses a custom dataset of animal images organized by species, with categories including:
- hippopotamus, sparrow, gorilla, cat, rhinoceros, wombat, seahorse, butterfly
- donkey, raccoon, dragonfly, crab, pig, orangutan, turtle, antelope
- dog, bee, coyote, fox, and others

## Project Status

This project is currently under active development.

## Author
Tamim Dostyar
