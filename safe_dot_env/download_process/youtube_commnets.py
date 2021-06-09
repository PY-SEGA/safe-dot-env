import os
import googleapiclient.discovery
import json
def youtube_comments(url):
    myapi = 'AIzaSyDGfngFMxQiVAweRw7ae4BqM_cgDEZBSmo'
    splitting = url.split('v=')
    id_not_complete = splitting[1]
    splitting2 = id_not_complete.split('&')
    id = splitting2[0]
    print(id, 'yhis is the id hhh')
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = myapi
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)
    try:
        request = youtube.commentThreads().list(
            part="replies",
            order="relevance",
            maxResults=100,
            videoId=id
        )
        response = request.execute()
    except:
         return "no comments"
    # print(json.dumps(response, indent=4))#['items'][5]["replies"]["comments"][0]["snippet"]["textOriginal"]
    # print(response['items'])#['items'][5]["replies"]["comments"][0]["snippet"]["textOriginal"]
    comments_list = []
    
    for i in response['items']:
        try:
            if i["replies"]:
                for x in i["replies"]["comments"]:
                    comments_list.append(x["snippet"]["textDisplay"])
                    print(x["snippet"]["textDisplay"])

        except:
           continue
    return comments_list
# if __name__ == "__main__":
#     main()
# main driver
if __name__ == "__main__":
    # youtube_comments('https://www.youtube.com/watch?v=7rTLkHZAYuk')
    # Y.get_subscriber_count()
    # Y.get_channel_videos()
    # Y.save_desc()
    print("\n\n ++++++++++++ All done ++++++++++++++")
    # youtube_comments('https://www.youtube.com/watch?v=sxGKgndSfCE&ab_channel=OneMorePleaseOneMorePlease')