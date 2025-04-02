import os
from pathlib import Path, PurePath
import shutil

from nodes.textnode import TextNode
from nodes.htmlnode import HTMLNode


DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"

def main():
   if os.path.exists(Path(DIR_PATH_PUBLIC)):
      shutil.rmtree(Path(DIR_PATH_PUBLIC))
      
   make_public_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)



def make_public_dir(source_path: Path, dest_path: Path) -> None:
   """Recursively create public folder from static."""

   source_path = Path(source_path)
   if not source_path.exists():
      raise FileNotFoundError(f"Source path does not exist: {source_path}")
    
   dest_path = Path(dest_path)
   dest_path.mkdir(parents=True, exist_ok=True)
   
   for item in source_path.iterdir():
      from_path = source_path / item.name
      to_path = dest_path / item.name

      if item.is_file():
         shutil.copy2(from_path, to_path)

      elif item.is_dir():
         make_public_dir(from_path, to_path)   


if '__main__' == __name__:
   main()
