import os
import requests
from datetime import date, timedelta
import json


META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT_ID = os.getenv("META_AD_ACCOUNT_ID")

GRAPH_API_VERSION = "v19.0"


def fetch_insights(date_preset=None, time_range=None):
    url = f"https://graph.facebook.com/{GRAPH_API_VERSION}/{AD_ACCOUNT_ID}/insights"

    params = {
    "fields": "ctr,cpm,frequency,spend,impressions",
    "level": "ad",
    "limit": 200,
    "date_preset": date_preset,
    "access_token": META_ACCESS_TOKEN
 }

    if date_preset:
        params["date_preset"] = date_preset

    if time_range:
        params["time_range"] = json.dumps(time_range)


    response = requests.get(url, params=params)
    response.raise_for_status()

    return response.json().get("data", [])


def fetch_ads_data():
    # Recent 7 days
    recent_data = fetch_insights(date_preset="last_7d")

    # Previous 7 days (explicit dates)
    today = date.today()
    prev_end = today - timedelta(days=7)
    prev_start = today - timedelta(days=14)

    previous_data = fetch_insights(
        time_range={
            "since": prev_start.strftime("%Y-%m-%d"),
            "until": prev_end.strftime("%Y-%m-%d")
        }
    )

    previous_lookup = {ad["ad_id"]: ad for ad in previous_data}

    ads_data = []

    for ad in recent_data:
        ad_id = ad["ad_id"]
        prev = previous_lookup.get(ad_id)

        if not prev:
            continue

        ads_data.append({
            "ad_id": ad.get("ad_id"),
            "ad_name": ad.get("ad_name"),
            "ctr_recent": float(ad.get("ctr", 0)),
            "ctr_prev": float(prev.get("ctr", 0)),
            "cpm_recent": float(ad.get("cpm", 0)),
            "cpm_prev": float(prev.get("cpm", 0)),
            "frequency": float(ad.get("frequency", 0)),
            "spend_recent": float(ad.get("spend", 0))
        })

    return ads_data
