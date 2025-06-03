from flask import Blueprint, request, jsonify, render_template
from app.extensions import collection
from app.config import GITHUB_SECRET
from datetime import datetime
import pytz
import hmac
import hashlib

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')


@webhook.route('/receiver', methods=["POST"])
def receiver():
    """
    Receives GitHub webhook POST requests, validates signature, and stores
    cleanly structured Push, Pull Request, or Merge events to MongoDB.
    """
    
    #Inline verify_signature logic
    signature = request.headers.get('X-Hub-Signature-256')
    if not signature:
        print("signature", signature)
        return jsonify({"error": "Missing signature"}), 403

    try:
        sha_type, github_signature = signature.split('=')
        if sha_type != 'sha256':
            return jsonify({"error": "Invalid signature format"}), 403

        mac = hmac.new(GITHUB_SECRET.encode(), msg=request.data, digestmod=hashlib.sha256)
        computed_signature = mac.hexdigest()

        if not hmac.compare_digest(computed_signature, github_signature):
            return jsonify({"error": "Signature mismatch"}), 403
    except Exception:
        print("Malformed signature")
        return jsonify({"error": "Malformed signature"}), 403

    #Signature verified, now handle the webhook payload
    event_type = request.headers.get("X-GitHub-Event")
    data = request.json
    utc = pytz.UTC
    doc = {}

    if event_type == "push":
        commit = data.get("head_commit", {})
        if not commit:
            return jsonify({"error": "No commit data"}), 400

        doc = {
            "request_id": commit.get("id"),
            "author": commit.get("author", {}).get("name"),
            "action": "push",
            "from_branch": None,
            "to_branch": data.get("ref", "").split("/")[-1],
            "timestamp": datetime.strptime(
             commit.get("timestamp"), "%Y-%m-%dT%H:%M:%S%z"
             ).astimezone(pytz.UTC) if commit.get("timestamp") else None
        }

    elif event_type == "pull_request":
        pr = data.get("pull_request", {})
        if not pr:
            return jsonify({"error": "No pull_request data"}), 400

        is_merged = pr.get("merged", False)
        date_field = "merged_at" if is_merged else "created_at"

        doc = {
            "request_id": str(pr.get("id")),
            "author": pr.get("user", {}).get("login"),
            "action": "merge" if is_merged else "pull_request",
            "from_branch": pr.get("head", {}).get("ref"),
            "to_branch": pr.get("base", {}).get("ref"),
            "timestamp": utc.localize(datetime.strptime(
                pr.get(date_field), "%Y-%m-%dT%H:%M:%SZ"
            )) if pr.get(date_field) else None
        }

    #Store only complete & valid events
    if doc and doc["author"] and doc["timestamp"]:
        collection.insert_one(doc)
        return jsonify({"status": "received"}), 200

    return jsonify({"status": "ignored"}), 400


@webhook.route('/events', methods=["GET"])
def get_events():
    """
    Returns the latest GitHub events stored in MongoDB.
    Optional query param `?since=timestamp` will return only newer records.
    """
    since = request.args.get("since")
    query = {}

    if since:
        try:
            since_time = datetime.fromisoformat(since)
            query["timestamp"] = {"$gt": since_time}
        except ValueError:
            return jsonify([])  # Ignore malformed timestamp

    events = list(collection.find(query).sort("timestamp", -1).limit(10))
    formatted = []

    for event in events:
        ts = event["timestamp"].strftime("%-d %B %Y - %-I:%M %p UTC")
        action = event["action"]
        msg = ""

        if action == "push":
            msg = f'{event["author"]} pushed to {event["to_branch"]} on {ts}'
        elif action == "pull_request":
            msg = f'{event["author"]} submitted a pull request from {event["from_branch"]} to {event["to_branch"]} on {ts}'
        elif action == "merge":
            msg = f'{event["author"]} merged branch {event["from_branch"]} to {event["to_branch"]} on {ts}'

        formatted.append({
            "message": msg,
            "timestamp": event["timestamp"].isoformat()
        })

    return jsonify(formatted)


@webhook.route('/', methods=["GET"])
def index():
    """ Serves the main frontend UI """
    return render_template("index.html")