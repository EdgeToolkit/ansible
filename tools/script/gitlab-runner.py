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

    def _flush(self):
        folder = os.path.dirname(self._path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(self._path, 'w') as f:
            yaml.safe_dump(self._runner, default_flow_style=False)


class GitlabRunner(object):
    # Type
    BUILDER = 'builder'
    RUNNER = 'runner'
    DEPLOYER = 'deployer'

    def __init__(self, config, record, type, hostname, bundle=None, property=None):
        """
        config_file
        rec_file: gitlab runner token , id record files
        """
        self._type = type
        self._hostname = hostname
        self._bundle = bundle        
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
        group = self._config['gitlab'].get('group') or None
        hash = {'hostname': self._hostname,
        'type': self._type,
        'bundle': self._bundle,
        'group': group,
        'property': self._property,        
        }
        return hash

    def register(self):
        if self.get() is None:
            description = f"{self._hostname}/{self._type}"
            token = self._config['gitlab']['register_token']
            hash = yaml.safe_dump(self.hash, default_flow_style=False)
            print(hash)
            runner = self.gitlab.runners.create({'token': token,
                                      'description': description,
                                      'info': {'name': hash}
                                      })
            self._record.set(runner.id, runner.token, hash=self.hash)

    def delete(self):
        runner = self.get()
        if runner:
            runner.delete()

    def get(self):
        for runner in self.gitlab.runners.list():
            try:
                hash = yaml.safe_load(runner.name or "")
                if hash ==  self.hash:
                    return runner
            except Exception as e:                
                pass
        return None

    def update(self, tags):
        pass



if __name__ == '__main__':
    runner = GitlabRunner('~/.edgetoolkit/config/gitlab-runner/oss.yml', '~/.edgetoolkit/config/gitlab-runner/runner-db.yml',
    GitlabRunner.BUILDER, hostname="1.2.3.4", bundle='toolset', group='oss',
    property={'a': 'b', 'c':'d'})
    runner.register()