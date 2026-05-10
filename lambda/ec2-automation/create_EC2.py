import os
from helper import create_instance, send_email

# ---------------------------------------------------------------------------
# create_EC2.py
# Lambda function triggered every morning at 8 AM UTC (1:30 PM IST)
# via EventBridge cron: cron(0 8 * * ? *)
#
# Job: Create an EC2 instance → send email confirmation
# ---------------------------------------------------------------------------

INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "bootcamp-dev-server")
INSTANCE_TYPE = os.environ.get("INSTANCE_TYPE", "t3.micro")


def lambda_handler(event, context):
    """
    entry point AWS Lambda calls.
    `event`   — JSON passed by EventBridge (we don't use it here)
    `context` — Lambda runtime info (request ID, time remaining, etc.)
    """
    print(f"[create_EC2] Starting. Event: {event}")

    try:
        instance_id = create_instance(
            name=INSTANCE_NAME,
            instance_type=INSTANCE_TYPE,
        )

        send_email(
            subject=f"✅ EC2 Instance Created — {INSTANCE_NAME}",
            body=(
                f"Your dev server is up and running!\n\n"
                f"Instance ID   : {instance_id}\n"
                f"Instance Name : {INSTANCE_NAME}\n"
                f"Instance Type : {INSTANCE_TYPE}\n"
                f"Region        : ap-south-1\n\n"
                f"It will be auto-terminated at 6 PM UTC (11:30 PM IST).\n"
                f"Log in: AWS Console → EC2 → Instances"
            ),
        )

        return {
            "statusCode": 200,
            "body": f"Instance {instance_id} created successfully.",
        }

    except Exception as e:
        print(f"[create_EC2] ERROR: {e}")
        send_email(
            subject=f"❌ EC2 Creation FAILED — {INSTANCE_NAME}",
            body=f"Lambda encountered an error:\n\n{str(e)}",
        )
        raise  # Re-raise so Lambda marks the invocation as failed
