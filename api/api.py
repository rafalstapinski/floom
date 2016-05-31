import web
import soundcloud
import config
import json
import urllib2

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

def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    request = opener.open(url)
    return request.url

def sc_search_tracks(q):

	result = []

	tracks = sc_client.get("/tracks", q=q)

	for track in tracks:

		saved_track = session.query(SC_Track).filter(SC_Track.sc_id == track.id)

		if saved_track is not None:
			stream_url = saved_track.stream_url
		else:
			stream_url = get_redirected_url(track.stream_url + "?client_id=%s" % config.auth.sc_client_id)
			session.add(SC_Track(sc_id=track.id, stream_url=stream_url))
	        session.commit()

		result.append({"title": track.title, "artist": track.user["username"], "artwork": track.artwork_url, "stream": stream_url})

		# cache results here
		# if result not in cache, then lookup redirected url
		# takes hella long to get redirected url

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
			return write(200, {"tracks": sc_search_tracks(q)})

################################################
#
#                  init
#
################################################

class SC_Track(base):
    __tablename__ = "sc_tracks"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    sc_id = sqlalchemy.Column(sqlalchemy.Integer)
	stream_url = sqlalchemy.Column(sqlalchemy.String)

base = declarative_base()


sc_client = soundcloud.Client(client_id = config.auth.sc_client_id)

urls = (
    "/search", "search"
)

if __name__ == "__main__":

	app = web.application(urls, globals())
	app.notfound = notfound
	app.run()
