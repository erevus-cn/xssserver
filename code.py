#! coding:utf-8

import web
import json

db = web.database(dbn='mysql', host='127.0.0.1', db='xssserver', user='root', pw='123456')
render = web.template.render('templates/')
urls = (
    '/', 'index',
    '/show','show'  
)

class index:
    def GET(self):
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
