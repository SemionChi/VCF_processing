import requests
from cachetools import cached, TTLCache

# Configure the cache with a time-to-live (TTL)
cache = TTLCache(maxsize=100, ttl=3600)  # Cache up to 100 responses for 1 hour

@cached(cache)  # Decorate the function with caching
def get_variant_gene(chr, pos, ref, alt, reference_version):
    api_url = "https://test.genoox.com/api/fetch_variant_details"
    payload = {
        "chr": chr,
        "pos": pos,
        "ref": ref,
        "alt": alt,
        "reference_version": reference_version
    }

    response = requests.post(api_url, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data.get("gene", None)
    else:
        print(f"Failed to fetch variant details. Status code: {response.status_code}")
        return None



