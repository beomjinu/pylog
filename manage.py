import argparse, json

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
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command")

    args = parser.parse_args()

    if args.command == "build":
        build = Build()
    else:
        raise ValueError('Unknown command: {}'.format(args.command))

if __name__ == "__main__":
    main()