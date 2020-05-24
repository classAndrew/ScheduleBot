class DataHandler:
    directory = "./data"
    @classmethod
    def write(cls, guild_id, task_name, due):
        with open(f'{cls.directory}/{guild_id}', 'a') as f:
            f.write(f"\"{task_name}\" {due}\n")
    @classmethod
    def get(cls, guild_id):
        try:
            with open(f'{cls.directory}/{guild_id}', 'r') as f:
                contents = f.read()
                ldata = contents.split("\n")
            if not contents:
                return
        except FileNotFoundError:
            return
        return [cls.parse_line(x) for x in ldata]
    #stringtools
    @classmethod
    def parse_line(cls, line):
        # "nested "test""
        # line[::-1].index('"')
        pos = -1
        for i in range(len(line)):
            if line[len(line)-i-1] == "\"":
                pos = len(line)-i-1
                break
        return [line[1:pos], line[pos+1:]]
    @classmethod
    def remove_task(cls, server, name):
        try:
            with open(f'{cls.directory}/{server}', 'r') as f:
                contents = f.read()
                ldata = contents.split("\n")
            if not contents:
                return
            found = False
            parsed = [cls.parse_line(x) for x in ldata]
            ctr = 0
            for task in parsed:
                if task[0] == name:
                    found = True
                    parsed.pop(ctr)
                    ctr -= 1
                ctr += 1
            if not found:
                return False
            with open(f'{cls.directory}/{server}', 'w') as f:
                f.write('\n'.join(''.join(x) for x in parsed))
            return True
        except FileNotFoundError:
            return