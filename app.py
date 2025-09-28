from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>我的 Flask 网站</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 40px auto; padding: 20px; }}
            h1 {{ color: #333; }}
            .info {{ background: #f5f5f5; padding: 15px; border-radius: 5px; }}
            a {{ color: #007bff; text-decoration: none; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>🎉 我的 Flask 网站</h1>
        <div class='info'>
            <p>✅ <strong>状态</strong>: 正常运行中</p>
            <p>📍 <strong>开发环境</strong>: D盘 (D:/F/my_flask_app)</p>
            <p>🕒 <strong>最后更新</strong>: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            <p>🐍 <strong>Python 版本</strong>: 3.13</p>
        </div>
        
        <h3>网站功能</h3>
        <ul>
            <li><a href='/'>首页</a></li>
            <li><a href='/about'>关于我们</a></li>
            <li><a href='/contact'>联系方式</a></li>
            <li><a href='/api/status'>API 状态</a></li>
        </ul>
    </body>
    </html>
    '''

@app.route('/about')
def about():
    return '''
    <h2>关于这个网站</h2>
    <p>这是一个使用 Flask 框架构建的演示网站。</p>
    <p>主要用于学习 Web 开发和 Python 编程。</p>
    <a href='/'>返回首页</a>
    '''

@app.route('/contact')
def contact():
    return '''
    <h2>联系我们</h2>
    <p>如有问题，可以通过以下方式联系：</p>
    <ul>
        <li>邮箱: example@example.com</li>
        <li>GitHub: 你的GitHub用户名</li>
    </ul>
    <a href='/'>返回首页</a>
    '''

@app.route('/api/status')
def api_status():
    return {
        'status': 'online',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    }

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
