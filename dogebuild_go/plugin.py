from typing import Union, Tuple, Dict, List
from subprocess import run
from pathlib import Path
from os import environ
import re
from shutil import copytree

from dogebuild.plugins import DogePlugin
from dogebuild.tools import Environment


class Go(DogePlugin):
    NAME = "go"

    def __init__(self, build_dir: Union[Path, str] = 'build', src_dir: Union[Path, str] = 'src'):
        super(Go, self).__init__(artifacts_to_publish=['go_path'])

        self.go = 'go'

        self.build_dir = Path(build_dir).resolve()
        self.src_dir = Path(src_dir).resolve()

        self.add_task(self.test, phase='test'),
        self.add_task(self.build, phase='build')
        self.add_task(self.run, phase='run')
        self.add_task(self.clean, phase='clean')

    def test(self, go_path):
        if not self.build_dir.exists():
            self.build_dir.mkdir(parents=True, exist_ok=True)

        module_name = self._extract_module_name()

        go_path_src_dir = self.build_dir / 'src' / module_name
        copytree(self.src_dir, go_path_src_dir, dirs_exist_ok=True)

        with Environment({"GOPATH": ':'.join(map(str, ['/home/su0/go'] + go_path + [self.build_dir]))}):
            print(environ['GOPATH'])
            run(
                [
                    self.go,
                    'test',
                ],
                check=True,
                cwd=go_path_src_dir,
            )
        return 0, {}

    def build(self, go_path) -> Tuple[int, Dict[str, List[Path]]]:
        if not self.build_dir.exists():
            self.build_dir.mkdir(parents=True, exist_ok=True)

        module_name = self._extract_module_name()

        go_path_src_dir = self.build_dir / 'src' / module_name
        copytree(self.src_dir, go_path_src_dir, dirs_exist_ok=True)

        with Environment({"GOPATH": ':'.join(map(str, ['/home/su0/go'] + go_path + [self.build_dir]))}):
            print(environ["GOPATH"])
            run(
                [
                    self.go,
                    'install',
                ],
                check=True,
                env=environ,
                cwd=go_path_src_dir,
            )

        return 0, {
            'go_path': [self.build_dir],
        }

    def run(self):
        run(
            [
                self.go,
                'run',
                '.',
            ],
            check=True,
        )
        return 0, {}

    def clean(self):
        run(
            [
                self.go,
                'run',
            ],
            check=True,
        )
        return 0, {}

    def _extract_module_name(self):
        match = re.search(r'module (.+)', (self.src_dir / 'go.mod').read_text())
        if match:
            return match.group(1)
        else:
            raise Exception('Cannot define package')
