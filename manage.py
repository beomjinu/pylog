import json, sys, time, os

class Build:
    def __init__(self):
        self.baseTemplate = self.readFile("templates/base.html")
        self.config = json.loads(self.readFile("config.json"))

        self.writeFile("index.html", self.createIndexHtml())

    def readFile(self, filepath: str):
        with open(filepath, "r") as file:
            return file.read()
        
    def writeFile(self, filepath: str, content: str):
        with open(filepath, "w") as file:
            file.write(content)
        
    def replaceVars(self, template: str, vars: dict):
        for key, value in vars.items():
            template = template.replace("{{ " + key + " }}", value)
        return template

    def createIndexHtml(self):
        template = self.readFile("templates/index.html")
        
        vars = {
            "title": self.config["blogName"],
        }; vars.update(self.config)
        
        indexHtml = self.replaceVars(self.replaceVars(self.baseTemplate, {"template": template}), vars)
        
        return indexHtml
    
class Main:
    def __init__(self):
        self.command = sys.argv[1]
        self.options = sys.argv[1:]

        if self.command in ["help", "h", ""]:
            self._help()
        
        elif self.command in ["build", "b"]:
            self.build()


    def _help(self):
        pass

    def build(self):
        Build()

        if ("-w" in self.options) or ("--watchdog" in self.options): # watchdog
            # clear terminal
            if os.name == "nt": # Windows
                os.system("cls")
            else: # macOS / Linux
                os.system("clear")


            print("Pylog watchdog build (manage.py) \n")

            file_last_modified = {}
            folder_paths = ["templates/", "static/", "media/"]

            try:
                while True:
                    for folder_path in folder_paths:
                        for root, _, files in os.walk(folder_path):
                            for file in files:
                                file_path = os.path.join(root, file)
                                last_modified = os.path.getmtime(file_path)

                                if file_path in file_last_modified:
                                    if last_modified != file_last_modified[file_path]:
                                        file_last_modified[file_path] = last_modified

                                        print(f"Modified File: {file_path}")
                                        Build()
                                        
                                        break
                                else:
                                    file_last_modified[file_path] = last_modified

                        time.sleep(0.5) 
            except KeyboardInterrupt:
                os._exit(0)

        


if __name__ == "__main__":
    Main()