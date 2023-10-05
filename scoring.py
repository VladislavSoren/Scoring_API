import hashlib
import json


def get_score(store, phone, email, birthday=None, gender=None, first_name=None, last_name=None):
    key_parts = [
        phone or "",
        email or "",
        gender or "",
        first_name or "",
        last_name or "",
        birthday or "",
    ]
    key_parts_str = [str(key) for key in key_parts]

    # gen key for request by params
    info_for_hash_bytes = "".join(key_parts_str).encode("utf-8")
    key = "uid:" + hashlib.md5(info_for_hash_bytes).hexdigest()

    score = store.get_cache(key) or 0
    if score:
        return score
    if phone:
        score += 1.5
    if email:
        score += 1.5
    if birthday and gender:
        score += 1.5
    if first_name and last_name:
        score += 0.5
    # cache for 30 sec
    store.set_cache(key, score, 30)
    return score


def get_interests(store, cid):
    r = store.get(cid)
    return json.loads(r) if r else []
