from blueprint.linode_server import linode_server
from blueprint.linode_token import linode_token
from blueprint.panel import panel
from blueprint.public import public
from main import app

app.register_blueprint(public, url_prefix='/')
app.register_blueprint(panel, url_prefix='/panel')
app.register_blueprint(linode_token, url_prefix='/linode_token')
app.register_blueprint(linode_server, url_prefix='/linode_server')
