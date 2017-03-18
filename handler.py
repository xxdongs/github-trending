import tornado.httpserver
import tornado.httpclient
import tornado.web
import tornado.options
import tornado.ioloop
import tornado.gen
import json

from scrapy import get_trending, REPOSITORY, DEVELOPER


class IndexHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    def get(self):
        self.write('Hello Heroku!')


class BaseHandler(tornado.web.RequestHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self):
        response = yield tornado.gen.Task(self.get_result, self.get_since())
        self.write(json.dumps(response, indent=2))
        self.finish('Ok')

    def get_since(self):
        return self.get_argument('since', None)

    @tornado.gen.coroutine
    def get_result(self, params):
        pass


class LanguageHandler(BaseHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, lang):
        response = yield tornado.gen.Task(self.get_result_language, self.get_since(), lang)
        self.write(json.dumps(response, indent=2))
        self.finish('Ok')

    @tornado.gen.coroutine
    def get_result_language(self, params, lang):
        return get_trending(url=self.get_url() + lang, params=params)

    def get_url(self):
        pass


class RepositoryHandler(BaseHandler):
    @tornado.gen.coroutine
    def get_result(self, params):
        return get_trending(url=REPOSITORY, params=params)


class RepositoryLanguageHandler(LanguageHandler):
    def get_url(self):
        return REPOSITORY


class DeveloperHandler(BaseHandler):
    @tornado.gen.coroutine
    def get_result(self, params):
        return get_trending(url=DEVELOPER, params=params)


class DeveloperLanguageHandler(LanguageHandler):
    def get_url(self):
        return DEVELOPER

