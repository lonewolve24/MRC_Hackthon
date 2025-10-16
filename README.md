# X-Ray Analysis API

AI-powered X-Ray analysis system built with FastAPI and PostgreSQL.

## Setup Instructions

### 1. Install Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-multipart
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your database credentials:

```bash
cp env.example .env
```

Edit `.env`:
```env
DB_USER=postgres
DB_PASS=your_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=xray_db
```

### 3. Create Database

```bash
createdb xray_db
```

### 4. Run the Server

```bash
source venv/bin/activate
uvicorn main:app --reload
```

Access the API:
- **Documentation**: http://localhost:8000/docs
- **API Base**: http://localhost:8000

---

## File Structure
MRC_Hackthon/
├── main.py (FastAPI app)
├── api/routes.py (endpoints)
├── services/patient_service.py (business logic)
├── db/models.py (database models)
├── db/schema.py (API schemas)
├── db/db.py (database setup)
├── uploads/ (X-ray images)
├── .env (environment variables)
└── venv/ (virtual environment)


---

## API Routes

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| **GET** | `/` | API welcome message | - |
| **GET** | `/health` | Database health check | - |
| **POST** | `/api/patients` | Create new patient | JSON |
| **GET** | `/api/patients` | List all patients | - |
| **GET** | `/api/patients/{patient_id}` | Get patient with X-rays | - |
| **POST** | `/api/patients/{patient_id}/xrays` | Upload X-ray images | Files (JPG/PNG) |
| **GET** | `/api/patients/{patient_id}/xrays` | Get all X-rays for patient | - |

---

## API Examples

### Create Patient
```bash
curl -X POST "http://localhost:8000/api/patients" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "date_of_birth": "1990-01-15T00:00:00",
    "gender": "male"
  }'
```

### Upload X-Rays
```bash
curl -X POST "http://localhost:8000/api/patients/1/xrays" \
  -F "files=@chest.jpg" \
  -F "files=@lung.png"
```

### Get Patient
```bash
curl "http://localhost:8000/api/patients/1"
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

---

## Features

- ✅ Create and manage patient records
- ✅ Upload multiple X-ray images (JPG/PNG only)
- ✅ AI model integration for analysis
- ✅ Store results in PostgreSQL
- ✅ Interactive API documentation at `/docs`
- ✅ CORS enabled for cross-origin requests
