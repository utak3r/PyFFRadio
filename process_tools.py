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
    
    def run_command(self, command):
        self.add_log(command)
        asyncio.run(self.run(command))
    
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

    async def run(self, command):
        try:
            self.process = await asyncio.create_subprocess_shell(command, stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            async with asyncio.TaskGroup() as tg:
                read_stdout_task = asyncio.create_task(self.read_stream(self.process.stdout))
                read_stderr_task = asyncio.create_task(self.read_stream(self.process.stderr))
        finally:
            self.add_log("Running command has finished: " + command)


    def terminate(self):
        """ Terminate the subprocess. """
        if self.process is not None:
            # Somehow terminate doesn't work for ffplay, it behaves best, when killed with CTRL_BREAK_EVENT
            self.process.send_signal(CTRL_BREAK_EVENT)
            #self.process.terminate()

    def add_log(self, text):
        print(text)
