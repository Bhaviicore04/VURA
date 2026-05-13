import cv2
import numpy as np
from ultralytics import YOLO
import json
import time
import datetime
import random

# ─────────────────────────────────────────────
#  VURA v3 — Final Detector
#  Terminal 1: python detector.py
#  Press Q to quit
# ─────────────────────────────────────────────

model = YOLO('yolov8n.pt')

CHAOS_THRESHOLD  = 3   # people in one cluster = chaotic
TIME_PER_PERSON  = 2   # minutes saved per person when queuing

# ── HYDERABAD BUS STOPS ───────────────────────
BUS_STOPS = [
    {"name": "Mehdipatnam",   "lat": 17.3951, "lng": 78.4396, "base_score": 38},
    {"name": "Ameerpet",      "lat": 17.4375, "lng": 78.4483, "base_score": 55},
    {"name": "Secunderabad",  "lat": 17.4399, "lng": 78.4983, "base_score": 78},
    {"name": "Koti",          "lat": 17.3850, "lng": 78.4867, "base_score": 42},
    {"name": "Dilsukhnagar",  "lat": 17.3688, "lng": 78.5247, "base_score": 61},
    {"name": "LB Nagar",      "lat": 17.3469, "lng": 78.5524, "base_score": 45},
    {"name": "Kukatpally",    "lat": 17.4849, "lng": 78.4138, "base_score": 70},
    {"name": "ECIL X Roads",  "lat": 17.4700, "lng": 78.5600, "base_score": 33},
    {"name": "Uppal",         "lat": 17.4059, "lng": 78.5590, "base_score": 52},
    {"name": "Begumpet",      "lat": 17.4435, "lng": 78.4683, "base_score": 67},
    {"name": "Tolichowki",    "lat": 17.4050, "lng": 78.4183, "base_score": 48},
    {"name": "SR Nagar",      "lat": 17.4531, "lng": 78.4364, "base_score": 59},
    {"name": "Miyapur",       "lat": 17.4965, "lng": 78.3685, "base_score": 74},
    {"name": "Hitech City",   "lat": 17.4474, "lng": 78.3762, "base_score": 82},
    {"name": "Charminar",     "lat": 17.3616, "lng": 78.4747, "base_score": 29},
]

