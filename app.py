from flask import Flask, render_template
from datetime import datetime
from ota_manager import ota_bp  # 导入OTA蓝图

app = Flask(__name__)
app.register_blueprint(ota_bp)  # 注册OTA蓝图

@app.route('/')
def home():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template('index.html', current_time=current_time)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/auto-deploy-test')
def auto_deploy_test():
    return "自动部署测试成功！部署时间：" + str(datetime.now())

if __name__ == '__main__':
    app.run(debug=True)
