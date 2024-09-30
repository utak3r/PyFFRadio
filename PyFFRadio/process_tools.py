import asyncio

CTRL_C_EVENT = 0
CTRL_BREAK_EVENT = 1
SIGKILL = 9
SIGTERM = 15

class RadioStreamDescription:

    # Sample output from ffplay:
    # Input #0, mp3, from 'https://an.cdn.eurozet.pl/ant-web.mp3':
    # Metadata:
    #     icy-br          : 128
    #     icy-description : Antyradio Warszawa
    #     icy-genre       : Rock
    #     icy-name        : Antyradio Warszawa
    #     icy-private     : 1
    #     icy-pub         : 0
    #     icy-url         : http://www.antyradio.pl
    #     StreamTitle     :
    # Duration: N/A, start: 0.000000, bitrate: 128 kb/s
    # Stream #0:0: Audio: mp3, 44100 Hz, stereo, fltp, 128 kb/s

    def __init__(self) -> None:
        self.bitrate = 0 # icy-br
        self.description = '' # icy-description
        self.genre = '' # icy-genre
        self.name = '' # icy-name
        self.url = '' # icy-url
        self.stream_title = '' # StreamTitle
        self.format = '' # Audio: mp3
    
    def __str__(self):
        return f'Name: {self.name}, genre: {self.genre}, description: {self.description}, bitrate: {self.bitrate}, stream title: {self.stream_title}'


class ProcessRunner:

    def __init__(self) -> None:
        self.process = None
        self.read_stdout_task = None
        self.read_stderr_task = None
        self.info = None
    
    def __del__(self):
        if self.process is not None:
            self.process.terminate()
    
    def run_command(self, program, *args):
        self.add_log(f'{program} {args}')
        asyncio.run(self.run(program, *args))
    
    async def read_process_output(self, process):
        while process.returncode is None:
            line = await process.stdout.readline()
            if line:
                #print(line.decode('utf-8').rstrip())
                if self.analyze_stream_output(line.decode('utf-8').rstrip()):
                    break
            await asyncio.sleep(0.1)

    # WARNING!
    # This code REQUIRES Python 3.11 at least!
    async def run(self, program, *args):
        try:
            # Redirect stderr to stdout
            self.process = await asyncio.create_subprocess_exec(program, *args, stdin=asyncio.subprocess.DEVNULL, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)
        finally:
            self.add_log("Run command: " + f'{program} {args}')
        # So, the current issue is:
        # Using TaskGroup reading stdout and stderr does work, but it blocks (this function exits only after it's done)
        # Without TaskGroup it doesn't block, but... tasks are never called.
        #
        # So, the current solution to this, is to read the output only to the point
        # we get all the stream info, and stop reading after that point.
        # This way it unblocks after few seconds.
        # See: read_process_output(self, process) and analyze_stream_output(self, input_line)
        self.info = RadioStreamDescription()
        async with asyncio.TaskGroup() as tg:
           self.read_stdout_task = tg.create_task(self.read_process_output(self.process))
        print(self.info)


    def terminate(self):
        """ Terminate the subprocess. """
        if self.process is not None:
            self.process.terminate()
            del self.info
            self.info = None

    def add_log(self, text):
        print(text)

    def analyze_stream_output(self, input_line) -> bool:
        is_end_of_info = False
        if 'icy-description' in input_line:
            vals = input_line.split(':')
            self.info.description = vals[1]
        if 'icy-genre' in input_line:
            vals = input_line.split(':')
            self.info.genre = vals[1]
        if 'icy-name' in input_line:
            vals = input_line.split(':')
            self.info.name = vals[1]
        if 'icy-url' in input_line:
            vals = input_line.split(':')
            self.info.url = vals[1]
        if 'StreamTitle' in input_line:
            vals = input_line.split(':')
            self.info.stream_title = vals[1]
        if 'icy-br' in input_line:
            vals = input_line.split(':')
            self.info.bitrate = vals[1]
        if 'Stream #' in input_line:
            audio_start = input_line.find('Audio: ')
            audio_end = input_line.find(',', audio_start)
            self.info.format = input_line[audio_start+7:audio_end]
            is_end_of_info = True

        return is_end_of_info
