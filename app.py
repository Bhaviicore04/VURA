from flask import Flask, render_template, jsonify
import json, time, datetime

app = Flask(__name__)

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/data')
def data():
    try:
        with open('zone_data.json', 'r') as f:
            return jsonify(json.load(f))
    except:
        return jsonify({
            'person_count':  0,
            'queuing_count': 0,
            'chaotic_count': 0,
            'is_queue':      False,
            'status':        'EMPTY',
            'civic_score':   60,
            'time_saved':    0,
            'stops':         [],
            'date':          datetime.date.today().isoformat(),
            'timestamp':     time.time(),
        })
if __name__ == '__main__':
    print("VURA v3 dashboard → http://localhost:5000")
    app.run(host='0.0.0.0', port=5000)
