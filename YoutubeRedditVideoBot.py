
# Reddit video bot v1.0
# by Frank Gabršek|u/FrankieManta|The Frenkenator
#
# Partially based on Youtube_Poster v2.0 by /u/EDGYALLCAPSUSERNAME



# Import modules for script
import time
import praw
from apiclient.discovery import build
import datetime
import html

print('import finished...')


# YouTube Data API credentials
DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

# Post variables
CHANNEL_ID = ''
DESIRED_FLAIR_TEXT = 'Official'
print('variables finished...')


# the youtube_search function used the YouTube API to search
# for the lastest video and return the title, url, uploader
# and upload-date in a list
# -- Code from Youtube_Poster v2.0 by /u/EDGYALLCAPSUSERNAME
def youtube_search(channel_ID):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    search_response = youtube.search().list(
                        channelId=channel_ID,
                        order='date',
                        part='id, snippet',
                        maxResults=1,
                        type='video').execute()

    video = []
    for search_result in search_response.get('items', []):
        video.append([search_result['snippet']['title'],
                       search_result['id']['videoId'],
                       search_result['snippet']['channelTitle'],
                       search_result['snippet']['publishedAt']])

    return video


# the submit_post function submits the post to reddit by first
# setting up the OAuth via praw using the bot account's login credentials,
# then using that to post the link.
# It then calls the flair_post function.
# In case of an erorr, it prints the error message and continues
def submit_post(data_entries):
  did_submit = False

  r = praw.Reddit(client_id='',
                  client_secret='',
                  user_agent='',
                  username='',
                  password='')

  title = html.unescape(data_entries[0])
  link = 'https://www.youtube.com/watch?v={}'.format(data_entries[1])

  try:
    print('Submitting {}...'.format(title))
    submission = r.subreddit('ThatMadCat').submit(title, url=link, resubmit=False)
    print('Submission: {} succesfully posted, continuing...'.format(title))
    did_submit = True

  except Exception as e:
    print('error: ' + str(e))
    did_submit = False

  if did_submit:
    try:
      flair_post(submission)
      print('Submission succesfully flaired with {} flair, continuing...'.format(DESIRED_FLAIR_TEXT))

    except Exception as e:
      print('error' + str(e))


# The flair_post function searches fot the available flair templates
# and then looks for the flair template id corresponding to flair
# with 'Official' as its text. It than adds this flair to the post
def flair_post(subm):
  flairs_available = subm.flair.choices()

  for flairs in flairs_available:
    if flairs['flair_text'] == DESIRED_FLAIR_TEXT:
      print(flairs)
      subm.flair.select(flairs['flair_template_id'])


# The main function calls youtube_search to find the latest video,
# then calls submit_post to post the video.
# The function is in a constant loop and waits 300 seconds / 5 minutes
# at the end of each cycle before it starts another cycle.
# When a cycle finishes, it prints out the current date and time.
def main():
  while True:
    videodata = []

    video_search_result = youtube_search(CHANNEL_ID)
    [videodata.append(data) for data in video_search_result]
    print('search finished...')

    for data_entries in videodata:
      print(data_entries)

    for data_entries in videodata:
      submit_post(data_entries)

    print('cycle completed at {}, sleeping...'.format(datetime.datetime.now()))
    time.sleep(300)

main()