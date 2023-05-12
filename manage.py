import json, sys

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
        if ("-w" in self.options) or ("--watchdog" in self.options):
            pass
        else:
            Build()

if __name__ == "__main__":
    Main()