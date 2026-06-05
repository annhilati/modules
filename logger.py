from pathlib import Path
from datetime import datetime
import rich, dataclasses, inspect

@dataclasses.dataclass
class Logger:
    stack: list[str] = dataclasses.field(init=False, default_factory=list)
    
    def log(self, msg: str):
        source = ".".join(
            [f.function for f in inspect.stack()[::-1][:-1]]
        )
        message = datetime.now().strftime(r"%Y-%m-%d %H:%M:%S") + f" [{source}] " + msg
        rendered = rich.print

        print(rendered)
        self.stack.append(message)
        
    def savelog(self, path: Path | str, overwrite: bool = False) -> None:
        path = Path(path)
        
        if path.exists() and not overwrite:
            raise FileExistsError
        
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as f:
            f.write("\n".join(self.stack))
            
def main():
    console = Logger()
    console.log("Hallo")
    console.savelog("log.log", overwrite=True)
    
main()