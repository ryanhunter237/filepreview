import requests
from pathlib import Path

response = requests.post(
    url="http://127.0.0.1:5000/api/file",
    json={
        "group_id": "exampleGroup123",
        "file_path": "path/to/file2.txt",
        "md5": "abc123",
    },
)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json()}")

response = requests.post(
    url="http://127.0.0.1:5000/api/file-data",
    json={"md5": "abc123", "num_bytes": 124124, "local_path": ""},
)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json()}")

response = requests.post(
    url="http://127.0.0.1:5000/api/thumbnail",
    json={
        "md5": "abc123",
        "order": 0,
        "path": r"C:\Users\ryanh\Documents\cad\data\office-chair\office chair26202301.jpg",
    },
)
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json()}")
