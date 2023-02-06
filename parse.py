# -*- coding: utf-8 -*-

import os
import googleapiclient.discovery
import csv
import pandas as pd

DEVELOPER_KEY = "AIzaSyCBRtNymwdIk1yXpLE9BqlpNkgVGZyT4fE"
VIDEO_ID = "1fgiO_yvjxI"


# Функция для скачивания корневых комментариев
def youtube(nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        pageToken=nextPageToken,
        videoId=VIDEO_ID
    )
    response = request.execute()
    return response


# Функция для скачивания реплаев на комментарии
def youtubechild(NextParentId, nextPageToken=None):
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.comments().list(
        part="id,snippet",
        maxResults=100,
        pageToken=nextPageToken,
        parentId=NextParentId
    )
    response = request.execute()
    return response


# Главная функция
def main():
    # Скачиваем комментарии
    print('download comments')
    response = youtube()
    items = response.get("items")
    nextPageToken = response.get("nextPageToken")  # скачивается порциями, на каждую следующую выдаётся указатель
    i = 1
    while nextPageToken is not None:
        print(str(i * 100))  # показываем какая сотня комментариев сейчас скачивается
        response = youtube(nextPageToken)
        nextPageToken = response.get("nextPageToken")
        items = items + response.get("items")
        if i * 100 == 10000:
            break
        i += 1

    print(f"Final count: {len(items)}")  # Отображаем количество скачаных комментариев

    # Делаем датафрейм из полученной инфы
    comments = [line.get("snippet").get("topLevelComment").get('snippet').get('textOriginal') for line in items]
    comments_df = pd.DataFrame({'comment': comments})
    comments_df.to_csv('youtuberesults.csv')
    
    print("Done")


if __name__ == "__main__":
    main()
