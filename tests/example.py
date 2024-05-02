import requests
from pathlib import Path

# Define the API endpoint URL (change localhost and port if needed)
url = "http://127.0.0.1:5000/api/file"

# Define the data you want to send (example data)
data = {
    "group_id": "exampleGroup123",
    "file_path": str(Path("path/to/file2.txt")),
    "md5": "e41d8cd98f00b204e9800998ecf8427e",  # An example MD5 hash
}

# Send a POST request
response = requests.post(url, json=data)

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.json()}")
