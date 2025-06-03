# 🚀 GitHub Action Webhook Tracker

This project demonstrates how to track GitHub activity (`push`, `pull_request`, and `merge` events) from one repository via webhooks, store it in a MongoDB database, and display the events in real-time on a frontend UI that polls for updates every 15 seconds.

---

## 🧩 Project Structure

### 📁 1. [`action-repo`](https://github.com/shubham3451/action-repo/)

A GitHub repository where activity triggers webhooks for events like:

* `Push`
* `Pull Request`
* `Merge` (bonus)

> These events are sent to a registered webhook endpoint.

### 📁 2. [`webhook-repo`](https://github.com/shubham3451/webhook-repo/)

A Flask-based backend that receives GitHub webhook data, processes the events, stores them in MongoDB, and serves them to the UI frontend.

---

## 🛠️ Features

* ✅ GitHub Webhook Integration
* ✅ MongoDB storage with clean schema
* ✅ Flask-based REST API to handle and serve event data
* ✅ Frontend UI that polls every 15 seconds
* ✅ Neatly formatted output for each type of GitHub event

---

## 📦 MongoDB Schema

Each event is stored with the following schema:

```json
{
  "id": 683efea2a8fw0f3u0d020475,
  "request_id" : "6014004874",
  "author": "Travis",
  "action_type": "push",  // or "pull_request", "merge"
  "from_branch": "dev",
  "to_branch": "master",
  "timestamp": "2021-04-01T12:30:00Z"
}
```

---

## 🖥️ UI Display Format

* **Push Event:**

  ```
  {author} pushed to {to_branch} on {timestamp}
  Example: "Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC
  ```

* **Pull Request Event:**

  ```
  {author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}
  Example: "Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC
  ```

* **Merge Event (Bonus):**

  ```
  {author} merged branch {from_branch} to {to_branch} on {timestamp}
  Example: "Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC
  ```

---

## 🔧 Setup Instructions

### 🔗 1. `action-repo` (GitHub Event Source)

* Clone or fork the [`action-repo`](https://github.com/shubham3451/action-repo/) repository.
* Go to **Settings > Webhooks** and add your webhook URL (e.g. `https://yourdomain.com/webhook`)
* Select events: `push`, `pull_request`, and optionally `merge` (custom implementation)

---

### 🌐 2. `webhook-repo` (Flask Backend)

* Clone the [`webhook-repo`](https://github.com/shubham3451/webhook-repo/) repository.
* Install dependencies:

  ```bash
  pip install -r requirements.txt
  ```
* Set up environment variables (Mongo URI, etc.) using a `.env` file:

  ```
  MONGO_URI=mongodb://localhost:27017/github_events
  ```
* Run the Flask server:

  ```bash
  python run.py
  ```

---

### 🧪 3. UI Client

* The UI polls `/events` endpoint every 15 seconds.
* Make sure the Flask server exposes an endpoint like:

  ```
  GET /events
  ```

---

## 🔗 Repository Links

* **Action Repo:** [🔗 GitHub - action-repo](https://github.com/shubham3451/action-repo/)
* **Webhook Repo:** [🔗 GitHub - webhook-repo](https://github.com/shubham3451/webhook-repo/)

---

## 🧑‍💻 Tech Stack

* **Python (Flask)**
* **MongoDB**
* **JavaScript / HTML / CSS** (for UI)
* **GitHub Webhooks**

---

## 📄 License

MIT License

---
