from flask import jsonify, request
from flask_restplus import Namespace, Resource, fields
from aedem.utils import dictionarize
from aedem.models import Session
from aedem.models.news import News

namespace = Namespace(
    'news',
    path = "/news",
    description = 'Operações de noticias'
)
create_news_model = namespace.model("create_news", {
    "title": fields.String(
        description = "Titulo da noticia",
        required = True),
    "content": fields.String(
        description = "Conteúdo da notícia",
        required = True),
    "source": fields.String(
        description = "Fonte emissora", 
        required = True),
    "published_at": fields.String(
        description = "Data de criação", 
        required = True),
    "external_link": fields.String(
        description = "Link externo", 
        required = True),
    "state_abbr": fields.String(
        description = "Estado", 
        required = True),
    "city_name": fields.String(
        description = "Cidade", 
        required = True),
})
@namespace.route('')
class list_news(Resource):
	@namespace.doc('list_news')
	def get(self):
		'''Listagem de todas as notícias'''
		session = Session()

		# get list of all news 
		news_list = []
		for news in session.query(News).all():
			news_list.append(dictionarize(news))

		# respond request
		response = {
			"status" : 200,
			"message" : "Success",
			"error" : False,
			"response" : news_list 
		}

		return jsonify(response)
	@namespace.doc('create_news')
	@namespace.expect(create_news_model)
	def post(self):
		session = Session()
		
		# get news information provided in the request
		news_data = request.get_json(force = True)
		
		#create database model
		new_news = News(
			title = news_data['title'],
			content = news_data['content'],
			source = news_data['source'],
			published_at = news_data['published_at'],
			external_link = news_data['external_link'],
			state_abbr = news_data['state_abbr'],
			city_name = news_data['city_name']
		) 
		
		# add new news entity to database
		session.add(new_news)
		session.commit()
        
		# respond request
		response = {
			"status": 200,
			"message": "Success",
			"error": False,
			"response": dictionarize(new_news)
		}
		return jsonify(response)

@namespace.route('/<id>')
@namespace.param('id','identificador da notícia')
@namespace.response(404, 'Notícia não encontrada')
class SpecificNews(Resource):
	@namespace.doc('get_news')
	def get(self, id):
		'''Mostrar uma notícia especifica'''
		session = Session()
		
		# get news by id 
		news = session.query(News).filter_by(id = id).first()
		
		# check if the news exists
		if news is None:
			namespace.abort(404)
		
		# respond request
		response = {
			"status": 200,
			"message": "Success",
			"error": False,
			"response": dictionarize(news)
		}
		return jsonify(response)

	@namespace.doc('delete_news')
	def delete(self, id):
		'''Deletar uma notícia'''
		session = Session()
		
		# look up given determined news
		determined_news = session.query(News).filter_by(id = id)
		
		# check if determined news exists 
		if determined_news.scalar() is None:
			namespace.abort(404)
		
		# delete news from database
		news = determined_news.one()
		records = dictionarize(news)
		session.delete(news)
		session.commit()
		
		#respond request
		response = {
			"status" : 200,
			"message" : "Sucess",
			"error" : False,
			"response" : records
		}
		return jsonify(response)
	@namespace.doc('update_news')
	def put(self, id):
		'''Atualiza os dados de uma noticia'''
		session = Session()
		
		# get news
		determined_news = session.query(News).filter_by(id = id)
		
		#check if news exists
		if determined_news.scalar() is None:
			namespace.abort(404)
		
		# update news data with given values
		news = determined_news.one()
		for datafield in request.args:
			setattr(news, datafield, request.args[datafield])
		session.add(news)
		session.commit()
		
		# respond request
		response = {
			"status": 200,
			"message": "Success",
			"error": False,
			"response": dictionarize(news)
		}
		return jsonify(response)