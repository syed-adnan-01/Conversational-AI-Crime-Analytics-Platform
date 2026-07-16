# Intelligent Conversational AI & Crime Analytics Platform

<p align="center">
  <img src="assets/logo.png" alt="CrimeSphere AI" width="180"/>
</p>

<p align="center">

![React](https://img.shields.io/badge/Frontend-React%20%7C%20Next.js-61DAFB?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)
![Zoho Catalyst](https://img.shields.io/badge/Platform-Zoho%20Catalyst-blue?style=for-the-badge)
![QuickML](https://img.shields.io/badge/AI-QuickML-purple?style=for-the-badge)
![Neo4j](https://img.shields.io/badge/Graph-Neo4j-008CC1?style=for-the-badge&logo=neo4j)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</p>

---

# 📖 Overview

CrimeSphere AI is an **AI-powered Crime Intelligence Platform** designed for law enforcement agencies to transform traditional crime record management into an intelligent investigative ecosystem.

The platform enables investigators, analysts, supervisors, and policymakers to interact with crime databases using **natural language**, uncover hidden criminal relationships, generate AI-powered case summaries, analyze crime trends, forecast crime hotspots, and support data-driven policing.

Built on **Zoho Catalyst**, CrimeSphere AI combines **Conversational AI, Knowledge Graphs, Crime Analytics, Machine Learning, and Explainable AI** into a unified intelligence platform.

---

# 🎯 Problem Statement

Traditional police information systems store enormous amounts of crime data but require investigators to manually search and correlate records.

CrimeSphere AI solves this problem by enabling users to:

- 💬 Ask questions in natural language
- 🔍 Search FIRs intelligently
- 🕸 Discover criminal networks
- 📈 Analyze crime trends
- 🧠 Generate AI-powered investigation summaries
- 📍 Detect crime hotspots
- ⚠ Predict future criminal activity
- 📄 Generate investigation reports instantly

---

# ✨ Key Features

## 🤖 Conversational AI

- Natural Language Querying
- Multi-turn conversations
- Context-aware chat
- English & Kannada support
- Voice interaction
- PDF conversation export

Example:

> Show all robbery FIRs registered in Bengaluru during the last six months involving repeat offenders.

---

## 🔎 Intelligent FIR Search

Search using

- FIR Number
- Crime Number
- Accused Name
- Victim Name
- Police Station
- IPC Sections
- Crime Type
- Investigation Status
- Date Range

---

## 🕸 Criminal Network Analysis

Discover relationships between

- Accused
- Victims
- Police Officers
- Courts
- Locations
- FIRs
- Acts
- Sections

Supports

- Gang Detection
- Criminal Associations
- Repeat Offenders
- Link Analysis

---

## 📊 Crime Analytics

Interactive dashboards including

- Crime Heatmaps
- Monthly Trends
- Crime Distribution
- Police Station Performance
- Crime Category Analysis
- Investigation Status
- FIR Growth

---

## 📍 Crime Hotspot Detection

AI identifies

- Emerging Crime Clusters
- High-Risk Areas
- Seasonal Crime Trends
- District-wise Analysis

---

## 🧠 Investigator Decision Support

Automatically generates

- Case Summaries
- Investigation Timelines
- Similar Past Cases
- Potential Investigation Leads
- Officer Recommendations

---

## 👮 Offender Profiling

Risk analysis using

- Previous FIR History
- Crime Frequency
- Violent Behaviour
- Repeat Offending
- Modus Operandi

Outputs

- Risk Score
- Threat Level
- Investigation Priority

---

## 📄 Report Generation

Generate

- PDF Reports
- Investigation Reports
- Crime Statistics
- Case Summaries

---

## 🌐 Multilingual Support

Supported Languages

- English
- Kannada

Future Support

- Hindi
- Tamil
- Telugu

---

## 🔒 Enterprise Security

- Role-Based Access Control
- JWT Authentication
- Audit Logs
- Secure APIs
- HTTPS
- Encryption

---

# 🏗 System Architecture

```
                             Users

 Investigator • Analyst • SHO • DGP • Admin

                     │

                     ▼

           React + Next.js Frontend

                     │

                     ▼

         Zoho Catalyst Authentication

                     │

                     ▼

           Catalyst API Gateway

                     │

                     ▼

             AI Orchestrator Layer

      ┌──────────────┬──────────────┬──────────────┐

      │              │              │

   SQL Agent     Graph Agent   Analytics Agent

      │              │              │

      ▼              ▼              ▼

Catalyst DB      Neo4j         QuickML

      │              │              │

      └──────────────┴──────────────┘

                     │

                     ▼

           AI Response Generator

                     │

                     ▼

                  Dashboard
```

---

# 🧠 AI Modules

| Module | Description |
|----------|-------------|
| SQL Agent | Natural language to SQL |
| Graph Agent | Criminal network discovery |
| Analytics Agent | Crime statistics |
| Forecast Agent | Crime prediction |
| Recommendation Agent | Similar cases |
| Report Agent | AI-generated summaries |
| Explainability Agent | Evidence-backed AI responses |

---

# 🗄 Database

Based on the Karnataka Police FIR ER Schema.

Major Entities

- CaseMaster
- Victim
- Accused
- ComplainantDetails
- ArrestSurrender
- Employee
- Court
- District
- Unit
- Chargesheet
- Act
- Section
- CrimeHead
- CrimeSubHead

Additional AI Tables

- ConversationHistory
- AIReports
- CrimeEmbeddings
- PredictionResults
- RiskScores
- Alerts
- Feedback
- AuditLogs

---

# ⚙ Tech Stack

## Frontend

- React
- Next.js
- Tailwind CSS
- TypeScript
- Framer Motion
- ECharts
- Leaflet.js

---

## Backend

- Python
- FastAPI
- Catalyst Functions

---

## AI

- Zoho QuickML
- RAG
- NLP
- LLM
- Explainable AI

---

## Graph Database

- Neo4j

---

## Database

- Catalyst Data Store
- Catalyst NoSQL

---

## Storage

- Catalyst Stratus

---

## Authentication

- Catalyst Authentication

---

## Deployment

- Zoho Catalyst

---

# 📂 Project Structure

```
CrimeSphere-AI/

│

├── frontend/

│ ├── app/

│ ├── components/

│ ├── pages/

│ ├── hooks/

│ ├── services/

│ └── assets/

│

├── backend/

│ ├── api/

│ ├── controllers/

│ ├── services/

│ ├── repositories/

│ ├── ai/

│ ├── analytics/

│ ├── graph/

│ ├── auth/

│ └── utils/

│

├── catalyst/

│ ├── functions/

│ ├── datastore/

│ ├── quickml/

│ ├── cron/

│ ├── signals/

│ ├── pipelines/

│ └── circuits/

│

├── graph/

│ ├── neo4j/

│ ├── cypher/

│ └── algorithms/

│

├── docs/

├── assets/

├── README.md

└── LICENSE
```

---

# 🚀 Future Roadmap

- Facial Recognition Integration
- CCTV Analytics
- Vehicle Tracking
- Mobile Application
- Live Crime Monitoring
- Digital Evidence Management
- Drone Surveillance Integration
- Cyber Crime Intelligence
- Social Media Threat Detection

---

# 📸 Screenshots

| Dashboard | AI Chat |
|------------|---------|
| Coming Soon | Coming Soon |

---

# 📈 KPIs

- AI Response < 5 seconds
- Search Response < 2 seconds
- 99% Availability
- High Precision Crime Search
- Explainable AI Responses
- Secure Role-Based Access

---

# 👨‍💻 Team

### Team Name

**CrimeSphere AI**

### Built For

**Smart India Hackathon (SIH) 2026**

### Organization

Karnataka Police Department

---

# 📜 License

This project is developed for educational and research purposes under the Smart India Hackathon.

---

# ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub.

---

<p align="center">

### **"Empowering Law Enforcement through Artificial Intelligence."**

Made with ❤️ for **Smart India Hackathon 2026**

</p>
