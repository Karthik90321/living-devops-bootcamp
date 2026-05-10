#!/usr/bin/env python3
"""
ec2_auto_stop.py — Stop all running EC2 instances tagged Environment=dev in ap-south-1.

Usage:
    python ec2_auto_stop.py            # live run
    python ec2_auto_stop.py --dry-run  # list targets without stopping
"""

import argparse
import logging
import os
import sys

import boto3
from botocore.exceptions import ClientError, NoCredentialsError

REGION = "ap-south-1"
TAG_KEY = "Environment"
TAG_VALUE = "dev"

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def get_client(region: str = REGION):
    return boto3.client("ec2", region_name=region)


def find_running_dev_instances(client) -> list[str]:
    """Return instance IDs of all running instances tagged Environment=dev."""
    paginator = client.get_paginator("describe_instances")
    pages = paginator.paginate(
        Filters=[
            {"Name": "instance-state-name", "Values": ["running"]},
            {"Name": f"tag:{TAG_KEY}", "Values": [TAG_VALUE]},
        ]
    )

    instance_ids = []
    for page in pages:
        for reservation in page["Reservations"]:
            for instance in reservation["Instances"]:
                instance_ids.append(instance["InstanceId"])

    return instance_ids


def stop_instances(client, instance_ids: list[str]) -> list[dict]:
    """Stop instances and return the state-change records."""
    response = client.stop_instances(InstanceIds=instance_ids)
    return response["StoppingInstances"]


def print_summary(state_changes: list[dict]) -> None:
    log.info("─" * 55)
    log.info("Stop summary  (%d instance(s))", len(state_changes))
    log.info("─" * 55)
    for change in state_changes:
        iid = change["InstanceId"]
        prev = change["PreviousState"]["Name"]
        curr = change["CurrentState"]["Name"]
        log.info("  %-22s  %s → %s", iid, prev, curr)
    log.info("─" * 55)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List target instances without stopping them.",
    )
    args = parser.parse_args()

    try:
        client = get_client()
        log.info(
            "Scanning for running instances tagged %s=%s in %s …",
            TAG_KEY, TAG_VALUE, REGION,
        )

        instance_ids = find_running_dev_instances(client)

        if not instance_ids:
            log.info("No running %s=%s instances found. Nothing to do.", TAG_KEY, TAG_VALUE)
            return

        log.info("Found %d instance(s): %s", len(instance_ids), ", ".join(instance_ids))

        if args.dry_run:
            log.info("[DRY RUN] Would stop: %s", ", ".join(instance_ids))
            return

        log.info("Stopping instances …")
        state_changes = stop_instances(client, instance_ids)
        print_summary(state_changes)

    except NoCredentialsError:
        log.error(
            "AWS credentials not found. Configure via environment variables, "
            "~/.aws/credentials, or an IAM role."
        )
        sys.exit(1)
    except ClientError as exc:
        error_code = exc.response["Error"]["Code"]
        error_msg = exc.response["Error"]["Message"]
        log.error("AWS API error [%s]: %s", error_code, error_msg)
        sys.exit(1)
    except Exception as exc:  # noqa: BLE001
        log.error("Unexpected error: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
