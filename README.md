# VURA
# VURA — Virtuous Urban Resilience Assistance

> “The infrastructure is ready. The citizen isn’t.”

VURA is an AI-powered civic behavior monitoring and nudging system built for Indian smart cities.

Instead of focusing only on infrastructure, VURA focuses on the real root problem behind urban chaos: civic behavior.

The system detects whether people are forming proper queues or clustering chaotically in public spaces such as bus stops, then responds in real time using:

- AI crowd analysis
- Social proof nudges
- Live dashboard monitoring
- Multilingual voice announcements
- Civic behavior scoring

Built during the AI4India × HopeWorks Hackathon under the Smart Cities track.
---

## Team SCRITHM

| Name | Role |
|---|---|
| **Sankhyasri Perali** | Project Lead · Product Direction · System Coordination · Execution |
| **Somasi Yogiswari Tejaswi** | Creative Partner · Presentation Design |
| **Merugu Srujana** | Creative & Documentation Partner |
| **Arukoti Bhavishya** | Technical Research & Support |## Team SCRITHM

---

# Problem Statement

Most smart city systems today only monitor infrastructure.

They record violations.
They store footage.
But they rarely change human behavior.

Through informal field observations and discussions with drivers, conductors, and commuters in Hyderabad, we identified recurring civic problems:

- Queue breaking at bus stops
- Chaotic crowd formation
- Signal violations
- Public disorder despite existing infrastructure

The insight behind VURA:

People usually follow rules when:
1. They see others following them
2. They personally benefit from following them

VURA is designed around behavioral psychology and positive reinforcement instead of punishment.

---

# Core Features

## Real-Time Crowd Detection
- Uses YOLOv8 Nano for person detection
- Detects people through webcam/IP camera feeds

## Queue vs Chaos Classification
- Custom behavioral analysis algorithm
- Identifies whether people are forming organized queues or chaotic clusters

## Social Proof Nudging
Example:
> “8 out of 10 people are already queuing. Join them.”

## Multilingual Voice Announcements
Supports:
- English
- Hindi
- Telugu
- Kannada
- Tamil
- Malayalam

## Civic Score System
- Tracks civic behavior trends over time
- Updates dynamically based on crowd behavior

## Live Smart City Dashboard
Includes:
- Live monitor
- Civic score analytics
- City heatmap
- Queue monitoring
- Crowd status

---

# Tech Stack

| Layer | Technology |
|---|---|
| AI Detection | YOLOv8 Nano |
| Computer Vision | OpenCV |
| Backend | Flask |
| Frontend | HTML, CSS, JavaScript |
| ML Runtime | PyTorch |
| Data Storage | JSON |
| Numerical Processing | NumPy |
| Voice Engine | Web Speech API |

---

# How It Works

Camera Feed → AI Detection → Queue Analysis → Dashboard Update → Voice Nudge → Civic Score Update

The system continuously monitors crowd behavior and responds in real time.

<img width="1886" height="918" alt="image" src="https://github.com/user-attachments/assets/bfc9e08f-727b-4029-81d4-c9a8cd1120c0" />

<img width="1884" height="806" alt="image" src="https://github.com/user-attachments/assets/adb32ca9-536e-4212-bed8-570511289aa5" />


---
## AI Assistance & Development Process

This prototype was developed using AI-assisted workflows alongside independent research, system design, testing, iteration, and integration by the team.

Tools such as Claude were used to support:
- code generation,
- debugging,
- rapid prototyping,
- documentation,
- and iterative development.

The project direction, behavioral framework, feature evolution, implementation decisions, testing flow, and overall system integration were led and managed by the team.

---

# Project Evolution

## V1
- Basic crowd detection
- Zone monitoring

## V2
- Heatmaps
- Civic scoring
- Multilingual dashboard

## V3 (Final Prototype)
- Queue vs chaos AI classification
- Social proof system
- Voice nudges
- Improved dashboard UX
- Behavioral reinforcement model

---

## Deployment link
   https://vura-5c47.onrender.com

---

# Installation

## Requirements

- Python 3.11+
- Webcam
- Chrome or Edge browser

## Install Dependencies

```bash
pip install opencv-python ultralytics numpy flask

---


