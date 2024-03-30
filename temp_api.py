import sys
import flask
from flask import request, abort, jsonify

comment_list = []
post_link_count = {}
group_link_list = []
total_bot = 15
slots = [0, 0]
bot_status = "running"
app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/comments/remain', methods=['POST'])
def count_comment():
    global post_link_count
    global total_bot
    """
    {
        "post_link": <post's link>
    }
    :return:
    """
    if not request.json:
        abort(400)
    post_link = request.json["post_link"]
    print("post_link: ", post_link, file=sys.stderr)
    total_bot_remain = total_bot - post_link_count.get(post_link) if post_link_count.get(post_link) else total_bot
    total_bot_remain = 0 if total_bot_remain < 0 else total_bot_remain
    response_data = dict(data=total_bot_remain)
    return jsonify(response_data)


@app.route('/groups/add_group_link', methods=['POST'])
def save_group_link():
    global group_link_list
    """
    {
        "group_link": <group_link>,
        "city": <city>
        "group_id": <group_id>,
        "region": <region>,
        "sector": <sector>
    }
    :return:
    """
    if not request.json:
        abort(400)
    print("save group link: ", request.json, file=sys.stderr)
    link = request.json["group_link"]
    city = request.json["city"]
    gr_id = request.json["group_id"]
    region = request.json["region"]
    sector = request.json["sector"]
    group_link_list.append({"group_link": link, "city": city, "group_id": gr_id,
                            "region": region, "sector": sector})
    response_data = dict(data=request.json)
    return jsonify(response_data)


@app.route('/groups/get_group_link', methods=['POST'])
def get_group_link():
    global group_link_list
    """
    {
        "city": <city>
    }
    :return:
    """
    print("group_link_list: ", group_link_list, file=sys.stderr)
    if not group_link_list:
        abort(400)
    # lay theo thu tu
    city = request.json["city"]
    for gr_data in group_link_list:
        if city == gr_data.get("city"):
            response_data = dict(group_link=gr_data.get("group_link"), group_id=gr_data.get("group_id"),
                                 sector=gr_data.get("sector"))
            group_link_list.remove(gr_data)
            return jsonify(response_data)


@app.route('/comments/add_comment', methods=['POST'])
def save_comment():
    global comment_list
    global post_link_count
    """
    {
        "comment": <comment>,
        "post_link": <post's link>
    }
    :return:
    """
    if not request.json:
        abort(400)
    print("save comment: ", request.json, file=sys.stderr)
    post_link = request.json["post_link"]
    post_link_count.setdefault(post_link, 0)
    post_link_count[post_link] += 1
    comment_list.append(request.json)
    response_data = dict(data=request.json)
    return jsonify(response_data)


@app.route('/comments/get_comment', methods=['POST'])
def get_comment():
    global comment_list
    """
        {
            "post_link_list": []
        }
    """
    post_link_list = request.json["post_link_list"]
    data = None
    try:
        post_link = comment_list[0].get("post_link")
        have_comment = False
        for old_link in post_link_list:
            if post_link and (post_link in old_link or old_link in post_link):
                have_comment = True
                break
        if not have_comment:
            data = comment_list[0]
            print("da lay comment", data, file=sys.stderr)
    except IndexError:
        return {}
    response_data = dict(data=data)
    return jsonify(response_data)


@app.route('/comments/remove_comment', methods=['POST'])
def remove_comment():
    global comment_list
    """
        {
            "comment": "",
            "post_link"
        }
    """
    comment_need_remove = None
    for comment_dict in comment_list:
        if comment_dict == request.json:
            comment_need_remove = request.json
            print("da xoa cmt")
            break
    if comment_need_remove:
        comment_list.remove(comment_need_remove)
    response_data = dict(data={})
    return jsonify(response_data)


@app.route('/slot/register', methods=['POST'])
def register_slot():
    global slots
    signal = request.json["signal"]
    """
        {
            "signal": 1,
        }
    """
    have_slot = False
    for idx, sl in enumerate(slots):
        if sl != signal:
            slots[idx] = signal
            have_slot = True
            break

    print("post_link: ", slots, file=sys.stderr)
    response_data = dict(data=have_slot, slots=slots)
    return jsonify(response_data)


app.run(host="0.0.0.0", port=8000)
