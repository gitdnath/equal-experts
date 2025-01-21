from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Base URL for GitHub API
GITHUB_API_BASE_URL = "https://api.github.com/users"

@app.route('/<username>', methods=['GET'])
def get_user_gists(username):
    """
    Fetch and return the list of publicly available gists for the specified GitHub user.
    """
    url = f"{GITHUB_API_BASE_URL}/{username}/gists"
    try:
        # Make a GET request to GitHub API
        response = requests.get(url)

        # Check if the response is successful
        if response.status_code == 200:
            gists = response.json()

            # Extract minimal gist details (e.g., ID and URL)
            gist_list = [
                {
                    "id": gist.get("id"),
                    "description": gist.get("description", "No description provided"),
                    "url": gist.get("html_url")
                }
                for gist in gists
            ]

            return jsonify({"username": username, "gists": gist_list}), 200
        elif response.status_code == 404:
            return jsonify({"error": "User not found"}), 404
        else:
            return jsonify({"error": "Failed to fetch gists from GitHub"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=8080)
