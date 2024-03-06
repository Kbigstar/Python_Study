from flask import Flask, request, jsonify, Response, render_template
import json
import easyocr
app = Flask(__name__)
reader = easyocr.Reader(['en', 'ko'], gpu=False)

@app.route('/upload', methods=['POST', 'GET'])
def upload_file():
    if request.method =='POST':
        f = request.files['file']
        print(f)
        if f.filename == '':
            return jsonify({'error': 'no selected file'})
        if f:
            img = f.read()
            # easyocr
            results = reader.readtext(img)
            dataset = []
            for bbox, text, prob in results:
                if prob > 0.1:
                    dataset.append({'text': text})
            json_result = json.dumps(dataset)
            return Response(json_result, mimetype='application/json')
    else:
        return render_template("index.html")
if __name__ == '__main__':
    app.run(debug=True)