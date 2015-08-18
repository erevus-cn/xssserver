#! coding:utf-8

import web
import json
import re
import base64

db = web.database(dbn='mysql', host='127.0.0.1', db='xssserver', user='root', pw='123456')
render = web.template.render('templates/')


urls = (
    '/', 'index',
    '/login','login',
    '/show','show'  
)

app = web.application(urls,globals())
allowed = (
            ('admin','shortshortmujj'),
          )



class login:
    def GET(self):
        auth = web.ctx.env.get('HTTP_AUTHORIZATION')
        authreq = False
        if auth is None:
            authreq = True
        else:
            auth = re.sub('^Basic ','',auth)
            username,password = base64.decodestring(auth).split(':')
            if (username,password) in allowed:
                raise web.seeother('/')
            else:
                authreq = True
        if authreq:
            web.header('WWW-Authenticate','Basic realm="Auth example"')
            web.ctx.status = '401 Unauthorized'
            return


class index:
    def GET(self):
        if web.ctx.env.get('HTTP_AUTHORIZATION') is not None:
            data = {}
            keys = web.input().keys()
            post = web.data()
            ip = web.ctx.ip
            referer = web.ctx.env.get('HTTP_REFERER')
            for key in keys:
                value = web.input()
                rs = {key:value[key]}
                data.update(rs)
            server_content = json.dumps({'HTTP_REFERER': referer, 'REMOTE_ADDR': ip})
            project_content = db.insert('xss_content', content=json.dumps(data),
                    server_content=server_content)
            return json.dumps({'status': 200,
                                    'data': data,
                                    'ip': ip,
                                    'referer': referer})
        else:
            raise web.seeother('/login')

    def POST(self):
        data = {}
        keys = web.input().keys()
        post = web.data()
        ip = web.ctx.ip
        referer = web.ctx.env.get('HTTP_REFERER')
        for key in keys:
            value = web.input()
            rs = {key:value[key]}
            data.update(rs)
        server_content = json.dumps({'HTTP_REFERER': referer, 'REMOTE_ADDR': ip})
        project_content = db.insert('xss_content', content=json.dumps(data),
                server_content=server_content)
        return json.dumps({'status': 200,
                                'data': data,
                                'ip': ip,
                                'referer': referer})     

        
class show:
    def GET(self):
        data = []
        results = db.select('xss_content')
        for result in results:
            tmp_rs = {
                     'header': json.loads(result.server_content),
                     'time': str(result.updateTime),
                     'request': json.loads(result.content),
                    }
            data.append(tmp_rs)
        data = json.dumps(data)
        return render.show(data)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
