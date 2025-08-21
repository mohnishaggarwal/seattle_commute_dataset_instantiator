#!/usr/bin/env python3
from __future__ import annotations

import sys
from models import CommuteResult
from typing import Optional

import requests


DISTANCE_MATRIX_ENDPOINT = "https://maps.googleapis.com/maps/api/distancematrix/json"

def get_commute_time(
        origin: str,
        destination: str,
        api_key: str,
        units: str = "imperial",
        timeout: int = 15,
) -> Optional[CommuteResult]:
    params = {
        "origins": origin,
        "destinations": destination,
        "mode": "driving",
        "departure_time": "now", # required to get result with traffic included
        "key": api_key,
        "units": units,
        "traffic_model": "best_guess",
    }

    try:
        resp = requests.get(DISTANCE_MATRIX_ENDPOINT, params=params, timeout=timeout)
    except requests.RequestException as e:
        print(f"[error] Network error: {e}", file=sys.stderr)
        return None

    if resp.status_code != 200:
        print(f"[error] HTTP {resp.status_code}: {resp.text}", file=sys.stderr)
        return None

    data = resp.json()
    status = data.get("status")
    if status != "OK":
        print(f"[error] API status: {status} — {data}", file=sys.stderr)
        return None

    rows = data.get("rows", [])
    if not rows or not rows[0].get("elements"):
        print("[error] Unexpected API response shape.", file=sys.stderr)
        return None

    el = rows[0]["elements"][0]
    el_status = el.get("status")
    if el_status != "OK":
        print(f"[error] Route status: {el_status}", file=sys.stderr)
        return None

    dur_obj = el.get("duration_in_traffic")
    dist_obj = el.get("distance")

    if not dur_obj or not dist_obj:
        print("[error] Missing duration/distance in response.", file=sys.stderr)
        return None

    duration_minutes = int(dur_obj.get("value", 0)) / 60
    duration_text = dur_obj.get("text", "")

    return CommuteResult(
        origin=origin,
        destination=destination,
        duration_minutes=duration_minutes,
        duration_text=duration_text,
    )
