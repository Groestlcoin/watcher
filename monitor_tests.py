import unittest

import os

from app import create_app
from models import db, Checkpoint
from monitor import checkpoint

os.environ['MONITOR_CONFIG'] = 'test_config.py'


class MonitorTestCase(unittest.TestCase):
    def setUp(self):
        self.real_app = create_app()
        self.real_app.testing = True
        self.app = self.real_app.test_client()
        self.context = self.real_app.app_context()
        self.context.push()
        db.create_all()

    def tearDown(self):
        self.context.pop()

    def test_checkpoint_none_existing(self):
        checkpoint('00000082c779d1f4468f34946468c1c7ebabd147d359b5e218e999a0e911282f')
        c = Checkpoint.query.filter_by(hash='00000082c779d1f4468f34946468c1c7ebabd147d359b5e218e999a0e911282f').one()
        assert c.hash == '00000082c779d1f4468f34946468c1c7ebabd147d359b5e218e999a0e911282f'

    def test_checkpoint_existing(self):
        c = Checkpoint(hash='00000082c779d1f4468f34946468c1c7ebabd147d359b5e218e999a0e911282f')
        db.session.add(c)
        db.session.commit()
        checkpoint('0000000b49a3b3d373838c3e1c14d294abdc31457b8d7f69ac0d3002a287f194')

        new_checkpoint = Checkpoint.query.filter_by(
            hash='0000000b49a3b3d373838c3e1c14d294abdc31457b8d7f69ac0d3002a287f194').one()
        assert new_checkpoint.hash == '0000000b49a3b3d373838c3e1c14d294abdc31457b8d7f69ac0d3002a287f194'
