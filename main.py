import requests
import json
import time
import os, sys
import pytube
from feedgen.feed import FeedGenerator

from config import *

if not os.path.exists(TEMP_DIRECTORY):
	os.mkdir(TEMP_DIRECTORY)

def download_and_convert(vid):
	print 'downloading...',vid
	try:
		vid_url = "https://www.youtube.com/watch?v={}".format(vid)
		filename = "{}.mp4".format(vid)
		full_path = os.path.join(WEB_HOST_DIRECTORY, filename)
		temp_path = os.path.join(TEMP_DIRECTORY, filename)
		yt = pytube.YouTube(vid_url)
		yt.set_filename(vid)
		mp4 = yt.filter('mp4')
		print 'formats:',mp4
		if len(mp4) < 1:
			print 'no mp4 files found'
			return
		mp4[0].download(TEMP_DIRECTORY)
		print 'downloaded'
		os.system(FFMPEG_CMD.format(temp_path,full_path))
		print 'converted'
		os.remove(temp_path)
		print 'removed temp file'
	except 3:
		print 'video',vid
		print '--- download failed'


def get_latest_videos():
	print 'get videos'
	if os.path.exists(HISTORY_JSON):
		old_json = open(HISTORY_JSON,'r')
		old_vids = json.loads(old_json.read())
		print 'loaded',len(old_vids),'videos'
		old_json.close()
	else:
		print 'new video history file'
		old_vids = {}
	api_url = API_PLAYLIST_URL.format(API_KEY,ITEMS_TO_SCAN,CHANNEL_PLAYLIST_ID)
	#print 'api request:',api_url
	api_request = requests.get(api_url)
	if api_request.status_code != 200:
		raise Exception('The API gave an error code')
	videos = api_request.json()['items']
	#print videos
	for vid in videos:
		try:
			#print vid
			vid_id = vid['snippet']['resourceId']['videoId']
			vid_title = vid['snippet']['title']
			print '+++',vid_title
			vid_desc = vid['snippet']['description']
			vid_date = time.mktime(time.strptime(vid['snippet']['publishedAt'],'%Y-%m-%dT%H:%M:%S.000Z')) ## unixtime
			vid_url = "https://www.youtube.com/watch?v={}".format(vid_id)
			if not vid_id in old_vids:
				print ' not downloaded...'
				old_vids[vid_id] = {'id':vid_id,'title':vid_title,'desc':vid_desc,'time':vid_date,'url':vid_url}
				download_and_convert(vid_id)
				time.sleep(10)
		except 5:
			print 'error getting video stuff'

	print 'truncating history'
	history_date = {} # this is a weird way to truncate it
	for v in old_vids.values():
		history_date[v['time']] = v['id']
	timez = sorted(history_date.keys())[-ITEMS_TO_KEEP:]
	to_del = []
	for v in old_vids.values():
		if v['time'] < timez[0]:
			to_del.append(v['id'])
	for dv in to_del:
		print 'deleting',dv
		del old_vids[dv]

	print 'saving history'
	history_file = open(HISTORY_JSON,'w')
	history_file.write(json.dumps(old_vids))
	history_file.close()

	print 'generating feed'
	fg = FeedGenerator()
	fg.id(FG_YOUTUBE)
	fg.title(CHANNEL_NAME)
	fg.author(FG_AUTHOR)
	fg.link(href='http://www.youtube.com',rel='alternate')
	fg.subtitle('This is an automatically generated feed')
	fg.language('en')

	for vid in [old_vids.get(history_date.get(i)) for i in timez]: # supposed to put them in the right order
		vid_id = vid.get('id')
		vid_url = vid.get('url')
		vid_title = vid.get('title')
		print 'video:',vid_title
		vid_desc = vid.get('desc')
		filename = "{}.mp4".format(vid_id)
		full_path = os.path.join(WEB_HOST_DIRECTORY, filename)
		url = WEB_BASE_URL+filename
		print url
		fe = fg.add_entry()
		fe.id(url)
		fe.title(vid_title)
		fe.description(vid_desc)
		fe.enclosure(url, 0, 'audio/mpeg')

	feed_file = os.path.join(WEB_HOST_DIRECTORY, PODCAST_FILE)
	fg.rss_file(feed_file)
	print 'feed saved...'


if __name__ == '__main__':
	get_latest_videos()
	print 'long delay...'
	time.sleep(REFRESH_TIME)
