import csv
from flask import Flask, jsonify

app = Flask(__name__)

def read_csv(path, skiplines=True, header=True):
    data = []
    with open(path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        if header:
            next(reader, None)
        for row in reader:
            data.append(row)
    return data

@app.route('/api/v1/positions', methods=['GET'])
def get_positions():
    return jsonify(read_csv('/home/ec2-user/test_positions.csv'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
