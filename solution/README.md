# Web Server API Solution

This document provides instructions to build, run, test, and clean up the Web Server API solution. The API fetches publicly available Gists of a specified GitHub user.

---

## Prerequisites

1. **Docker**: Ensure Docker is installed and running on your machine.
2. **Python**: Required to run the test script (`test-api.py`).
3. **`jq`** (optional): A command-line JSON processor for pretty-printing API responses.

---

## Steps to Build and Run the Web Server API

### 1. Build the Docker Image
```bash
docker build -t web-server-api .
```

### 2. Run the Docker Container
```bash
docker run -d -p 8080:8080 web-server-api
```

### 3. Access the Application
Use the following command to fetch Gists for the GitHub user `octocat`:
```bash
curl http://localhost:8080/octocat | jq
```

---

## Optional: Pagination Support

If the optional app with pagination is configured (`app-optional.py`), update the `Dockerfile` to set:
```dockerfile
CMD ["python", "app-optional.py"]
```

Then build and run the container as usual. Access paginated results with:
```bash
curl "http://localhost:8080/octocat?page=1&per_page=5" | jq
```

---

## Testing the API

Run the automated test script (`test-api.py`) to validate the API:
```bash
python test-api.py
```

**Note**: The test script is written for the original app (`app.py`).

---

## Stopping and Cleaning Up

### 1. Stop the Docker Container
```bash
docker stop <container-id>
```

### 2. Remove the Docker Container
```bash
docker rm <container-id>
```

### 3. Remove the Docker Image
```bash
docker rmi web-server-api
```

---

## Additional Notes

- **Default Port**: The application runs on port `8080`. Ensure the port is available or modify the `docker run` command to map to a different port.
- **Dependencies**: All dependencies are specified in `dependencies.txt` and are installed during the Docker build process.
