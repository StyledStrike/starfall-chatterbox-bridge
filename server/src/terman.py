import logger

"""
    A basic class to handle terminal commands and main program loop.
"""
class TerminalManager():
    def __init__(self):
        self.commands = {}

        def helpCallback(args, rawargs):
            for name in self.commands:
                helpText = self.commands[name]["helpText"]
                logger.info(f"{logger.highlight(name)}\t-\t{helpText}")

        self.addCommand("help", "Show a list of commands", helpCallback)

    def runForever(self):
        while True:
            try:
                data = input("> ")

                if "exit" == data:
                    break

                self._onLine(data)

            except KeyboardInterrupt:
                break
            
            except Exception as e:
                logger.error(e)
                break

        logger.info("Bye!")

    def addCommand(self, name: str, helpText: str, callback):
        self.commands[name] = {
            "helpText": helpText,
            "callback": callback
        }

    def _onLine(self, line: str):
        if len(line) == 0:
            return
        
        line = line.strip()
        args = line.split()
        name = args.pop(0)

        cmd = self.commands.get(name, None)

        if cmd is None:
            logger.error(f"Command not found: {logger.highlight(name)}")
        else:
            cmd["callback"](args, " ".join(args))
