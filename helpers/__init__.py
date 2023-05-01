import requests
from bs4 import BeautifulSoup
import json
import re
import base64

def dict_to_base64_string(d):
    json_str = json.dumps(d)
    b64_bytes = base64.b64encode(json_str.encode('utf-8'))
    return b64_bytes.decode('utf-8').replace("=", "")

# sources
SOURCES = {
    "62756C65": "xxxbule",
    "76696B69": "vikiporn",
    "7768697465": "pornwhite",
}

######################### $$$$$$$$$$$$$$###########################
# http://xxxbule.com
##################################################################
def fetch_xxxbule(query):
    url = f"http://www.xxxbule.com/"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tags = soup.select(".style47")

    videos = []
    for tag in tags:
        tag.select(".style49")

        video_id = tag.attrs.get("data-id")

        if video_id:
            title = BeautifulSoup(tag.__str__(), "html.parser").select_one(".style49").text
            src = f"http://www.xxxbule.com/videos/{video_id}/{title.replace(' ', '-').lower()}.mp4"
            thumb = "http://www.xxxbule.com" + BeautifulSoup(tag.__str__(), "html.parser").find("img")["src"]

            # id = [box_id, source_id, video_id]
            id = ["False",  '62756C65', video_id]
            hash = dict_to_base64_string(id)

            data = {
                "id": hash,
                "source_url": "www.xxxbule.com",
                "thumb": thumb,
                "title": title,
                "title_id": title.replace(" ", "-").lower(),
                "source_url": f"https://www.xxxbule.com/sex-clips/{title}".replace(" ", "-").lower(),
                "video_url": src,
                # "box_id": video_id,
                # "source_id": "62756C65",
                # "video_id": video_id,
            }

            videos.append(data)

    return videos

def fetch_xxxbule_single_video(video_id):
    url = f"http://www.xxxbule.com/sex-clips/{video_id}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tag = soup.select_one("script")
    data = json.loads(tag.getText())

    if ("contentUrl" in data and "thumbnailUrl" in data and "description" in data and "keywords" in data):
        video = {
            "source": "www.xxxbule.com",
            "video_url": data["contentUrl"],
            "description": data["description"],
            "thumb": data["thumbnailUrl"],
            "keywords": str(data["keywords"]).split(","),
        }
        return video
    else:
        return False


##################################################################
# http://vikiporn.com
##################################################################
def fetch_vikiporn(query):
    # Make a GET request to the webpage
    url = f'https://www.vikiporn.com/latest-updates/'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    tags = soup.select(".thumbs-list .thumb")
    videos = []

    for tag in tags:
        video = tag.select_one(".img")
        info = tag.select_one(".info-inner")
        url = tag.select_one("a")["href"]
        box_id = video["data-src"].replace("https://cdn.vikiporn.com/contents/videos/","").replace("_preview.mp4", "").split("/")[0]
        title = info.select_one("h3").getText()
        video_id = video["data-id"]
        
        # id = [box_id, source_id, video_id]
        id = [box_id,  '76696B69', video_id]
        hash = dict_to_base64_string(id)

        data = {
            "id": hash,
            "source_url": "www.vikiporn.com",
            "source_url": url,
            "video_url": video["data-src"].replace("_preview", ""),
            "thumb": video["data-poster"],
            "title": title,
            "title_id": title.replace(" ", "-").lower()
            # "source_id": "76696B69",
            # "video_id": video["data-id"],
            # "box_id": box_id,
        }
        videos.append(data)
    return videos

def fetch_vikiporn_single_video(box_id, video_id, title_id):
    url = f'https://www.vikiporn.com/videos/{video_id}/{title_id}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.select(".player meta")

    video = {
        "box_id": box_id,
        "video_id": video_id,
        "title_id": title_id,
        "video_url": f"https://cdn.vikiporn.com/contents/videos/{box_id}/{video_id}/{video_id}.mp4"
    }

    for tag in tags:
        if (tag["itemprop"] == "description" or tag["itemprop"] == "thumbnailUrl") or tag["itemprop"] == "name" or tag["itemprop"] == "keywords":
            if tag["itemprop"] == "keywords":
                video["keywords"] = tag["content"].split(", ")

            elif tag["itemprop"] == "thumbnailUrl":
                video["thumb"] = tag["content"]

            elif tag["itemprop"] == "url":
                video["source_url"] = tag["content"]

            else:
                video[tag["itemprop"]] = tag["content"]

    return video


##################################################################
# www.pornwhite.com
##################################################################
def fetch_pornwhite(category):
    url_with_category = f"https://www.pornwhite.com/category/{category}"
    url_feed = f"https://www.pornwhite.com/latest-updates/"
    url = url_with_category if bool(category) else url_feed

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tags = soup.select(".thumbs-list .thumb")

    videos = []
    for tag in tags:
        url = tag.find("a")["href"]
        thumb = tag.select_one(".img")["data-poster"]
        title = tag.select_one(".info-inner h3").getText()
        box_id = tag.select_one(".img")["data-src"].replace("https://cdn.pornwhite.com/contents/videos/", "").replace("_preview.mp4", "").split("/")[0]
        video_id = tag.select_one(".img")["data-src"].replace("https://cdn.pornwhite.com/contents/videos/", "").replace("_preview.mp4", "").split("/")[-1]
        video_url = tag.select_one(".img")["data-src"].replace("_preview", "")
        title_id = re.sub(r'[^A-Za-z0-9-]+', '', url.replace(f"https://www.pornwhite.com/videos/", "").split("/")[1])
        video = {"source_id": "7768697465"}
        
        id = [box_id, '7768697465', video_id]
        hash = dict_to_base64_string(id)

        if video_url:
            video = {
                "id": hash,
                "thumb": thumb,
                "title": title,
                "title_id": title_id,
                "video_url": video_url,
                "source_url": url,
                "video_id": video_id,
                "source_id": "7768697465",
                "box_id": box_id,
            }
            videos.append(video)
    return videos

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
        
        if bool(video["video_url"]):
            return video
        return False
