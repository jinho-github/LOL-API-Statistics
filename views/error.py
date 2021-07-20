from flask import Flask, Blueprint, render_template


err = Blueprint('err', __name__)

#에러페이지 404, 500
@err.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@err.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500