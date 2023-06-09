from .. import db
from .models import Score
from .schemas import RankSchema
from flask import (
	Blueprint, 
	jsonify, 
	request, 
	session, 
	url_for
)
from sqlalchemy import func
import re


blueprint = Blueprint(
	'scores',
	__name__,
	url_prefix='/scores'
)

@blueprint.route('/')
def index():
	page = request.args.get('page', 0, type=int)

	ranks = Score.query.with_entities(
		Score.id, 
		Score.name, 
		Score.points, 
		func.row_number().over(order_by=Score.points.desc()).label('rank'), 
	).order_by(Score.points.desc()).limit(10).offset(page*10).all()
	
	meta = {}
	if len(ranks) == 10: 
		meta['next'] = url_for('.index', page=page+1)

	scores_schema = RankSchema(many=True)
	return jsonify(
		data=scores_schema.dump(ranks), 
		meta=meta 
	)

@blueprint.post('/')
def create():
	name = request.json.get('name', '').strip()
	points = session.get('points', 0)

	score = None
	if points >= 50 \
		and 3 <= len(name) <= 8 \
		and re.match(r'^[A-Za-z]+[A-Za-z\-\_]*[0-9]*', name):
		
		score = Score(name=name, points=points)
		db.session.add(score)
		db.session.commit()

	rank_up = Score.query.filter(Score.points >= points).count()
	rank_down = Score.query.filter(Score.points < points).count()
	
	start_rank = max(1, rank_up - (4 if rank_down >= 6 else 9 - rank_down))
	end_rank = start_rank + 9

	ranks = Score.query.with_entities(
		Score.id, 
		Score.name, 
		Score.points, 
		func.row_number().over(order_by=Score.points.desc()).label('rank'), 
	).order_by(Score.points.desc()).slice(start_rank - 1, end_rank).all()

	meta = {}
	if score:
		meta['current_id'] = score.id

	scores_schema = RankSchema(many=True)
	return jsonify(
		data=scores_schema.dump(ranks), 
		meta=meta
	)

# ---

@blueprint.route('/stats')
def stats():
	seen_songs = session.get('seen_songs', [])
	qids = session.get('qids', [])

	d = []
	l = []
	i = 0
	for song_id in seen_songs[:-1]:
		if song_id in qids: # answered
			i += 1
			l += [1]
		else: # failed
			l += [2]
		if i == 5:
			d.append(l + [3 for _ in range(7 - len(l))])
			l = []
			i = 0
	d.append(l + [3 for _ in range(7 - len(l))])
	
	return jsonify(d)
