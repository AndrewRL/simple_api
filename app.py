import csv
from flask import Flask, jsonify, request, abort

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

def write_pos_file(pos_data, outfile):
    with open(outfile, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([row for row in pos_data])

@app.route('/api/v1/positions', methods=['GET'])
def get_positions():
    return jsonify(read_csv('/home/ec2-user/test_positions.csv'))

@app.route('/api/v1/positions', methods=['POST'])
def add_positions():
    if not request.json or not 'positions' in request.json:
        abort(400)
    
    # load positions from csv
    all_positions = read_csv('/home/ec2-user/test_positions.csv')
    # create a list of position data from post + test_positions.csv
    all_positions.extend(request.json['positions'])
    # sort data by timestamp
    all_positions = sorted(all_positions, key=lambda x: float(x[1]))
    print(all_positions)
    # save data to positions.csv
    write_pos_file(all_positions, 'positions.csv')
    return jsonify({'success': True}), 201

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
