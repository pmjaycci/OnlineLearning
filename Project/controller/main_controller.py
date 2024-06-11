from flask import Blueprint, Flask, redirect, render_template, request, session, url_for
from model.main import Main, Account

main = Blueprint('main', __name__)


@main.route('/')
def index():
    # 세션에서 사용자 이름을 가져옵니다.
    login_user = '로그인되지 않은 상태입니다.'
    is_login = False
    if "user_id" in session:
        login_user = f'안녕하세요, {session.get('user_id')}님!'
        is_login = True
    rows = Main.learn_load()
    return render_template('index.html', login_user=login_user, is_login=is_login, rows=rows)


@main.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    Account.login_check(username, password)
    print(f"Name [{username}]/[{password}]")
    return redirect(url_for('main.index'))


@main.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
