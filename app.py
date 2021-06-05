import requests
from flask import Flask
from flask import render_template
from flask import request
from src.searcher import Searcher

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
        try:
            similarity_list = searcher.search_similarity()
            if not similarity_list:
                return render_template('message.html', message="Similarity not found")
            else:
                return render_similarity_template("Similarity code", similarity_list)
        except (KeyError, requests.exceptions.HTTPError) as e:
            return render_similarity_template("Github API rate limit exceeded. Limit = 5000 requests per hour. Try later. Matches found before error:", searcher.similarity_list)
        except requests.exceptions.Timeout as e:
            return render_similarity_template(str(e).split("'")[-2] + ". Matches found before error:", searcher.similarity_list)
        except (ValueError, requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as e:
            return render_similarity_template(str(e) + ". Matches found before error:", searcher.similarity_list)
    else:
        return render_template('message.html', message="Search was not started")


def render_similarity_template(header, similarity_list):
    return render_template(
        'similarity.html',
        header=header,
        similarity_list=similarity_list,
        len=len(similarity_list)
    )


@app.errorhandler(404)
def not_found(e):
    return render_template('message.html', message="Page not found")
