import time
import redis
from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

@app.route('/titanic')
def titanic():
    df = pd.read_csv('titanic.csv')
    table = df.head().to_html(index=False)
    return render_template('titanic.html', table=table)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)



