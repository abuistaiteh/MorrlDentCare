# Morrl DentCare — Family Dental Care

<p align="center">
  <img src="assets/logo.png" width="180" />
</p>

A production-ready serverless web app for **online dental appointment scheduling**, built entirely on AWS.

---

## 🧠 Core Features

| Feature | Description |
|--------|-------------|
| Online Appointment Booking | Patients select provider, date, service, and time |
| **45-Minute Time Slot Scheduling** | Appointment times are generated in realistic 45-minute blocks |
| **Automatic Time Slot Blocking** | Once a time slot is booked with a specific doctor, that time is **removed from availability** to prevent double-booking |
| Multi-Doctor Support | The same time slot may still be available for **other doctors** |
| Email Confirmation | Appointment confirmation email is automatically sent via **Amazon SES** from `no-reply@morrl.com` |
| Reminder Emails | **1-day** and **same-day** automatic reminders via **EventBridge → Lambda → SES** |
| Serverless & Scalable | Built using **S3 + CloudFront + API Gateway + Lambda + DynamoDB + SES** |
| Contact Form Storage | Patient contact messages are securely written to DynamoDB |
| Global Performance | CloudFront ensures fast loading speeds anywhere |

---

## 🏛️ Architecture

![Architecture Diagram](assets/morrl_architecture.png)

---

## 🧱 Tech Stack & AWS Services

| Area | Service(s) | Purpose |
|---|---|---|
| Hosting | S3 + CloudFront | Static website + global CDN |
| API Layer | Amazon API Gateway | Connects frontend to Lambda backend |
| Compute | AWS Lambda | Booking logic, reminders, validation |
| Database | DynamoDB | Stores appointments + contact messages |
| Email | Amazon SES | Sends confirmation + reminder emails |
| Scheduling | Amazon EventBridge | Triggers reminder Lambdas daily |
| Monitoring | CloudWatch | Logs + operational visibility |
| Operations | AWS Health Dashboard | Service health awareness |

---

## 🔗 API Endpoints

```
GET  https://pl65lk9u96.execute-api.us-east-1.amazonaws.com/prod/booked?doctor=Dr.%20Sarah%20Johnson&date=2025-11-12

POST https://pl65lk9u96.execute-api.us-east-1.amazonaws.com/prod/book
```

### POST Body Example
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "doctor": "Dr. Sarah Johnson",
  "service": "Teeth Cleaning",
  "date": "2025-11-12",
  "time": "10:30"
}
```

---

## 🗂 Project Structure

```
.
├─ assets/
│  ├─ logo.png
│  ├─ morrl_architecture.png
│   ├─ homepage.png
│  ├─ homepage2.png
│  ├─ booking_form.png
│  └─ confirmation_email.png
├─ backend/
│  ├─ lambda_book_appointment.py
│  ├─ lambda_ContactHandler.py
│  ├─ lambda_getbookedslots.py
│  ├─ lambda_reminder_one_day.py
│  └─ lambda_reminder_same_day.py
├─ frontend/
│  └─ appointment.html
├─ LICENSE
└─ README.md
```

---

## 🚀 Deployment Summary

1. **DynamoDB** → Create table `amzn-clinic1data` (PK: `AppointmentsId`)
2. **Lambda Functions** → Deploy backend logic
3. **API Gateway** → Connect Lambdas to HTTPS endpoints
4. **SES** → Verify domain + sender email (`no-reply@morrl.com`)
5. **EventBridge** → Create:
   - 1-day reminder rule
   - Same-day reminder rule
6. **Frontend Hosting** → Upload website to S3 → Serve via CloudFront

---

## 🖼️ Screenshots / Demo

### Home Page  
![Home Page](assets/homepage2.png)

### Appointment Booking Form  
![Appointment Form](assets/booking_form.png)

### Email Confirmation  
![Confirmation Email](assets/confirmation_email.png)

---

## 📄 License
MIT — see [LICENSE](LICENSE)

---

## 🧑‍💻 Author
**Mahmoud Abuistaiteh**  
AWS Cloud Practitioner — Serverless Application Builder
