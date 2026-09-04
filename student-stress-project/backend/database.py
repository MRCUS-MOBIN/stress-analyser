import os
import json
from datetime import datetime

# Optional PyMongo import
try:
    import pymongo
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

DB_FILE = os.path.join(os.path.dirname(__file__), "storage_db.json")

class EmbeddedDatabase:
    """
    Fallback high-performance embedded JSON document storage engine.
    Ensures complete functionality out-of-the-box even when a local MongoDB server is offline.
    """
    def __init__(self, filepath=DB_FILE):
        self.filepath = filepath
        self._ensure_storage()

    def _ensure_storage(self):
        if not os.path.exists(self.filepath):
            initial_data = {
                "students": [],
                "assessments": [],
                "stress_profiles": [],
                "recovery_logs": [],
                "effectiveness_profiles": {}
            }
            with open(self.filepath, "w") as f:
                json.dump(initial_data, f, indent=2)

    def _load(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except Exception:
            return {"students": [], "assessments": [], "stress_profiles": [], "recovery_logs": [], "effectiveness_profiles": {}}

    def _save(self, data):
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def insert_one(self, collection_name, document):
        data = self._load()
        if collection_name not in data:
            data[collection_name] = []
        if "_id" not in document:
            document["_id"] = f"{collection_name}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        document["created_at"] = datetime.now().isoformat()
        data[collection_name].append(document)
        self._save(data)
        return document["_id"]

    def find(self, collection_name, query=None, limit=100):
        data = self._load()
        items = data.get(collection_name, [])
        if not query:
            return items[-limit:]
        
        filtered = []
        for doc in items:
            match = True
            for k, v in query.items():
                if doc.get(k) != v:
                    match = False
                    break
            if match:
                filtered.append(doc)
        return filtered[-limit:]

    def find_one(self, collection_name, query):
        results = self.find(collection_name, query, limit=1)
        return results[0] if results else None

class DatabaseManager:
    def __init__(self):
        self.mode = "embedded"
        self.client = None
        self.db = None
        self.embedded = EmbeddedDatabase()
        
        # Try MongoDB connection if pymongo is installed
        if HAS_PYMONGO:
            try:
                mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
                self.client = pymongo.MongoClient(mongo_uri, serverSelectionTimeoutMS=1000)
                # Quick test ping
                self.client.admin.command('ping')
                self.db = self.client["student_stress_db"]
                self.mode = "mongodb"
                print("Connected successfully to local MongoDB instance!")
            except Exception:
                self.mode = "embedded"
                print("MongoDB server not reachable. Utilizing high-reliability Embedded DB engine.")

    def get_db(self):
        if self.mode == "mongodb" and self.db is not None:
            return self.db
        return self.embedded

db_manager = DatabaseManager()

def get_database():
    return db_manager.get_db()
