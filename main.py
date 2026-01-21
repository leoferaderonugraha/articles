import markdown
import os
import pathlib

from flask import (
    abort,
    Flask,
    render_template,
)


def get_articles():
    valid_articles = {}
    with os.scandir('./articles') as entries:
        for entry in entries:
            if entry.is_file():
                valid_articles[pathlib.Path(entry.path).stem] = entry.path

    return dict(sorted(valid_articles.items()))


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html"), 404


@app.get('/')
def index():
    articles = get_articles()
    return render_template('index.html', articles=articles)


@app.get('/<name>')
def article(name):
    valid_articles = get_articles()
    article_path = valid_articles.get(name)
    if article_path is not None:
        data = open(article_path, 'r').read()
        content = markdown.markdown(data, extensions=['toc', 'attr_list'])
        return render_template('article.html',
                               title=name,
                               content=content)

    abort(404)


if __name__ == '__main__':
    app.run(debug=True)
