from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f'''
    <h1>🎉 我的 Flask 网站运行成功！</h1>
    <p>✅ <strong>状态</strong>: 从GitHub自动部署</p>
    <p>✅ <strong>当前时间</strong>: {current_time}</p>
    <p>✅ <strong>部署方式</strong>: GitHub + PythonAnywhere</p>
    <p>🎯 <strong>测试功能</strong>: 显示实时时间</p>
    <hr>
    <a href="/about">关于我们</a> | <a href="/contact">联系方式</a>
    '''

@app.route('/about')
def about():
    return '''
    <h2>关于这个网站</h2>
    <p>这是一个完整的 Flask 应用演示</p>
    <p>✅ 本地开发环境 (D盘)</p>
    <p>✅ GitHub 版本控制</p>
    <p>✅ PythonAnywhere 生产环境</p>
    <a href="/">返回首页</a>
    '''

@app.route('/contact')
def contact():
    return '''
    <h2>联系我们</h2>
    <p>这是一个联系页面示例</p>
    <p>📧 邮箱: example@example.com</p>
    <a href="/">返回首页</a>
    '''

if __name__ == '__main__':
    app.run(debug=True)