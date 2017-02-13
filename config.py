### channel configuration

CHANNEL_NAME = 'ThreatWire'
CHANNEL_PLAYLIST_ID = 'PLW5y1tjAOzI0Sx4UU2fncEwQ9BQLr5Vlu'
ITEMS_TO_SCAN = 5

FG_YOUTUBE = 'https://www.youtube.com/channel/UC3s0BtrBJpwNDaflRSoiieQ' # channel link
FG_AUTHOR = {'name':'Shannon Morse','email':'shannon@hak5.org'}

### data storage and history

ITEMS_TO_KEEP = 25
HISTORY_JSON = 'history.json'
PODCAST_FILE = 'podcast.rss'

### web hosting

WEB_HOST_DIRECTORY = '/var/www/html/ytp'
WEB_BASE_URL = 'http://10.0.1.25/ytp/'

### api stuff

API_KEY = 'insert your api key here so you won’t get rate-limited'
API_PLAYLIST_URL = 'https://www.googleapis.com/youtube/v3/playlistItems?key={}&part=snippet&contentDetails&status&maxResults={}&playlistId={}'

### other config items

REFRESH_TIME = 7200  # in seconds, this is 2 hours


FFMPEG_CMD = 'ffmpeg -i {} -b:a 192K -vn {}'
TEMP_DIRECTORY = '/tmp/yt-podcast/'
