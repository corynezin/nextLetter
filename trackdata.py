import os
import subprocess
import hashlib

class Source(object):
    def __init__(self, repo, sha, token):
        shasha = hashlib.sha1(sha.encode('utf8')).hexdigest()
        self.opt = f"--git-dir={shasha}/.git --work-tree={shasha}"
        if not os.path.isdir(shasha):
            os.system(f"git clone {repo} {shasha}")
        os.system(f"git {self.opt} reset --hard {sha}")
        self.path_prefix = os.path.abspath(shasha)

    def get(self, path):
        path = os.path.join(self.path_prefix, path)
        if os.path.isdir(path):
            for filepath in os.listdir(path):
                with open(os.path.join(path, filepath)) as f:
                    yield f.read()
        elif os.path.isfile(path):
            with open(path) as f:
                return f.read()

    def add(self, path, dependencies, code):
        import pdb; pdb.set_trace()
        os.system(f"git {self.opt} status")
        os.system(f"git {self.opt} add {path}")
        os.system(f"git {self.opt} status")
        sha = subprocess.check_output('git rev-parse HEAD', shell=True)
        gitstr = f"git {self.opt} commit -m 'add {path}' -m 'depends on: {', '.join(dependencies)}\n{sha}'"
        os.system(gitstr)

    def listdir(self, path):
        path = os.path.join(self.path_prefix, path)
        if not os.path.isdir(path):
            raise ValueError("Path provided is not a directory")
        for filepath in os.listdir(path):
            yield filepath
    
    def writer(self, path, code_file):
        return Writer(self, path, code_file)

class Writer(object):
    def __init__(self, source, path, code_file):
        self.source = source
        self.path = path
        self.code_file = code_file
        self.paths = []

    def get(self, path):
        self.paths.append(path)
        return self.source.get(path)

    def write(self, content):
        self.fp.write(content)

    def __enter__(self):
        path = os.path.join(self.source.path_prefix, self.path)
        self.fp = open(path, 'w')
        return self

    def __exit__(self, type_, value, traceback):
        with open(self.code_file) as f:
            self.source.add(self.path, dependencies=self.paths, code=f.read())
        self.fp.close()
        print(self.paths)

class Snapshot(object):
    def __init__(self, token, branch, repo):
        self.branch = branch

    def __enter__(self):
        import pdb; pdb.set_trace()
        os.system(f"git branch {self.branch}")
        os.system(f"git checkout {self.branch}")
        os.system(f"git add *")
        os.system(f"git commit -m 'automatic commit'")

    def __exit__(self, type_, value, traceback):
        os.system(f"git checkout master")
