# OPD Claim Adjudication System

> AI-powered automated insurance claim processing system for Outpatient Department (OPD) claims

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.0%2B-61DAFB)](https://reactjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14%2B-336791)](https://www.postgresql.org/)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)

## 🎯 Overview

This system automates the adjudication (approval/rejection) of OPD insurance claims using AI and rule-based validation. It processes medical documents (prescriptions, bills, lab reports), extracts data using OCR and LLM, validates against policy terms, and makes intelligent approval decisions.

### Key Capabilities

- **Document Processing**: OCR extraction using Docling
- **AI Data Extraction**: Structured data extraction using Google Gemini with few-shot prompting
- **Rule Engine**: 5 sequential validation checks (eligibility, documents, coverage, limits, medical necessity)
- **Fraud Detection**: Pattern analysis for suspicious claims
- **Decision Engine**: Automated approval/rejection with confidence scoring

## ✨ Features

### Core Features
- ✅ Multi-document upload (prescription, bill, lab reports)
- ✅ Automated OCR text extraction
- ✅ AI-powered structured data extraction
- ✅ Sequential rule-based validation
- ✅ Medical necessity verification using LLM
- ✅ Fraud pattern detection
- ✅ Confidence-based manual review escalation
- ✅ Copay and network discount calculation
- ✅ Complete audit trail

### Decision Types
- **APPROVED**: All validations passed, amount calculated with deductions
- **REJECTED**: Hard validation failures (eligibility, coverage, limits)
- **PARTIAL**: Approved with capping due to sub-limits or annual limits
- **MANUAL_REVIEW**: High-value claims, low confidence, or fraud indicators

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL 14+ with SQLAlchemy ORM
- **OCR**: Docling
- **LLM**: Google Gemini (gemini-1.5-flash)
- **Validation**: Pydantic
- **CORS**: FastAPI CORS Middleware

### Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: CSS3 with custom design system
- **HTTP Client**: Axios

### Database Schema
- `members` - Member/policyholder information
- `claims` - Claim records with status
- `documents` - Uploaded documents with OCR data
- `decisions` - Adjudication decisions with reasoning
- `audit_logs` - Complete audit trail

## 🏗 Architecture

The system follows a layered architecture with clear separation of concerns:

![Architecture Diagram](Pipline.png)

For detailed flow diagrams, see [OPD_CLAIM_FLOW_DIAGRAMS.md](./OPD_CLAIM_FLOW_DIAGRAMS.md)

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or higher**
- **PostgreSQL 14 or higher**
- **Node.js 18+ and npm** (for frontend)
- **Git**
- **Google Gemini API Key**

### System Requirements
- OS: Windows 10+, macOS 10.15+, or Linux
- RAM: 4GB minimum, 8GB recommended
- Disk Space: 2GB minimum

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Plum2
```

### 2. Backend Setup

#### Create Virtual Environment

```bash
cd backend
python -m venv venv
```

#### Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

#### Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

#### Create PostgreSQL Database

```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE plum_opd;

# Exit
\q
```

#### Initialize Database Schema

```bash
python setup.py
```

This will:
- Create all required tables
- Seed 10 test members (EMP001-EMP010)
- Load policy terms configuration

### 4. Frontend Setup

```bash
cd ../frontend
npm install
```

## ⚙️ Configuration

### Backend Configuration

Create a `.env` file in the `backend` directory:

```env
# Database
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/name_of_Database

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

# Application
PROJECT_NAME="Plum OPD Adjudication API"
VERSION="1.0.0"
API_V1_PREFIX="/api/v1"

# Server
HOST=0.0.0.0
PORT=8000
```

### Frontend Configuration

Create a `.env` file in the `frontend` directory:

```env
VITE_API_BASE_URL=http://localhost:8000
```

### Getting Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key to your `.env` file

## 🎮 Running the Application

### Start Backend Server

```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

python run.py
```

Backend will start at: `http://localhost:8000`

API Documentation: `http://localhost:8000/docs`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

Frontend will start at: `http://localhost:5173`

### Access the Application

1. Open your browser
2. Navigate to `http://localhost:5173`
3. Submit a claim with test documents
4. View results and decision details

## 📚 API Documentation

### Interactive API Docs

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Claims

```
POST   /api/v1/claims                    # Submit new claim
GET    /api/v1/claims/{claim_id}         # Get claim details
GET    /api/v1/claims                    # List all claims
GET    /api/v1/decisions/{claim_id}      # Get decision details
GET    /api/v1/claims/{claim_id}/documents  # Get claim documents
```

#### Members

```
GET    /api/v1/members                   # List all members
GET    /api/v1/members/{member_id}       # Get member details
POST   /api/v1/members                   # Create new member
```

#### Health Check

```
GET    /                                  # API info
GET    /health                            # Health check
```

### Example: Submit Claim

```bash
curl -X POST "http://localhost:8000/api/v1/claims" \
  -H "Content-Type: multipart/form-data" \
  -F "member_id=EMP001" \
  -F "treatment_date=2024-11-20T10:30:00Z" \
  -F "files=@prescription.jpg" \
  -F "files=@bill.pdf"
```

## 📁 Project Structure

```
Plum2/
├── backend/
│   ├── app/
│   │   ├── config/
│   │   │   ├── settings.py           # App configuration
│   │   │   └── policy_terms.json     # Policy rules
│   │   ├── models/
│   │   │   ├── database.py           # DB connection
│   │   │   ├── db_models.py          # SQLAlchemy models
│   │   │   └── schemas.py            # Pydantic schemas
│   │   ├── routers/
│   │   │   ├── claims.py             # Claim endpoints
│   │   │   └── members.py            # Member endpoints
│   │   ├── services/
│   │   │   ├── ocr_service.py        # Docling OCR
│   │   │   ├── llm_service.py        # Gemini LLM
│   │   │   ├── rule_engine.py        # Validation logic
│   │   │   ├── decision_engine.py    # Decision logic
│   │   │   └── storage_service.py    # File handling
│   │   └── utils/
│   │       ├── db_init.py            # DB initialization
│   │       └── helpers.py            # Utility functions
│   ├── uploads/                       # Uploaded documents
│   ├── requirements.txt               # Python dependencies
│   ├── setup.py                       # Database setup
│   └── run.py                         # Development server
├── frontend/
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── services/                 # API services
│   │   ├── App.tsx                   # Main app
│   │   └── main.tsx                  # Entry point
│   ├── package.json                  # Node dependencies
│   └── vite.config.ts                # Vite configuration
├── Instructions/                      # Assignment materials
├── Data/                             # Test data
├── OPD_CLAIM_FLOW_DIAGRAMS.md        # System architecture
├── IMPLEMENTATION_SUMMARY.md         # Implementation details
├── QUICK_START.md                    # Quick reference guide
└── README.md                         # This file
```

## 🧪 Testing

### Test with Sample Members

The database is pre-seeded with 10 test members:

- **EMP001** - Standard case
- **EMP002** - Dental claim
- **EMP003** - High-value claim
- **EMP004** - Missing documents
- **EMP005** - Waiting period case
- **EMP006** - Alternative medicine
- **EMP007** - Pre-auth required
- **EMP008** - Fraud indicators
- **EMP009** - Excluded treatment
- **EMP010** - Network hospital

### Running Test Cases

```bash
cd backend
python test_api.py
```

This will test all 10 scenarios from `Instructions/test_cases.json`

### Manual Testing

1. Start both backend and frontend
2. Navigate to `http://localhost:5173`
3. Select a test member (EMP001-EMP010)
4. Upload sample documents
5. Submit claim
6. View decision and reasoning

## 🚢 Deployment

### Production Considerations

1. **Environment Variables**
   - Use production database credentials
   - Secure the Gemini API key
   - Set proper CORS origins

2. **Database**
   - Enable PostgreSQL connection pooling
   - Set up automated backups
   - Configure proper indexes

3. **Security**
   - Enable HTTPS
   - Add authentication/authorization
   - Implement rate limiting
   - Sanitize file uploads

4. **Monitoring**
   - Set up logging aggregation
   - Add performance monitoring
   - Configure error tracking

### Deployment Options

- **Backend**: Railway, Render, AWS EC2, Google Cloud Run
- **Frontend**: Vercel, Netlify, AWS S3 + CloudFront
- **Database**: AWS RDS, Google Cloud SQL, Supabase

## 📖 Additional Documentation

- [Flow Diagrams](./OPD_CLAIM_FLOW_DIAGRAMS.md) - Complete system architecture diagrams
- [Implementation Summary](./IMPLEMENTATION_SUMMARY.md) - Detailed implementation notes
- [Quick Start Guide](./QUICK_START.md) - Fast setup reference

## 📄 License

This project is created as part of an internship assignment.

## 🙏 Acknowledgments

- **Plum** - For the assignment opportunity
- **Google Gemini** - For LLM capabilities
- **Docling** - For OCR functionality
- **FastAPI** - For the excellent web framework

## 📞 Support

For questions or issues:
1. Check the [Quick Start Guide](./QUICK_START.md)
2. Review [Flow Diagrams](./OPD_CLAIM_FLOW_DIAGRAMS.md)
3. Check API documentation at `/docs`

---

**Built with ❤️ for automated insurance claim processing**
#   A I - P o w e r e d - O P D - C l a i m - A d j u d i c a t i o n - E n g i n e 
 
 
