import markdown

from flask import Flask, render_template, render_template_string


app = Flask(__name__)


@app.get('/')
def index():
    data = open('./articles/idor.md', 'r').read()
    content = markdown.markdown(data, extensions=['toc', 'attr_list'])
    print(content)
    return render_template('index.html', title="IDOR", content=content)


if __name__ == '__main__':
    app.run()
