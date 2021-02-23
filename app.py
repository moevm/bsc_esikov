from flask import Flask
from flask import render_template
from flask import request
from searcher import Searcher

app = Flask(__name__)
searcher = None


@app.route('/')
def index():
    name = 'Test'
    return render_template('index.html', x=name)


@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        global searcher
        searcher = Searcher(
            check_path=request.form['check'],
            search_path=request.form['data'],
            limit=request.form['limit'],
            branches=request.form['branches'],
            file_extension="c"
        )
        print("start search")
        searcher.search_similarity()
        print("end search")

        page = 0
    else:
        page = request.args.get('page')

    if searcher is None:
        return '<h1>Search was not started</h1>'

    sim = searcher.get_similarity(page)
    check_file_similarity_src, detected_file_similarity_src = sim.get_similarity_src()
    return render_template(
        'similarity.html',
        page=page,
        percentage=sim.similarity_percentage,
        check_file_source=sim.check_file_source + "  " + sim.check_file_path,
        check_file_src_list=check_file_similarity_src,
        detected_file_source=sim.detected_file_source + "  " + sim.detected_file_path,
        detected_file_src_list=detected_file_similarity_src,
        block_left_button=int(page) <= 0,
        block_right_button=int(page) >= len(searcher.similarity_list) - 1,
    )