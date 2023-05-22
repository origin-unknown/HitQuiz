from .. import ma

class RankSchema(ma.Schema):
	class Meta:
		fields = ('name', 'points', 'rank')
