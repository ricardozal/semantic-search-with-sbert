from sentence_transformers import SentenceTransformer
from flask import Flask
from flask import request
import os
import numpy as np
import json

# You can find the trained model here: https://drive.google.com/drive/folders/1LP944V7jRgAw1nPUnWiI-R0HJEUeAvkT?usp=share_link
model_path = 'search-model'
model = SentenceTransformer(model_path)


def encode_query(query):
    encoded_data = model.encode(query)
    encoded_data = np.asarray(encoded_data.astype('float32'))

    return json.dumps(encoded_data.tolist())


app = Flask(__name__)


@app.route('/get-encoded-query', methods=['GET'])
def get_vector():
    if request.method == 'GET':
        query = request.args.get('query', None)

        return encode_query(query)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
