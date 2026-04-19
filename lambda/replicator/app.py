import json
import os

import boto3
import pg8000.native

secrets_client = boto3.client("secretsmanager")


def get_db_credentials():
    secret_name = os.environ["SECRET_NAME"]
    print(f"Reading secret: {secret_name}")
    response = secrets_client.get_secret_value(SecretId=secret_name)
    secret = json.loads(response["SecretString"])
    return secret


def get_connection():
    secret = get_db_credentials()
    print("Trying DB connection...")

    conn = pg8000.native.Connection(
        host=secret["host"],
        port=int(secret["port"]),
        database=secret["dbname"],
        user=secret["username"],
        password=secret["password"]
    )

    print("DB connection successful")
    return conn


def ddb_value_to_python(value):
    if "S" in value:
        return value["S"]
    if "N" in value:
        n = value["N"]
        return int(n) if n.isdigit() else float(n)
    return None


def parse_ddb_image(image):
    parsed = {}
    for key, value in image.items():
        parsed[key] = ddb_value_to_python(value)
    return parsed


def ensure_table(conn):
    print("Ensuring users table exists...")

    conn.run("""
        CREATE TABLE IF NOT EXISTS users (
            user_id VARCHAR(100) PRIMARY KEY,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone_number VARCHAR(20),
            age INT,
            gender VARCHAR(20),
            updated_at TIMESTAMP
        );
    """)

    print("Users table ready")


def upsert_user(conn, user):
    print(f"Upserting user: {user.get('user_id')}")

    conn.run("""
        INSERT INTO users (
            user_id, first_name, last_name, phone_number, age, gender, updated_at
        )
        VALUES (:user_id, :first_name, :last_name, :phone_number, :age, :gender, :updated_at)
        ON CONFLICT (user_id)
        DO UPDATE SET
            first_name = EXCLUDED.first_name,
            last_name = EXCLUDED.last_name,
            phone_number = EXCLUDED.phone_number,
            age = EXCLUDED.age,
            gender = EXCLUDED.gender,
            updated_at = EXCLUDED.updated_at;
    """, **user)

    print(f"User replicated: {user.get('user_id')}")


def lambda_handler(event, context):
    print("🔥 Replicator Lambda started")
    print("Incoming event:", json.dumps(event))

    conn = get_connection()
    ensure_table(conn)

    count_result = conn.run("SELECT COUNT(*) FROM users;")
    print(f"Current users count in RDS: {count_result}")

    records = event.get("Records", [])
    print(f"Number of stream records received: {len(records)}")

    for record in records:
        event_name = record.get("eventName")
        print(f"Processing event: {event_name}")

        if event_name in ["INSERT", "MODIFY"]:
            new_image = record["dynamodb"].get("NewImage")
            if new_image:
                user = parse_ddb_image(new_image)
                print(f"Parsed user data: {user}")
                upsert_user(conn, user)

    print("✅ Replicator Lambda completed successfully")

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Replication successful"})
    }