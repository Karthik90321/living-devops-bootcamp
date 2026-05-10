# EC2 Auto Start/Stop via Lambda + EventBridge

Bootcamp project from Akhilesh's Living DevOps session (Apr 29, 2026).

## What it does
| Time | Action |
|---|---|
| 8:00 AM UTC (1:30 PM IST) | Lambda creates a dev EC2 instance |
| 6:00 PM UTC (11:30 PM IST) | Lambda terminates it to save cost |
| Both times | SES email notification sent |

## File structure
```
ec2-automation/
├── helper.py            # Shared: create_instance, terminate_instance, send_email
├── create_EC2.py        # Lambda 1: triggered at 8 AM UTC
├── terminate_handler.py # Lambda 2: triggered at 6 PM UTC
└── README.md
```

## Environment variables to set on each Lambda
| Variable | Example value |
|---|---|
| INSTANCE_NAME | bootcamp-dev-server |
| INSTANCE_TYPE | t2.micro |
| AWS_REGION | ap-south-1 |
| SENDER_EMAIL | nimmaturi234@gmail.com |
| RECEIVER_EMAIL | nimmaturi234@gmail.com |

## IAM permissions needed
Both Lambda execution roles need:
- `ec2:RunInstances`
- `ec2:TerminateInstances`
- `ec2:DescribeInstances`
- `ec2:CreateTags`
- `ses:SendEmail`
- `logs:CreateLogGroup` / `logs:PutLogEvents`

## EventBridge cron expressions
- Create:    `cron(0 8 * * ? *)`   → 8:00 AM UTC daily
- Terminate: `cron(0 18 * * ? *)`  → 6:00 PM UTC daily

## Deployment steps
1. Zip helper.py + create_EC2.py → upload to Lambda function "create_EC2"
2. Zip helper.py + terminate_handler.py → upload to Lambda function "terminate_handler"
3. Set environment variables on both functions
4. Attach IAM policies to both execution roles
5. Create two EventBridge rules pointing to each function
