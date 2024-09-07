# Ecommerce Task Veeva
### Overview
This project implements a cloud-native e-commerce platform designed to run on AWS. The platform is built with a focus on high availability, scalability, and security, while supporting real-time processing of sales data.
The system includes:
- A web front end hosted on a Content Delivery Network (CDN).
- A RESTful API backend for managing product-related operations.
- A database for persistent storage, Amazon DynamoDB(NoSQL).
- Amazon Cognito for user authentication and secure access to APIs.
- AWS Kinesis and AWS Lambda for real-time data processing and analysis of products events.

## Table of Contents
- [Architecture Diagram](#features)
- [Scalability and Availability](#scalability-and-availability)
- [Security](#security)
- [Cost Optimization](#cost-optimization)
- [Monitoring and Performance](#monitoring-and-performance)
- [Setup](#setup)
- [API Endpoints](#usage)
- [Workflows](#workflows-for-monitoring)
- [Running Tests](#running-tests)

## Architecture Diagram
Diagram is attached to this repo, with explanations about each part.
[picture here with some explnations]

### Scalability and Availability
To ensure scalability and availability, I used a Load Balancer (ELB), Auto-scaling groups, and a multi-AZ setup in the databases.
Load Balancer - Distributes incoming traffic across multiple servers to prevent overload.
Auto-scaling groups - Ensures that the infrastructure scales up or down based on demand.
Multi-AZ deployments provide high availability by ensuring that services remain available even if one data center fails.
In this project, it ensures the e-commerce platform can handle high traffic during peak periods, such as holidays.

### Security
AWS IAM - Manages access to AWS resources, ensuring that only authorized users can perform certain actions.
AWS CloudTrail - Logs all API calls and actions performed within the AWS environment, for tracking down unauthorized activities.
AWS WAF - Protects the ecommerce platform from common web threats like SQL injection and DDoS attacks.
Encryption with AWS KMS -  Ensures that sensitive data (e.g., customer payment information) is encrypted both at rest and in transit.

IAM roles ensure that each part of the e-commerce system (such as Lambda functions or EC2 instances) has the minimum level of access required to perform its function.
AWS WAF protects the e-commerce website from malicious attacks. I have added two WAFs: one to protect the CDN from possible attacks, and the second to protect the ELB, particularly for specific APIs or endpoints.
According to the [AWS Docs](https://docs.aws.amazon.com/whitepapers/latest/web-application-hosting-best-practices/an-aws-cloud-architecture-for-web-hosting.html), it's a common practice.

### Real-Time Processing
For the aspect of Real-time processing, I used AWS Kinesis and AWS Lambda.
AWS Kinesis allows for the collection of large streams of data related to the e-commerce platform, such as product creation or stock updates. It can also capture user behavior for triggering future marketing features.
### Cost Optimization
Auto-scaling ensures resources are only scaled up when needed and scaled down when traffic is lower than usual.
Spot Instances also help us to use lower cost unused AWS capacity.
In the ecommerce project it helps us to avoid excessive payment for unused resources.
### Monitoring
Amazon CloudWatch tracks essential metrics such as CPU usage, memory, request latency, and error rates across all AWS services.
CloudWatch can also be filtered to specific parameters.
AWS X-Ray provides detailed tracing of requests in the services, to pinpoint performance issues.
In the ecommerce platform, it can help us to monitor critical aspects, such as page load time, and inventory API performance. These services can also be useful for future development like tracing the preformance of using a cart currectly, etc.
## Setup
- Python Environment: 3.12.1
1. Clone the repository(if you downloaded via zip file, skip this part):
   ```bash
   git https://github.com/Dark-Floyd/ecommerce-veeva.git
   cd ecommerce-veeva
2. Create and activate virutal environment:
    ```bash
    python -m venv env
    # On Windows
    .\env\Scripts\activate
    # On macOS/Linux
    source env/bin/activate
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
4. Installing test dependencies:
    ```bash
    pip install -r requirements-dev.txt
    ```

### Usage
Run the FastApi app:
```bash
uvicorn app.main:app --reload
```
 
## API Endpoints
```api/products``` - [GET] Retrieve all products.
```api/products``` - [POST] Add a new product.
```api/products/{:id}``` - [GET] Retrieve a specific product by ID.
```api/products/{:id}``` - [PUT] Update an existing product.
```api/products/{:id}``` - [DELETE] Remove a product.
## Workflows for monitoring:
To track and monitor crucial aspects of the e-commerce platform, I set up the following workflows with AWS Lambda:
 - Lambda to Monitor API Gateway or Load Balancers for high rates of 4xx (client) and 5xx (server) errors.
 - Lambda to Monitor and alert suppliers in case of low stock in some of the products.
- Configuring CloudWatch to monitor high response times.
- Monitoring Aurora DB for events like slow queries, failed queries, replication lag, or storage nearing its limit.
- Setting up alerts for suspicious activity in CloudTrail, to track unknown logins, and unusual data transfers.



## Running Tests
 After installing the ```requirements-dev.txt``` file, just run ```pytest``` to run the test file.
 Further elaboration about the tests:
```test_create_product``` - Validates create product.
 ```test_list_products``` - Validates get products.
``` test_update_product``` - Validates update product.
```test_delete_product``` - Validates delete product.

```test_create_product_missing_field``` - Tests for the creation of a product with missing field.
```test_create_product_invalid_data_type``` - Tests product creation with incorrect data types.
```test_get_nonexistent_product``` - Tests a nonexistent product.
```test_update_nonexistent_product``` - Tests an update on nonexistent product.
```test_delete_nonexistent_product``` - Tests a deletion on nonexistent product.


Helpful Documentation:
[Web Application Hosting in the AWS Cloud](https://docs.aws.amazon.com/whitepapers/latest/web-application-hosting-best-practices/an-aws-cloud-architecture-for-web-hosting.html)
[How to Move Your E-Commerce Website to Amazon Web Services](https://clutch.co/resources/how-to-move-your-e-commerce-website-to-amazon-web-services)

 
