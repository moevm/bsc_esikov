from flask import Flask
from flask import render_template
from flask import request
from searcher import Searcher

# Dictionary of programming languages:
# Name: src_file_extension
languages = {
    "C": "c",
}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', languages=languages)


@app.route('/similarity', methods=['POST', 'GET'])
def similarity():
    if request.method == 'POST':
        searcher = Searcher(
            check_path=request.form['check'],
            search_path=request.form['data'],
            limit=request.form['limit'],
            branches=request.form['branches'],
            file_extension=request.form['language']
        )
        similarity = searcher.search_similarity()
    else:
        return '<h1>Search was not started</h1>'

    if not similarity:
        return render_template('not_similarity.html')
    else:
        return render_template(
            'similarity.html',
            similarity_list=similarity,
            len=len(similarity)
        )
