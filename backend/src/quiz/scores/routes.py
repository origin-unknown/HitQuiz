from .. import db
from .models import Score
from .schemas import ScoreSchema
from flask import (
	Blueprint, 
	jsonify, 
	request, 
	session
)


blueprint = Blueprint(
	'scores',
	__name__,
	url_prefix='/scores'
)

@blueprint.route('/')
def index():
	scores = Score.query.order_by(Score.points.desc()).limit(10).all()
	scores_schema = ScoreSchema(many=True)
	return scores_schema.jsonify(scores)

@blueprint.post('/')
def create():
	name = request.json.get('name', '')
	points = session.get('points', 0)

	# use webargs
	if points >= 50 and len(name.strip()) > 3:
		score = Score(name=name, points=points)
		db.session.add(score)
		db.session.commit()

	scores = Score.query.order_by(Score.points.desc()).limit(10).all()
	scores_schema = ScoreSchema(many=True)
	return scores_schema.jsonify(scores)
