from oslo_config import cfg
from config import default, cors, zendesk, jaeger

CONF = cfg.CONF

conf_modules = [default, cors, zendesk, jaeger]

def configure(conf=None, config_file_path="/etc/rca/rca.conf"):
    if conf is None:
        conf = CONF

    for module in conf_modules:
        module.register_opts(conf)

    CONF(['--config-file=' + config_file_path], project='rca')
