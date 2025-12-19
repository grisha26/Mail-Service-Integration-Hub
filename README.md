## Mail Service Integration Hub

This project is a mail service management system that allows working with different mail providers (Boomlify and Mail.tm) through a unified interface.

## Project Structure

- `boomlify_manager.py` - Boomlify mail service implementation
- `mail_manager.py` - Mail.tm mail service implementation
- `mail_service_API.py` - FastAPI service for working with mail accounts
- `mail_prod/` - Interfaces and implementations of mail services
- `tests/` - Tests for functionality

## Dependencies

- Python 3.7+
- requests
- fastapi
- uvicorn
- pytest

## Installation

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`

## Running

To start the API service:
```bash
python mail_service_API.py
```

By default, the service runs on port 8000.

## Usage

The API provides the following endpoints:
- `GET /get_mail` - Get a new mail address or list of active addresses
- `POST /get_messages` - Get all messages for a specified address

## Testing

To run tests:
```bash
pytest tests/
```

## Docker

To build and run the project using Docker:

1. Build the Docker image:
```bash
docker build -t mail-service .
```

2. Run the Docker container (this will start the API service):
```bash
docker run -p 8000:8000 mail-service
```

3. To run tests inside the container:
```bash
docker run mail-service pytest tests/ -v
```

## License

This project is licensed under the MIT License.
