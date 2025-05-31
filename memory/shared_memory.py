# import sqlite3
# from datetime import datetime
# import json

# class SharedMemory:
#     def __init__(self, db_path=":memory:"):
#         self.conn = sqlite3.connect(db_path)
#         self.cursor = self.conn.cursor()
#         self._create_table()

#     def _create_table(self):
#         self.cursor.execute("""
#             CREATE TABLE IF NOT EXISTS logs (
#                 id TEXT PRIMARY KEY,
#                 format TEXT,
#                 intent TEXT,
#                 timestamp TEXT,
#                 data TEXT
#             )
#         """)

#     # def log(self, request_id: str, format: str, intent: str, data: dict):
#     #     self.cursor.execute(
#     #         "INSERT INTO logs VALUES (?, ?, ?, ?, ?)",
#     #         (request_id, format, intent, datetime.now().isoformat(), str(data))
#     #     )
#     #     self.conn.commit()
#     def log(self, request_id, format, intent, data):
#         self.cursor.execute(
#                """
#             INSERT OR REPLACE INTO logs (id, format, intent, data, timestamp)
#             VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
#             """,
#         (request_id, format, intent, json.dumps(data))
#         )
#         self.conn.commit()



import sqlite3
from datetime import datetime
import json

class SharedMemory:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id TEXT PRIMARY KEY,
                stage TEXT,
                data TEXT,
                timestamp TEXT
            )
        """)

    def log(self, request_id, stage, data):
        self.cursor.execute(
            """
            INSERT OR REPLACE INTO logs (id, stage, data, timestamp)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            """,
            (request_id, stage, json.dumps(data))
        )
        self.conn.commit()


