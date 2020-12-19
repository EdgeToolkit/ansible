#!/usr/bin/env python3
import os
import sys
import yaml

import os
import gitlab


#from conans.tools import ConanOutput
import gitlab

class GitlabRunnerRecord(object):

    def __init__(self, path):
        self._path = os.path.abspath(os.path.expanduser(path))
        self._runner = {}        

    def delete(self, id):
        if id in self._runner:
            del self._runner[token]
            self._flush()

    def set(self, id, token, hash=None):
        self._runner[id] = {'token': token, 'hash': hash }
        self._flush()
        
    def token(self, id):
        return self._runner.get(id) or None

class GitlabRunner(object):
    # Type
    BUILDER = 'builder',
    RUNNER = 'runner',
    DEPLOYER = 'deployer'

    def __init__(self, config, record, type, hostname, bundle=None, group=None, property=None):
        """
        config_file
        rec_file: gitlab runner token , id record files
        """
        self._type = type
        self._hostname = hostname
        self._bundle = bundle
        self._group = group
        self._property = property
        self._gitlab = None
        self._record = GitlabRunnerRecord(record)
        path = os.path.abspath(os.path.expanduser(config))
        with open(path) as f:
            self._config = yaml.safe_load(f)
            self._config['__file__'] = path

    @property
    def gitlab(self):
        if self._gitlab is None:
            url = self._config['gitlab']['url']
            token = self._config['gitlab']['private_token']
            self._gitlab = gitlab.Gitlab(url, private_token=token)
        return self._gitlab

    @property
    def hash(self):
        hash = {'hostname': self._hostname,
        'type': self._type,
        'bundle': self._bundle,
        'property': self._property,
        'group': self._group,
        }
        return hash

    def name(self):
        name = f"{self._hostname}/{self._type}"
        if self._group:
            name = f"{self._group}:{name}"
        if self._bundle:
            name = f"{name}/{self._bundle}"
        if self._device:
            name = f"{name}[{self._device}]"
        return name

    def register(self):
        if self.get() is None:
            token = self._config['gitlab']['register_token']
            runner = gitlab.runners.create({'token': token,
                                      'description': self.name,
                                      'info': {'name': self.name}
                                      })
            self.db.add(runner.id, runner.token, hash=self.hash)

    def delete(self):
        runner = self.get()
        if runner:
            runner.delete()

    def get(self):
        for runner in self.gitlab.runners.list():
            hash = yaml.safe_load(runner.name or "")
            if cmp(hash, self.hash):
                return runner
        return None

    def update(self, tags):
        pass
    


if __name__ == '__main__':
    runner = GitlabRunner('~/.edgetoolkit/config/gitlab-runner/oss.yml', '~/.edgetoolkit/config/gitlab-runner/runner-db.yml',
    GitlabRunner.BUILDER, hostname="1.2.3.4", bundle='toolset', group='oss')
    runner.register()