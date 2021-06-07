import os
import googleapiclient.discovery
import json
def youtube_comments(url):
    myapi = 'AIzaSyDnaMpaPAvgJfhbrTszGlA2tE8fVAKBN8c'
    splitting = url.split('v=')
    id = splitting[1]
    print(id)
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = myapi
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    request = youtube.commentThreads().list(
        part="replies",
        order="relevance",
        videoId=id
    )
    response = request.execute()
    print(json.dumps(response, indent=4))#['items'][5]["replies"]["comments"][0]["snippet"]["textOriginal"]
    # print(response['items'])#['items'][5]["replies"]["comments"][0]["snippet"]["textOriginal"]
    for i in response['items']:
        try:
            if i["replies"]:
                for x in i["replies"]["comments"]:
                    print(x["snippet"]["textDisplay"])
                    print(x["snippet"]["textOriginal"])
        except:
            continue
# if __name__ == "__main__":
#     main()
# main driver
if __name__ == "__main__":
    youtube_comments('https://www.youtube.com/watch?v=B7G5B8P8k9s')
    # Y.get_subscriber_count()
    # Y.get_channel_videos()
    # Y.save_desc()
    print("\n\n ++++++++++++ All done ++++++++++++++")