import requests
from bs4 import BeautifulSoup
import json
import re
import base64
import datetime

# https://www.megatube.xxx/get_file/11/22d672857266d62a96b2cf16f68ed004/117000/117268/117268.mp4


def dict_to_base64_string(d):
    json_str = json.dumps(d)
    b64_bytes = base64.b64encode(json_str.encode('utf-8'))
    return b64_bytes.decode('utf-8').replace("=", "")


class PervClips():
    def __init__(self):
        self.base_url = "https://www.pervclips.com/tube/"

    def all(self, category):
        category_url = f"{self.base_url}/categories/{category}/"
        url = category_url if bool(category) else f'{self.base_url}'

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.select(".items-list .item")

        videos = []
        for tag in tags:

            video_id = tag.select_one("a").attrs["data-id"]
            if video_id:
                video_url = tag.select_one("a").attrs["data-src"].replace("_preview", "")
                box_id = video_url.replace("https://cdn0.pervclips.com/contents/videos/", "").split("/")[0]
                title_id = tag.select_one("a").attrs["href"].replace( "/tube/videos/", "").replace("/", "").lower()
                source_url = f"https://www.pervclips.com{tag.select_one('a').attrs['href']}"
                title = tag.select_one(".title").getText().strip()
                thumb = tag.select_one("a").attrs["data-poster"]
                
                id = [box_id, "706f726e", video_id] # [box_id, source_id, video_id]
                hash = dict_to_base64_string(id)

            data = {
                "id": hash,
                "video_url": video_url,
                "source_url": source_url,
                "box_id": box_id,
                "thumb": thumb,
                "title": title,
                "title_id": title_id
            }
            videos.append(data)

        return videos

    def one(self, box_id, video_id, title_id):
        url = f'{self.base_url}videos/{title_id}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        match = re.search(r'flashvars\s*=\s*{([^}]*)}', response.text)
        
        if match:
            flashvars = match.group(1)
            
            data = flashvars.replace("\t", "")
            data = re.sub(r'\s+', '', data)
            data = json.dumps(data).replace("\"", "")
            
            string_list = data.split("',")
            
            video = {
                "title_id": title_id,
                "box_id": box_id,
                "title": title_id.replace("-", " ").title(),
                "source_url": url,
                "thumb": f"https://cdn.pervclips.com/tube/contents/videos_screenshots/{box_id}/{video_id}/preview.jpg",
            }
            #  https://cdn.pervclips.com/tube/contents/videos_screenshots/1063891000/1063891606/preview.jpg
            for i in range(len(string_list)):
                key_and_value = None

                if string_list[i].split(':')[0].strip() != "video_url":
                    key_and_value = string_list[i].split(":")
                    
                else:
                    key_and_value = string_list[i].split(":'")
                    video["video_url"] = key_and_value[1][:-1]


                key = key_and_value[0].strip()
                value = key_and_value[1].strip()

                if key == "video_id":
                    video[key] = value.replace("'", "")

                elif key == "video_tags":
                    video["keywords"] = [item for item in value.replace("'", "").lower().split(",") if item != ""]
               
        return video


pervclips = PervClips()
# all = pornicom.all("anal")
one = pervclips.one("1063934000", "1063934148", "charming-lady-gets-ass-licked-and-fucked-by-bbc-stud")


# print(json.dumps(all, indent=4))
print(json.dumps(one, indent=4))
