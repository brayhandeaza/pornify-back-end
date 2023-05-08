import requests
from bs4 import BeautifulSoup
import json
import re
import base64
import datetime


def dict_to_base64_string(d):
    json_str = json.dumps(d)
    b64_bytes = base64.b64encode(json_str.encode('utf-8'))
    return b64_bytes.decode('utf-8').replace("=", "")


def format_duration(duration_str):
    hours = 0
    minutes = 0
    seconds = 0

    if 'H' in duration_str:
        hours = int(duration_str.split('T')[-1].split('H')[0])
        duration_str = duration_str.split('H')[-1]

    if 'M' in duration_str:
        if 'H' in duration_str:
            minutes = int(duration_str.split('H')[-1].split('M')[0])
            duration_str = duration_str.split('M')[-1]
        else:
            minutes = int(duration_str.split('T')[-1].split('M')[0])
            duration_str = duration_str.split('M')[-1]

    if 'S' in duration_str:
        if 'M' in duration_str:
            seconds = int(duration_str.split('M')[-1].split('S')[0])
        elif 'H' in duration_str:
            seconds = int(duration_str.split('H')[-1].split('S')[0])
        else:
            seconds = int(duration_str.split('T')[-1].split('S')[0])

    time = datetime.timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    )

    duration = str(time).split(":")
    if duration[0] == "0":
        return str(time)[2:]
    else:
        return str(time)


# sources
SOURCES = {
    "62756C65": "xxxbule",
    "76696B69": "vikiporn",
    "706f726e": "pornicom",
    "70657276": "pervclips",
    "7768697465": "pornwhite",
}

CATEGORIES = [
    'girlfriend', 'reality', 'compilation', 'big ass', '18+', 'latina', 'shemale / tranny', 'saggy tits', 'fisting', 'stockings', 'nudist', 'bisexual', 'japanese', 'blowjob', 'rimming', 'cumshot', 'shaved', 'threesome', 'big tits', 'masturbation', 'brunette', 'fully clothed sex', 'squirting', 'hidden camera', 'coed', 'retro', 'playboy', 'hd', 'pornstar', 'mature', '3d', 'celebrity', 'kissing', 'babe', 'massage', 'big cock', 'pantyhose', 'cuckold', 'american', 'milf', 'hentai', 'babysitter', 'teen', 'bdsm', 'lesbian', 'skinny', 'cfnm', 'amateur', 'fetish', 'masturbating', 'interracial', 'creampie', 'domination', 'stepmom', 'pov', 'solo', 'european', 'voyeur', 'indian', 'anime', 'lingerie', 'anal', 'double penetration', 'bbw', 'small tits', 'orgasm', 'gf', 'midget', 'orgy', 'outdoors', 'busty', 'old and young', 'wife', 'beach', 'bukkake', 'outdoor', 'solo girl', 'foot', 'cumshots', 'fantasy', 'humiliation', 'dad', 'shemale', 'rough sex', 'camel toe hoes', 'black hair', 'gangbang', 'german', 'petite', 'granny', 'tight pussy', 'cartoon', 'doctor', 'asian', 'hardcore', 'big dick', 'gay', 'mom', 'hairy', 'pissing', 'blonde', 'beautiful', 'group sex', 'cum swallowing', 'black', 'dp', 'taboo', 'ebony', 'teen (18+)', 'homemade', 'redhead', 'step fantasy', 'gonzo', 'vintage', 'french', 'casting', 'tranny', 'bikini', 'ass', '18 year old', 'handjob', 'toys'
]

class XxxBule():
    def __init__(self):
        self.base_url = "https://www.xxxbule.com"

    def all(self, search, search_type=""):
        url = None

        if search_type == "search":
            url = f"{self.base_url}/search/?q={search}/"
        elif search_type == "category":
            url = f"{self.base_url}/streams/{search}-freeporn/"
        else:
            url = f"{self.base_url}/latest-updates/"

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.select(".style47")

        videos = []
        for tag in tags:

            video_id = tag.attrs.get("data-id")
            if video_id:
                title = BeautifulSoup(
                    tag.__str__(), "html.parser").select_one(".style49").text
                src = f"{self.base_url}videos/{video_id}/{title.replace(' ', '-').lower()}.mp4"
                thumb = f"{self.base_url}" + \
                    BeautifulSoup(tag.__str__(), "html.parser").find(
                        "img")["src"]

                # id = [box_id, source_id, video_id]
                id = ["False",  '62756C65', video_id]
                hash = dict_to_base64_string(id)

                data = {
                    "id": hash,
                    "thumb": thumb,
                    "title": title,
                    "title_id": title.replace(" ", "-").lower(),
                    "source_url": f"{self.base_url}sex-clips/{title}".replace(" ", "-").lower(),
                    "video_url": src
                }

                videos.append(data)

        return videos

    def one(self, video_id):
        url = f"{self.base_url}sex-clips/{video_id}"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tag = soup.select_one("script")
        data = json.loads(tag.getText())

        if ("contentUrl" in data and "thumbnailUrl" in data and "keywords" in data):
            video = {
                "source": "www.xxxbule.com",
                "video_url": data["contentUrl"],
                "thumb": data["thumbnailUrl"],
                "keywords": str(data["keywords"]).split(","),
            }
            return video

        return False


