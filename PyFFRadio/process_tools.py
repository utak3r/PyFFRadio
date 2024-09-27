import asyncio

CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
SIGKILL = 9
SIGTERM = 15

class ProcessRunner:

    def __init__(self) -> None:
        self.process = None
    
    def __del__(self):
        self.terminate()
    
    def run_command(self, program, *args):
        self.add_log(f'{program} {args}')
        asyncio.run(self.run(program, *args))
    
    async def read_stream(self, stream):
        while self.process.returncode is None:
            try:
                line = await stream.readline()
            except (asyncio.LimitOverrunError, ValueError):
                continue
            if line:
                line = line.decode("utf-8")[:-1]
                print(line)
                self.add_log(line)
            else:
                break

    # WARNING!
    # This code REQUIRES Python 3.11 at least!
    async def run(self, program, *args):
        try:
            self.process = await asyncio.create_subprocess_exec(program, *args, stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            async with asyncio.TaskGroup() as tg:
                read_stdout_task = asyncio.create_task(self.read_stream(self.process.stdout))
                read_stderr_task = asyncio.create_task(self.read_stream(self.process.stderr))
        finally:
            self.add_log("Running command has finished: " + f'{program} {args}')


    def terminate(self):
        """ Terminate the subprocess. """
        if self.process is not None:
            self.process.terminate()

    def add_log(self, text):
        print(text)
