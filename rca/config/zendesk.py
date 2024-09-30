from oslo_config import cfg
import sys

GROUP_NAME = __name__.split('.')[-1]

ALL_OPTS = [
    cfg.StrOpt('url', default='https://devstack.zendesk.com/api/v2/'),
    cfg.StrOpt('user_email', default='test@devstack.co.kr'),
    cfg.StrOpt('admin_email', default='admin@devstack.co.kr'),
    cfg.StrOpt('token', default='ddddddddddddddddddddddd'),
]

def register_opts(conf):
    conf.register_opts(ALL_OPTS, group=GROUP_NAME)
