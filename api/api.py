import web
import soundcloud
import config
import json

# import sqlalchemy
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import scoped_session

################################################
#
#                  support methods
#
################################################

def write(payload, status):
    return json.dumps({"payload": payload, "status": status})

def notfound():
    return web.notfound("404")

def new_request(request):
    web.header("Content-Type", "application/json")
    web.header("Access-Control-Allow-Origin", "*")

def sc_search_tracks(q):

	result = []

	tracks = sc_client.get("/tracks", q=q, limit=20, linked_partition=1)

	for track in tracks:
		result.append({"title": track.title, "artist": track.user["username"]})

	return result

def tbd_search_trakcs(q):

	result = []
	tracks = 0


################################################
#
#                  search classes
#
################################################

class search:

	def POST(self):
		new_request(self)
		data = web.input()

		try:
			q = data["q"].encode("utf-8")
		except UnicodeError:
			return write({"error": "Search query not UTF-8 encoded. "}, 400)
		except KeyError:
			return write({"error": "Search query not supplied. "}, 400)

		try:
			t = data["t"].encode("utf-8")

			if t is not "track" or t is not "artist":
				return write({"error": "Invalid search type supplied. "}, 400)

		except UnicodeError:
			return write({"error": "Search type not UTF-8 encoded. "}, 400)
		except KeyError:
			t = "track"

		if t == "track":



################################################
#
#                  init
#
################################################

# class Track(base):
#     __tablename__ = "tracks"
#     id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
#     title = sqlalchemy.Column(sqlalchemy.String)
# 	album = sqlalchemy.Column(sqlalchemy.Integer)
# 	artist = sqlalchemu.Column(sqlalchemy.Integer)


sc_client = soundcloud.Client(client_id = config.auth.sc_client_id)

urls = (
    "/search", "search"
)

if __name__ == "__main__":

	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()
