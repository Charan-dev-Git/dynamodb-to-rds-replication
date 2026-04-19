# DynamoDB to RDS Replication (AWS Project)

This project demonstrates a secure, event-driven data replication pipeline on AWS using Terraform.

## 🚀 Overview

The system captures data changes from DynamoDB and replicates them into a private Amazon RDS PostgreSQL database using AWS Lambda.

## 🏗️ Architecture

EventBridge (Scheduler)  
→ Lambda (User Generator)  
→ DynamoDB  
→ DynamoDB Streams  
→ Lambda (Replicator)  
→ Private RDS PostgreSQL  

## 🧰 Technologies Used

- AWS Lambda  
- Amazon DynamoDB  
- DynamoDB Streams  
- Amazon RDS (PostgreSQL)  
- AWS Secrets Manager  
- VPC (Private Networking)  
- VPC Interface Endpoint  
- Amazon EventBridge  
- Terraform (Infrastructure as Code)

## ⚙️ Key Features

- Scheduled user data generation using EventBridge  
- Real-time change detection using DynamoDB Streams  
- Data replication to RDS using Lambda  
- Secure database access using Secrets Manager  
- Private RDS deployment (not publicly accessible)  
- Fully automated infrastructure using Terraform  

## 🔐 Security Design

- RDS deployed in private subnets  
- Lambda connected through VPC  
- No public database exposure  
- Secrets stored in AWS Secrets Manager  
- Access to Secrets Manager via VPC Endpoint (no internet dependency)  

## 📊 Output

- Data successfully replicated from DynamoDB to PostgreSQL  
- Verified using DBeaver and CloudWatch logs  

## 📁 Project Structure
.
├── lambda/
│ ├── user_processor/
│ └── replicator/
├── dynamodb.tf
├── rds.tf
├── lambda.tf
├── iam.tf
├── scheduler.tf
├── provider.tf
├── variables.tf
├── outputs.tf
├── README.md


## ⚠️ Notes

- `terraform.tfvars` is excluded for security reasons  
- No sensitive data is stored in the repository  
- Resources should be destroyed after use to avoid cost  

## 🧠 Learning Outcome

- Built a secure event-driven architecture  
- Understood DynamoDB Streams processing  
- Learned VPC-based Lambda to RDS connectivity  
- Implemented real-world AWS security practices  

---
