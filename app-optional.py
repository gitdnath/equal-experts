from flask import Flask, jsonify, request
from flask_caching import Cache
import requests

app = Flask(__name__)

# Configure caching
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Cache timeout in seconds
cache = Cache(app)

GITHUB_API_URL = "https://api.github.com/users"

@app.route('/<user>', methods=['GET'])
def get_user_gists(user):
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    # Create a unique cache key
    cache_key = f"{user}_page_{page}_per_page_{per_page}"

    # Check if the result is already in the cache
    cached_data = cache.get(cache_key)
    if cached_data:
        return jsonify(cached_data)

    try:
        url = f"{GITHUB_API_URL}/{user}/gists"
        response = requests.get(url, params={"page": page, "per_page": per_page})
        response.raise_for_status()

        gists = response.json()
        result = {
            "page": page,
            "per_page": per_page,
            "gists": gists
        }

        # Store the result in the cache
        cache.set(cache_key, result)
        return jsonify(result)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run the server
    app.run(host='0.0.0.0', port=8080)
