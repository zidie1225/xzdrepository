# from flask import Flask, Markup
# app = Flask(__name__)    #创建了一个实例，name代表这个模块的名字
#
# @app.route('/')    #route()这个修饰器定义了一个路由，告诉flask如何访问该函数
# def index():
#     return Markup('<div>Hello %s</div>') % '<em>Flask</em>'
# if __name__=='__main__':
#     app.debug = True
#     app.run()    #run()函数使这个应用在服务器上运行起来



# from flask import Flask
# from flask import render_template
#
# app = Flask(__name__)
# @app.route('/hello')
# @app.route('/hello/<name>')
# def hello(name=None):
#     return render_template('hello.html',name=name)    #调用了”render_template()”方法来渲染模板，第一个参数”hello.html”指向你想渲染的模板名称，第二个参数”name”是你要传到模板去的变量，变量可以传多个
#
# if __name__ == '__main__':
#     app.run(debug=True)



from flask import Flask,url_for,request,render_template,redirect,session,make_response
import time

app = Flask(__name__)
@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin':    #”form”变量是一个字典，可以获取Post请求表单中的内容
            session['user'] = request.form['user']    #”admin”登陆成功后，将admin赋予seesion
            # return 'Admin login successfully!'
            response= make_response('Admin login successfully!')
            response.set_cookie('login_time',time.strftime('%Y-%m-%d %H:%M:%S'))    #”response.set_cookie()”函数，来设置Cookie项，之后这个项值会被保存在浏览器中
            #set_cookie函数的第三个参数（max_age）可以设置该Cookie项的有效期，单位是秒，不设的话，在浏览器关闭后，该Cookie项即失效
            return response
        else:
            return 'No such user!'
    if 'user' in session:
        # return 'Hello %s!' %session['user']    #”admin”登陆成功后，再打开”login”页面就不会出现表单了
        login_time = request.cookies.get('login_time')    #在请求中，”request.cookies”对象就是一个保存了浏览器Cookie的字典，使用其”get()”函数就可以获取相应的键值
        response = make_response('Hello %s, you logged in on %s' % (session['user'], login_time))
        return response
    else:
        title = request.args.get('title','xzd')    #”request.args.get()”方法则可以获取Get请求URL中的参数，该函数的第二个参数是默认值，当URL参数不存在时，则返回默认值
        # return render_template('login.html',title=title)    #通过模板来构建响应内容
        response = make_response(render_template('login.html',title=title),200)    #构建响应对象，设置一些参数（比如响应头）后，再将其返回，”make_response”方法就是用来构建response对象的，第二个参数代表响应状态码，缺省就是200
        response.headers['key']='value'
        return response

@app.route('/logout')
def logout():
    session.pop('user',None)    #然后打开logout页面可以登出。session对象的操作就跟一个字典一样
    return redirect(url_for('login'),302)    #重定向”redirect()”函数，作用就是当客户端浏览某个网址时，将其导向到另一个网址，比如用户在未登录时浏览某个需授权的页面，我们将其重定向到登录页要求其登录先，“redirect()”的第二个参数时HTTP状态码，可取的值有301, 302, 303, 305和307，默认即302

app.secret_key = '123456dahb'    #使用session时一定要设置一个密钥”app.secret_key”，不然你会得到一个运行时错误，内容大致是”RuntimeError: the session is unavailable because no secret key was set”。密钥要尽量复杂，最好使用一个随机数，这样不会有重复
if __name__=="__main__":
    app.run(debug=True)


# #错误处理
# from flask import Flask,abort,render_template,make_response
#
# class InvalidUsage(Exception):    #定义了一个异常”InvalidUsage”
#     status_code = 400
#
#     def __init__(self,message,status_code=400):
#         Exception.__init__(self)
#         self.message = message
#         self.status_code = status_code
#
# app = Flask(__name__)
#
# @app.errorhandler(InvalidUsage)    #通过装饰器”@app.errorhandler()”修饰了函数”invalid_usage()”，装饰器中注册了我们刚定义的异常类，一但遇到”InvalidUsage”异常被抛出，这个”invalid_usage()”函数就会被调用
# def invalid_usage(error):
#     response = make_response(error.message)
#     response.status_code = error.status_code
#     return response
# @app.route('/exception')
# def exception():
#     raise InvalidUsage('No privilege to access the resource',status_code=403)    #一但遇到”InvalidUsage”异常被抛出，这个”invalid_usage()”函数就会被调用
# if __name__=="__main__":
#     app.run(debug=True)



# #url重定向
# from flask import Flask
#
# app = Flask(__name__)
# @app.route('/projects/')    #访问第一个路由不带/时，Flask会自动重定向到正确地址
# def projects():
#     return 'The project page'
#
# @app.route('/about')    #访问第二个路由时末尾带上/后Flask会直接报404 NOT FOUND错误
# def about():
#     return 'The about page'
#
# if __name__=="__main__":
#     app.run(debug=True)