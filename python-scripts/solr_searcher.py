from flask import Flask
from flask import request
import pysolr
import os
import requests
from flask_cors import cross_origin


app = Flask(__name__)


@app.route('/search', methods=['GET'])
@cross_origin()
def get_vector():
    if request.method == 'GET':
        query = request.args.get('q', None)
        method = request.args.get('method', None)
        top = request.args.get('top', None)

        solr = pysolr.Solr('http://localhost:8983/solr/cord-papers/', always_commit=True, timeout=10)
        results = None
        papers = []

        if method == 'sbert':
            response = requests.get(f'http://localhost:8080/get-encoded-query?query={query}')
            results = solr.search("{!knn f=vector topK=" + top + "}" + str(response.json()))
        elif method == 'inverted':
            params = {
                "df": "abstract",
                "indent": "true",
                "q.op": "OR",
                "useParams": "",
                "rows": top
            }

            results = solr.search(query, **params)

        if results is not None:
            for result in results:
                paper = {
                    "title": result['title'],
                    "url": result['url']
                }
                papers.append(paper)

        return papers


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9090))
    app.run(debug=True, host='0.0.0.0', port=port)
