# dynamodb-to-rds-replication
Secure AWS event-driven project: DynamoDB Streams → Lambda → Private RDS PostgreSQL with Secrets Manager VPC endpoint.

# Secure Event-Driven Data Replication on AWS

This project implements a secure, event-driven data replication pipeline on AWS using Terraform.

## Architecture
EventBridge -> Lambda -> DynamoDB -> DynamoDB Streams -> Lambda -> Private RDS PostgreSQL

## AWS Services Used
- AWS Lambda
- Amazon DynamoDB
- DynamoDB Streams
- Amazon RDS PostgreSQL
- AWS Secrets Manager
- VPC Interface Endpoint
- Amazon EventBridge
- Terraform

## Features
- Scheduled user data generation
- Real-time change capture using DynamoDB Streams
- Replication into private RDS PostgreSQL
- Secrets Manager access through VPC Endpoint
- Infrastructure as Code using Terraform

## Security
- RDS kept private
- Lambda connected through VPC
- Secrets accessed securely using VPC Endpoint

## Notes
Do not commit `terraform.tfvars`, state files, or secrets.
