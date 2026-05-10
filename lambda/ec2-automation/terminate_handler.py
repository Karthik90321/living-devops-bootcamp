import os
from helper import terminate_instance, send_email

# ---------------------------------------------------------------------------
# terminate_handler.py
# Lambda function triggered every evening at 6 PM UTC (11:30 PM IST)
# via EventBridge cron: cron(0 18 * * ? *)
#
# Job: Terminate the dev EC2 instance → send email confirmation
# This ensures you're never billed for an idle instance overnight.
# ---------------------------------------------------------------------------

INSTANCE_NAME = os.environ.get("INSTANCE_NAME", "bootcamp-dev-server")


def lambda_handler(event, context):
    """
    Entry point AWS Lambda calls.
    Terminates the instance by Name tag, then sends an email.
    """
    print(f"[terminate_handler] Starting. Event: {event}")

    try:
        terminated = terminate_instance(name=INSTANCE_NAME)

        if terminated:
            send_email(
                subject=f"🛑 EC2 Instance Terminated — {INSTANCE_NAME}",
                body=(
                    f"Your dev server has been shut down to save costs.\n\n"
                    f"Instance Name : {INSTANCE_NAME}\n"
                    f"Region        : ap-south-1\n\n"
                    f"It will be recreated tomorrow at 8 AM UTC (1:30 PM IST).\n"
                    f"No action needed."
                ),
            )
            return {
                "statusCode": 200,
                "body": f"Instance '{INSTANCE_NAME}' terminated successfully.",
            }
        else:
            # Instance not found — maybe it was already stopped manually
            msg = f"Instance '{INSTANCE_NAME}' not found. Nothing to terminate."
            print(f"[terminate_handler] {msg}")
            send_email(
                subject=f"⚠️ EC2 Terminate — Instance Not Found",
                body=f"{msg}\n\nCheck the AWS console if this is unexpected.",
            )
            return {"statusCode": 200, "body": msg}

    except Exception as e:
        print(f"[terminate_handler] ERROR: {e}")
        send_email(
            subject=f"❌ EC2 Termination FAILED — {INSTANCE_NAME}",
            body=f"Lambda encountered an error:\n\n{str(e)}",
        )
        raise
