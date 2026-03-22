import asyncio
import os.path
import sys
from asyncio.subprocess import Process

from aio_mcserver.config import AppConfig


class Server:
    proc: Process

    def __init__(self, conf: AppConfig, launch_only: bool = False):
        self.conf = conf
        self.launch_only = launch_only

        if sys.platform == "win32":
            self.startup_cmd = [
                "cmd.exe", "/c",
                os.path.join(".", "run.bat"),
            ]
        else:
            self.startup_cmd = [
                "bash",
                os.path.join(".", "run.sh"),
            ]

    async def watch_stdin(self):
        loop = asyncio.get_running_loop()
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)

            if not line:
                break
            if self.proc.returncode is not None:
                break

            if not self.proc.stdin.is_closing():
                self.proc.stdin.write(line.encode())
                await self.proc.stdin.drain()

    async def read_and_print(self, stream, buffer):
        while True:
            line = await stream.readline()
            if not line:
                break
            if self.launch_only and b'For help, type "help"' in line:
                self.proc.stdin.write(b"stop\n")

            buffer.write(line)
            buffer.flush()

    async def start(self):
        self.proc = await asyncio.create_subprocess_exec(
            *self.startup_cmd,
            cwd=self.conf.server.path,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.gather(
            self.watch_stdin(),
            self.read_and_print(self.proc.stdout, sys.stdout.buffer),
            self.read_and_print(self.proc.stderr, sys.stderr.buffer),
        )

    async def wait(self):
        await self.proc.wait()