def load_scores():
    try:
        with open('civic_scores.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_scores(scores):
    with open('civic_scores.json', 'w') as f:
        json.dump(scores, f, indent=2)

def init_stop_scores():
    scores = load_scores()
    today  = datetime.date.today().isoformat()
    if today not in scores:
        scores[today] = {}
    for stop in BUS_STOPS:
        name = stop['name']
        if name not in scores[today]:
            variation = random.uniform(-8, 8)
            scores[today][name] = round(
                max(0, min(100, stop['base_score'] + variation)), 1)
    save_scores(scores)
    return scores

def update_camera_score(scores, is_queue):
    today = datetime.date.today().isoformat()
    if today not in scores:
        scores[today] = {}
    current = scores[today].get('Camera Location', 60.0)
    if is_queue:
        current = min(100, current + 0.05)
    else:
        current = max(0,   current - 0.08)
    scores[today]['Camera Location'] = round(current, 1)
    save_scores(scores)
    return scores[today]['Camera Location']

def detect_queue_pattern(boxes, frame_width, frame_height):
    """
    Detect if people are forming a queue (linear spread)
    or clustered chaotically (all in one spot).
    Returns: is_queue (bool), queuing_count, chaotic_count
    """
    if len(boxes) == 0:
        return False, 0, 0
    if len(boxes) == 1:
        return True, 1, 0

    # Get center points
    centers = [(int((x1+x2)/2), int((y1+y2)/2)) for (x1,y1,x2,y2) in boxes]
    xs = [c[0] for c in centers]
    ys = [c[1] for c in centers]

    # Spread in x and y
    x_spread = max(xs) - min(xs)
    y_spread = max(ys) - min(ys)

    # If people are spread across more than 40% of frame width
    # OR more than 40% of frame height → queue-like
    is_linear = (x_spread > frame_width * 0.4) or (y_spread > frame_height * 0.4)

    if is_linear:
        # Estimate how many are "in queue" vs outliers
        queuing = max(1, int(len(boxes) * 0.75))
        chaotic = len(boxes) - queuing
        return True, queuing, chaotic
    else:
        # Clustered
        queuing = max(0, int(len(boxes) * 0.2))
        chaotic = len(boxes) - queuing
        return False, queuing, chaotic

def save_data(person_count, is_queue, queuing_count,
              chaotic_count, civic_score, time_saved, stops):
    today = datetime.date.today().isoformat()
    scores = load_scores()
    stops_data = []
    for stop in BUS_STOPS:
        name  = stop['name']
        score = scores.get(today, {}).get(name, stop['base_score'])
        stops_data.append({
            'name':  name,
            'lat':   stop['lat'],
            'lng':   stop['lng'],
            'score': score,
        })
    cam_score = scores.get(today, {}).get('Camera Location', 60)
    stops_data.append({
        'name':  'Camera Location (Live)',
        'lat':   17.4200,
        'lng':   78.4500,
        'score': cam_score,
    })

    status = 'QUEUE' if is_queue else ('CHAOTIC' if person_count > 0 else 'EMPTY')

    payload = {
        'person_count':   person_count,
        'queuing_count':  queuing_count,
        'chaotic_count':  chaotic_count,
        'is_queue':       is_queue,
        'status':         status,
        'civic_score':    civic_score,
        'time_saved':     time_saved,
        'stops':          stops_data,
        'date':           today,
        'timestamp':      time.time(),
    }
    with open('zone_data.json', 'w') as f:
        json.dump(payload, f)

def run():
    scores = init_stop_scores()

    cap = cv2.VideoCapture(1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH,  640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("ERROR: No webcam found.")
            # Run in demo mode
            while True:
                scores = load_scores()
                save_data(0, False, 0, 0, 60, 0, scores)
                time.sleep(2)
            return

    print("VURA v3 running. Press Q to quit.")
    score_timer = time.time()
    civic_score = 60.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        h, w = frame.shape[:2]

        # ── YOLO ─────────────────────────────
        results = model(frame, classes=[0], verbose=False)
        boxes   = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                boxes.append((x1, y1, x2, y2))

        person_count = len(boxes)

        # ── QUEUE DETECTION ──────────────────
        is_queue, queuing_count, chaotic_count = detect_queue_pattern(boxes, w, h)
        time_saved = queuing_count * TIME_PER_PERSON

        # ── COLORS ───────────────────────────
        main_color = (0, 180, 80) if is_queue else (0, 60, 220)

        # ── DRAW BOXES ───────────────────────
        for (x1, y1, x2, y2) in boxes:
            cv2.rectangle(frame, (x1,y1), (x2,y2), main_color, 2)

        # ── TOP BAR ──────────────────────────
        cv2.rectangle(frame, (0,0), (w, 52), (20,20,20), -1)
        status_text = "QUEUE FORMING" if is_queue else "CHAOTIC — PLEASE QUEUE"
        cv2.putText(frame, f'VURA  |  {person_count} people  |  {status_text}',
                    (10, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.6, main_color, 2)

        # ── NUDGE BAR ────────────────────────
        if person_count > 0:
            if is_queue:
                msg = f'Great! {queuing_count}/{person_count} queuing. Saving ~{time_saved} min.'
                bcol = (0, 100, 40)
            else:
                msg = f'{chaotic_count}/{person_count} not queuing. Form a line — save {time_saved} min!'
                bcol = (0, 0, 180)
            cv2.rectangle(frame, (0,52), (w,90), bcol, -1)
            cv2.putText(frame, msg, (8,76),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255,255,255), 2)

        # ── SCORE UPDATE ─────────────────────
        if time.time() - score_timer > 8:
            civic_score = update_camera_score(scores, is_queue)
            scores      = load_scores()
            score_timer = time.time()

        # ── FOOTER ───────────────────────────
        col = (0,200,80) if civic_score >= 70 else (0,165,255) if civic_score >= 50 else (0,0,220)
        cv2.rectangle(frame, (0, h-36), (w, h), (20,20,20), -1)
        cv2.putText(frame,
                    f'Civic Score: {civic_score:.1f}/100  |  Time Saved: {time_saved} min  |  Q=quit',
                    (8, h-12), cv2.FONT_HERSHEY_SIMPLEX, 0.42, col, 1)

        save_data(person_count, is_queue, queuing_count,
                  chaotic_count, civic_score, time_saved, scores)

        cv2.imshow('VURA v3 — Live Monitor', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run()
