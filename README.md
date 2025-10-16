# X-Ray Analysis API

AI-powered X-Ray analysis system built with FastAPI and PostgreSQL. Supports multiple X-ray image uploads per patient with cloud storage using Supabase S3.

## Setup Instructions

### 1. Install Dependencies

**Option A: Using requirements.txt (Recommended)**

```bash
# Activate virtual environment
source venv/bin/activate

# Install all dependencies at once
pip install -r requirements.txt
```

**Option B: Manual installation**

```bash
# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv python-multipart boto3
```

### 2. Configure Environment

Copy `env.example` to `.env` and update with your credentials:

```bash
cp env.example .env
```

Edit `.env`:
```env
# Database Configuration
DB_USER=postgres
DB_PASS=your_postgres_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=xray_db

# Supabase S3 Configuration (for file uploads)
AWS_ACCESS_KEY_ID=your_supabase_s3_access_key
AWS_SECRET_ACCESS_KEY=your_supabase_s3_secret_key
AWS_S3_ENDPOINT=https://your-project-id.storage.supabase.co
S3_BUCKET_NAME=xray-images
AWS_REGION=us-east-1

# Debug Mode (True = upload to cloud, False = save locally)
DEBUG=True
```

**How to Get Supabase S3 Credentials:**
1. Go to **Supabase Dashboard** → **Settings** → **Storage**
2. Scroll to **S3 API Credentials**
3. Click **Regenerate** to get new credentials
4. Copy **Access Key ID**, **Secret Access Key**, and **Endpoint URL**

### 3. Create Database

```bash
createdb xray_db
```

### 4. Create Supabase Storage Bucket

1. Go to **Supabase Dashboard** → **Storage**
2. Click **New bucket**
3. Name it: `xray-images`
4. Click **Create bucket**

### 5. Run the Server

```bash
source venv/bin/activate
uvicorn main:app --reload
```

Access the API:
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## File Structure

- **main.py** - FastAPI app entry point
- **api/routes.py** - All API endpoints  
- **services/patient_service.py** - Business logic & file handling
- **db/models.py** - Database models (Patient, Xray)
- **db/schema.py** - API request/response schemas
- **db/db.py** - Database connection setup
- **uploads/** - Local X-ray images storage (development only)
- **.env** - Environment variables (git-ignored)
- **venv/** - Virtual environment

---

## Storage Configuration

The API supports **two storage modes**:

| Mode | Storage | DEBUG Value | When |
|------|---------|-------------|------|
| **Cloud** | Supabase S3 ☁️ | `DEBUG=True` | Production & Railway |
| **Local** | `/uploads` folder | `DEBUG=False` | Local development only |

**Note:** Local storage on Railway is ephemeral and files are deleted on restart. Always use `DEBUG=True` for production.

---

## API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| **GET** | `/` | API welcome message |
| **GET** | `/health` | Database health check |
| **POST** | `/api/patients` | Create new patient |
| **GET** | `/api/patients` | List all patients |
| **GET** | `/api/patients/{patient_id}` | Get patient with X-rays |
| **POST** | `/api/patients/{patient_id}/xrays` | Upload X-ray images (JPG/PNG) |
| **GET** | `/api/patients/{patient_id}/xrays` | Get all X-rays for patient |

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

### Upload X-Rays (Multiple Files)
```bash
curl -X POST "http://localhost:8000/api/patients/1/xrays" \
  -F "files=@chest.jpg" \
  -F "files=@lung.png"
```

**Response:**
```json
{
  "patient_id": 1,
  "uploaded_count": 2,
  "results": [
    {
      "id": 101,
      "filename": "chest.jpg",
      "result": "No abnormalities detected",
      "confidence": 0.95
    },
    {
      "id": 102,
      "filename": "lung.png",
      "result": "Normal",
      "confidence": 0.98
    }
  ]
}
```

### Get Patient with X-Rays
```bash
curl "http://localhost:8000/api/patients/1"
```

### Get All X-Rays for Patient
```bash
curl "http://localhost:8000/api/patients/1/xrays"
```

### Health Check
```bash
curl "http://localhost:8000/health"
```

---

## Features

- ✅ Create and manage patient records (name, DOB, gender, age)
- ✅ Upload multiple X-ray images per patient
- ✅ File validation (JPG/PNG only)
- ✅ Cloud storage with Supabase S3
- ✅ AI model integration ready
- ✅ Store results in PostgreSQL
- ✅ Interactive API documentation at `/docs`
- ✅ CORS enabled for cross-origin requests
- ✅ Error handling and validation
