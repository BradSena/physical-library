import sys, urllib.parse, json
import xbmcgui, xbmcaddon
try:
    import urllib.request as request
except ImportError:
    import urllib2 as request

addon = xbmcaddon.Addon()
backend = addon.getSetting('backend_url') or 'http://homeassistant.local:8099'
params = dict(urllib.parse.parse_qsl(sys.argv[2][1:])) if len(sys.argv) > 2 else {}
movie_id = params.get('movie_id')
if movie_id:
    try:
        with request.urlopen(f'{backend}/api/kodi/play/{movie_id}', timeout=5) as r:
            data = json.loads(r.read().decode('utf-8'))
    except Exception as e:
        xbmcgui.Dialog().ok('Physical Disc', f'Erreur backend: {e}')
        raise SystemExit
    msg = f"{data.get('message','Insérer le disque')}\n\nSupport : {data.get('support')}\nEmplacement : {data.get('original_location')}"
    if data.get('status') != 'stock':
        msg += f"\nStatut : {data.get('status')}"
        if data.get('holder'):
            msg += f" chez {data.get('holder')}"
    xbmcgui.Dialog().ok('Physical Disc', msg)
else:
    xbmcgui.Dialog().ok('Physical Disc', 'Aucun film demandé')
