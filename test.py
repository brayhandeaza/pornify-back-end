import re
import requests
import json


def fetch_pornwhite_single_video(video_id, title_id, box_id):
    url = f"https://www.pornwhite.com/videos/{video_id}/{title_id}/"
    response = requests.get(url)
    match = re.search(r'flashvars\s*=\s*{([^}]*)}', response.text)

    if match:
        flashvars = match.group(1)

        data = flashvars.replace("\t", "")
        data = re.sub(r'\s+', '', data)
        data = json.dumps(data).replace("\"", "")

        string_list = data.split("',")

        video = {
            "title_id": title_id,
            "title": title_id.replace("-", " ").title(),
            "source_url": url,
            "thumb": f"https://cdni.pornwhite.com/contents/videos_screenshots/{box_id}/{video_id}/{video_id}/3.jpg?ver=3",
        }
        for i in range(len(string_list)):
            key_and_value = None

            if string_list[i].split(':')[0].strip() != "video_url":
                key_and_value = string_list[i].split(":")
            else:
                key_and_value = string_list[i].split(":'")
                video["video_url"] = key_and_value[1]
                print(key_and_value)

            key = key_and_value[0].strip()
            value = key_and_value[1].strip()
      

            if key == "video_id":
                video[key] = value.replace("'", "")
                
            elif key == "video_tags":
                video["keywords"] = value.replace("'", "").lower().split(",")

        print(json.dumps(video, indent=4))


video_id = "3109027"
title_id = "milfaf-milf-wendy-raine-got-sprayed-with-jizz"
box_id = "3109000",

fetch_pornwhite_single_video(video_id, title_id, box_id)