class VikiPorn():
    def __init__(self):
        self.base_url = "https://www.vikiporn.com/"

    def all(self, search, search_type=""):
        url = None

        if search_type == "search":
            url = f"{self.base_url}/search/?q={search}/"
        elif search_type == "category":
            url = f"{self.base_url}/categories/{search}/"
        else:
            url = f"{self.base_url}latest-updates/"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        tags = soup.select(".thumbs-list .thumb")
        videos = []

        for tag in tags:
            video = tag.select_one(".img")
            info = tag.select_one(".info-inner")
            url = tag.select_one("a")["href"]
            box_id = video["data-src"].replace("https://cdn.vikiporn.com/contents/videos/",
                                               "").replace("_preview.mp4", "").split("/")[0]
            title = info.select_one("h3").getText()
            video_id = video["data-id"]

            # id = [box_id, source_id, video_id]
            id = [box_id,  '76696B69', video_id]
            hash = dict_to_base64_string(id)

            data = {
                "id": hash,
                "source_url": url,
                "video_url": video["data-src"].replace("_preview", ""),
                "thumb": video["data-poster"],
                "title": title,
                "title_id": title.replace(" ", "-").lower()
            }
            videos.append(data)
        return videos

    def one(self, box_id, video_id, title_id):
        url = f'{self.base_url}videos/{video_id}/{title_id}/'
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
            if (tag["itemprop"] == "description" or tag["itemprop"] == "duration" or tag["itemprop"] == "thumbnailUrl") or tag["itemprop"] == "name" or tag["itemprop"] == "keywords":
                if tag["itemprop"] == "keywords":
                    video["keywords"] = tag["content"].split(", ")

                elif tag["itemprop"] == "thumbnailUrl":
                    video["thumb"] = tag["content"]

                elif tag["itemprop"] == "url":
                    video["source_url"] = tag["content"]

                else:
                    video[tag["itemprop"]] = tag["content"]

        return video


