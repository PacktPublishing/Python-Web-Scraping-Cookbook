import json
import requests

raw_json = requests.get("http://www.freegeoip.net/json/63.153.113.92").text
parsed = json.loads(raw_json)
print(json.dumps(parsed, indent=4, sort_keys=True))
