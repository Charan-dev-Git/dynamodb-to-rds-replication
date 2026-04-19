import json
import os
import time
import random
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])


def generate_user(user_id: str):
    first_names = ["Arun", "Vijay", "Kumar", "Priya", "Divya", "Nila"]
    last_names = ["Raj", "Kannan", "Mohan", "Devi", "Suresh", "Mani"]
    genders = ["Male", "Female"]

    return {
        "user_id": user_id,
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "phone_number": f"9{random.randint(100000000, 999999999)}",
        "age": random.randint(18, 45),
        "gender": random.choice(genders),
        "updated_at": datetime.now(timezone.utc).isoformat()
    }


def lambda_handler(event, context):
    now = int(time.time())

    # every run: insert one new user
    new_user_id = f"user-{now}"
    new_user = generate_user(new_user_id)

    table.put_item(Item=new_user)

    result = {
        "inserted_user": new_user_id,
        "updated_user": None
    }

    # every 10 min effect: alternate runs do one update
    # since scheduler runs every 5 min, even 10-minute bucket = update
    bucket = now // 600

    if bucket % 2 == 0:
        existing_user_id = new_user_id  # simple project logic
        table.update_item(
            Key={"user_id": existing_user_id},
            UpdateExpression="SET phone_number = :p, age = :a, updated_at = :u",
            ExpressionAttributeValues={
                ":p": f"9{random.randint(100000000, 999999999)}",
                ":a": random.randint(18, 45),
                ":u": datetime.now(timezone.utc).isoformat()
            }
        )
        result["updated_user"] = existing_user_id

    return {
        "statusCode": 200,
        "body": json.dumps(result)
    }