class PornWhite():
    def __init__(self):
        self.base_url = "https://www.pornwhite.com/"

    def all(self, search, search_type=""):
        url = None

        if search_type == "search":
            url = f"{self.base_url}/search/?q={search}/"
        elif search_type == "category":
            url = f"{self.base_url}/categories/{search}/"
        else:
            url = f"{self.base_url}latest-updates/"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = soup.select(".thumbs-list .thumb")

        videos = []
        for tag in tags:
            url = tag.find("a")["href"]
            thumb = tag.select_one(".img")["data-poster"]
            title = tag.select_one(".info-inner h3").getText()
            box_id = tag.select_one(".img")["data-src"].replace(
                "https://cdn.pornwhite.com/contents/videos/", "").replace("_preview.mp4", "").split("/")[0]
            video_id = tag.select_one(".img")["data-src"].replace(
                "https://cdn.pornwhite.com/contents/videos/", "").replace("_preview.mp4", "").split("/")[-1]
            video_url = tag.select_one(
                ".img")["data-src"].replace("_preview", "")
            title_id = re.sub(
                r'[^A-Za-z0-9-]+', '', url.replace(f"{self.base_url}videos/", "").split("/")[1])
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

    def one(self, box_id, video_id, title_id):
        url = f"{self.base_url}videos/{video_id}/{title_id}/"
        response = requests.get(url)
        match = re.search(r'flashvars\s*=\s*{([^}]*)}', response.text)

        if match:
            flashvars = match.group(1)

            data = flashvars.replace("\t", "")
            data = re.sub(r'\s+', '', data)
            data = json.dumps(data).replace("\"", "")

            string_list = data.split("',")

            video = {
                "video_url": f"https://cdn.pornwhite.com/contents/videos/{box_id}/{video_id}/{video_id}.mp4",
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
                    # video["video_url"] = key_and_value[1][:-1]

                key = key_and_value[0].strip()
                value = key_and_value[1].strip()

                if key == "video_id":
                    video[key] = value.replace("'", "")

                elif key == "video_tags":
                    video["keywords"] = value.replace(
                        "'", "").lower().split(",")

            if bool(video["video_url"]):
                return video
            return False


class Pornicom():
    def __init__(self):
        self.base_url = "https://www.pornicom.com/"

    def all(self, search, search_type=""):
        url = None

        if search_type == "search":
            url = f"{self.base_url}/search/?q={search}/"
        elif search_type == "category":
            url = f"{self.base_url}/categories/{search}/"
        else:
            url = self.base_url

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.select(".items-list .item")

        videos = []
        for tag in tags:
            video_id = tag.select_one(".img-holder").attrs['data-id']
            if video_id:
                title = tag.select_one(".thumb").attrs["alt"]
                video_url = tag.select_one(
                    ".img-holder").attrs['data-src'].replace("_preview", "")
                source_url = tag.select_one("a").attrs['href']
                box_id = video_url.replace(
                    "https://cdn.pornicom.com/storage/contents/videos/", "").split("/")[0]
                thumb = f"https://cdni.pornicom.com/contents/videos_screenshots/{box_id}/{video_id}/390x293/3.jpg"

            # id = [box_id, source_id, video_id]
            id = [box_id, "706f726e", video_id]
            hash = dict_to_base64_string(id)

            data = {
                "id": hash,
                "box_id": box_id,
                "thumb": thumb,
                "title": title,
                "title_id": source_url.replace(f"https://www.pornicom.com/videos/{video_id}/", "").replace("/", "").lower(),
                "source_url": source_url,
                "video_url": video_url
            }

            videos.append(data)

        return videos

    def one(self, box_id, video_id, title_id):
        url = f'{self.base_url}videos/{video_id}/{title_id}/'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        tags = soup.select(".player meta")

        video = {
            "box_id": box_id,
            "video_id": video_id,
            "title_id": title_id,
            "video_url": f"https://cdn.pornicom.com/storage/contents/videos/{box_id}/{video_id}/{video_id}.mp4"
        }

        for tag in tags:
            if (tag["itemprop"] == "duration" or tag["itemprop"] == "thumbnailUrl") or tag["itemprop"] == "name" or tag["itemprop"] == "keywords":
                if tag["itemprop"] == "keywords":
                    video["keywords"] = [
                        item for item in tag["content"].split(", ") if item != ""]

                elif tag["itemprop"] == "thumbnailUrl":
                    video["thumb"] = tag["content"]

                elif tag["itemprop"] == "url":
                    video["source_url"] = tag["content"]

                elif tag["itemprop"] == "name":
                    video["title"] = tag["content"]

                else:
                    video[tag["itemprop"]] = tag["content"]

        if bool(video["video_url"]):
            return video
        return False


class PervClips():
    def __init__(self):
        self.base_url = "https://www.pervclips.com/tube/"

    def all(self, search, search_type=""):
        url = None

        if search_type == "search":
            url = f"{self.base_url}/search/?q={search}/"
        elif search_type == "category":
            url = f"{self.base_url}/categories/{search}/"
        else:
            url = self.base_url

        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.select(".items-list .item")

        videos = []
        for tag in tags:

            video_id = tag.select_one("a").attrs["data-id"]
            if video_id:
                video_url = tag.select_one(
                    "a").attrs["data-src"].replace("_preview", "")
                box_id = video_url.replace(
                    "https://cdn0.pervclips.com/contents/videos/", "").split("/")[0]
                title_id = tag.select_one("a").attrs["href"].replace(
                    "/tube/videos/", "").replace("/", "").lower()
                source_url = f"https://www.pervclips.com{tag.select_one('a').attrs['href']}"
                title = tag.select_one(".title").getText().strip()
                thumb = tag.select_one("a").attrs["data-poster"]

                # [box_id, source_id, video_id]
                id = [box_id, "70657276", video_id]
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

            for i in range(len(string_list)):
                key_and_value = None

                if string_list[i].split(':')[0].strip() != "video_url":
                    key_and_value = string_list[i].split(":")

                else:
                    key_and_value = string_list[i].split(":'")
                    video["video_url"] = f"https://cdn0.pervclips.com/contents/videos/{box_id}/{video_id}/{video_id}.mp4"
                    # video["video_url"] = key_and_value[1][:-1]

                key = key_and_value[0].strip()
                value = key_and_value[1].strip()

                if key == "video_id":
                    video[key] = value.replace("'", "")

                elif key == "video_tags":
                    video["keywords"] = [item for item in value.replace(
                        "'", "").lower().split(",") if item != ""]

        return video


pervclips = PervClips()
xxxbule = XxxBule()
vikiporn = VikiPorn()
pornwhite = PornWhite()
pornicom = Pornicom()
