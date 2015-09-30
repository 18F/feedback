import datetime

from flask import Flask, request, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from sqlalchemy.dialects.postgresql import JSON

from webargs import fields
from webargs.flaskparser import use_kwargs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
db = SQLAlchemy(app)

class Feedback(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    url = db.Column(db.String)
    referer = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    settings = db.Column(JSON)

    upvote = db.Column(db.Boolean)
    comment = db.Column(db.Text)

@app.route('/feedback/', methods=['POST'])
@use_kwargs({
    'url': fields.Url(required=True),
    'referer': fields.Url(missing=None, allow_none=True),
    'upvote': fields.Boolean(missing=None, allow_none=True),
    'comment': fields.Str(missing=None, allow_none=True),
})
def submit_feedback(**kwargs):
    kwargs.update({
        'timestamp': datetime.datetime.utcnow(),
        'settings': {
            'headers': dict(request.headers),
        },
    })
    feedback = Feedback(**kwargs)
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'status': 'success'}), 201

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)