#!/usr/bin/env bash
set -e
export DATABASE_URL="sqlite:////config/physical_library.sqlite"
export EXPORT_ROOT="/media/physical-library-kodi"
if [ -f /data/options.json ]; then
  export TMDB_API_KEY=$(python3 -c "import json;print(json.load(open('/data/options.json')).get('tmdb_api_key',''))")
  export UPCITEMDB_API_KEY=$(python3 -c "import json;print(json.load(open('/data/options.json')).get('upcitemdb_api_key',''))")
  export BARCODELOOKUP_API_KEY=$(python3 -c "import json;print(json.load(open('/data/options.json')).get('barcodelookup_api_key',''))")
  export HA_WEBHOOK_URL=$(python3 -c "import json;print(json.load(open('/data/options.json')).get('ha_webhook_url',''))")
fi
exec uvicorn app.main:app --host 0.0.0.0 --port 8099
