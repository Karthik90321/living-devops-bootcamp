import boto3
import os

# ---------------------------------------------------------------------------
# helper.py
# Shared utility functions used by both create_EC2.py and terminate_handler.py
# Think of this as your "toolbox" — functions here do one job each.
# ---------------------------------------------------------------------------

REGION = os.environ.get("AWS_REGION", "ap-south-1")
ec2 = boto3.client("ec2", region_name=REGION)
ses = boto3.client("ses", region_name=REGION)

SENDER_EMAIL  = os.environ.get("SENDER_EMAIL", "nimmaturi234@gmail.com")
RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL", "nimmaturi234@gmail.com")


# ── EC2 helpers ────────────────────────────────────────────────────────────

def create_instance(name: str, instance_type: str = "t3.micro", ami_id: str = None) -> str:
    """
    Launch one EC2 instance and tag it with a Name.
    Returns the new instance's ID.

    Why we tag with Name:
        AWS treats Name as a tag, not a real property.
        We use this tag later to find and terminate the instance by name.
    """
    if ami_id is None:
        # Amazon Linux 2023 AMI for ap-south-1 (free tier eligible)
        # Replace this if you're in a different region
        ami_id = "ami-0627662924eb1b8c6"

    response = ec2.run_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": name}],
            }
        ],
    )

    instance_id = response["Instances"][0]["InstanceId"]
    print(f"[helper] Created instance: {instance_id} with name tag: {name}")
    return instance_id


def get_instance_id_by_name(name: str) -> str | None:
    """
    Find an EC2 instance ID by its Name tag.
    Returns the instance ID string, or None if not found.

    Why we need this:
        terminate_instances() requires an instance ID (i-xxxx), not a name.
        So we first look up the ID from the Name tag.
    """
    response = ec2.describe_instances(
        Filters=[
            {"Name": "tag:Name",           "Values": [name]},
            {"Name": "instance-state-name", "Values": ["running", "pending", "stopped"]},
        ]
    )

    reservations = response.get("Reservations", [])
    if not reservations:
        print(f"[helper] No instance found with Name tag: {name}")
        return None

    instance_id = reservations[0]["Instances"][0]["InstanceId"]
    print(f"[helper] Found instance: {instance_id} for name: {name}")
    return instance_id


def terminate_instance(name: str) -> bool:
    """
    Terminate an EC2 instance by its Name tag.
    Returns True if terminated, False if instance not found.
    """
    instance_id = get_instance_id_by_name(name)
    if not instance_id:
        return False

    ec2.terminate_instances(InstanceIds=[instance_id])
    print(f"[helper] Terminating instance: {instance_id}")
    return True


# ── SES email helper ───────────────────────────────────────────────────────

def send_email(subject: str, body: str) -> None:
    """
    Send a plain-text email via SES.
    Both sender and receiver must be verified in SES sandbox mode.
    """
    try:
        ses.send_email(
            Source=SENDER_EMAIL,
            Destination={"ToAddresses": [RECEIVER_EMAIL]},
            Message={
                "Subject": {"Data": subject},
                "Body":    {"Text": {"Data": body}},
            },
        )
        print(f"[helper] Email sent: {subject}")
    except Exception as e:
        # Don't let email failure crash the main Lambda job
        print(f"[helper] Email failed (non-fatal): {e}")
