import asyncio

CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
SIGKILL = 9
SIGTERM = 15

class ProcessRunner:

    def __init__(self) -> None:
        self.process = None
        self.read_stdout_task = None
        self.read_stderr_task = None
    
    def __del__(self):
        if self.process is not None:
            self.process.terminate()
    
    def run_command(self, program, *args):
        self.add_log(f'{program} {args}')
        asyncio.run(self.run(program, *args))
    
    async def read_stream(self, process, stream):
        while process.returncode is None:
            try:
                line = await stream.readline()
                if line:
                    line = line.decode("utf-8")[:-1]
                    print(line)
                    #self.add_log(line)
            except (asyncio.LimitOverrunError, ValueError):
                continue

    # WARNING!
    # This code REQUIRES Python 3.11 at least!
    async def run(self, program, *args):
        try:
            self.process = await asyncio.create_subprocess_exec(program, *args, stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        finally:
            self.add_log("Run command: " + f'{program} {args}')
        # So, the current issue is:
        # Using TaskGroup reading stdout and stderr does work, but it blocks (this function exits only after it's done)
        # Without TaskGroup it doesn't block, but... tasks are never called.
        #async with asyncio.TaskGroup() as tg:
        #    self.read_stdout_task = tg.create_task(self.read_stream(self.process, self.process.stdout))
        #    self.read_stderr_task = tg.create_task(self.read_stream(self.process, self.process.stderr))
        self.read_stdout_task = asyncio.create_task(self.read_stream(self.process, self.process.stdout))
        self.read_stderr_task = asyncio.create_task(self.read_stream(self.process, self.process.stderr))


    def terminate(self):
        """ Terminate the subprocess. """
        if self.process is not None:
            self.process.terminate()

    def add_log(self, text):
        print(text)
