import requests
from flask import jsonify, request, Blueprint
import json
from helpers import fetch_vikiporn, fetch_pornwhite, fetch_pornwhite_single_video, fetch_xxxbule, fetch_xxxbule_single_video, fetch_vikiporn_single_video, SOURCES
import random
from flask_caching import Cache
import base64
import ast

videos = Blueprint('videos', __name__, url_prefix="/videos")
cache = Cache()


def base64_string_to_list(string):
    my_list = ast.literal_eval(string)
    print(my_list)

# Fetch videos from multiple sources


@videos.route('/')
@cache.cached(timeout=60 * 10)
def get_feed_videos():
    query = request.args.get('q')
    limit = request.args.get('limit') if request.args.get('limit') else 100

    vikiporn = fetch_vikiporn(query)
    xxxbule = fetch_xxxbule(query)
    pornwhite = fetch_pornwhite("")

    results = xxxbule + pornwhite + vikiporn
    random.shuffle(results)

    return jsonify({
        "status": 200,
        "count": len(results[:int(limit)]),
        "data": results[:int(limit)]
    })

# Fetch videos by category


@videos.route('/category/<category>')
@cache.cached(timeout=60 * 10)
def get_videos_by_category(category):
    # query = request.args.get('q')
    limit = request.args.get('limit') if request.args.get('limit') else 30

    vikiporn = fetch_vikiporn(category)
    xxxbule = fetch_xxxbule(category)
    pornwhite = fetch_pornwhite(category)

    results = vikiporn + xxxbule + pornwhite
    random.shuffle(results)

    return jsonify({
        "status": 200,
        "count": len(results[:int(limit)]),
        "data": results[:int(limit)]
    })


# Fetcch single video from expecify source
@videos.route('/play', methods=['GET'])
def get_video_to_play():
    id = request.args.get('id') + "=="
    title_id = request.args.get('title_id')

    decoded_string = base64.b64decode(id)
    my_list = ast.literal_eval(decoded_string.decode('utf-8'))  # [box_id, source_id, video_id]
    box_id = my_list[0]
    source_id = my_list[1]
    video_id = my_list[2]
    
    print(my_list)

    video = None
    if (SOURCES[source_id] == "vikiporn" and bool(title_id) and box_id != "False" and video_id != "False"):
        video = fetch_vikiporn_single_video(box_id, video_id, title_id)
        if video == False:
            return jsonify({
                "status": 404,
                "data": {},
                "error": True
            })
        else:
            return jsonify({
                "status": 200,
                "data": video,
                "error": False
            })
    elif (SOURCES[source_id] == "pornwhite" and bool(title_id) and box_id != "False" and video_id != "False"):
        video = fetch_pornwhite_single_video(video_id, title_id, box_id)
        if video == False:
            return jsonify({
                "status": 404,
                "data": {},
                "error": True
            })
        else:
            return jsonify({
                "status": 200,
                "data": video,
                "error": False
            })


# Register Blueprints
def register_blueprints(app):
    app.register_blueprint(videos)
    cache.init_app(app)
