import os
import sys
from pathlib import Path
import shutil

from utilities.page_utilities import generate_page, generate_pages_recursive


DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./docs"

FROM_PATH = "./content/index.md"
TEMPLATE_HTML_PATH = "./template.html"
DEST_PATH = f'./{DIR_PATH_PUBLIC}/index.html'

def main():
   base_path = sys.argv[0]

   if os.path.exists(Path(DIR_PATH_PUBLIC)):
      shutil.rmtree(Path(DIR_PATH_PUBLIC))

   make_public_dir(DIR_PATH_STATIC, DIR_PATH_PUBLIC)

   generate_pages_recursive("./content", TEMPLATE_HTML_PATH, DIR_PATH_PUBLIC, base_path)
   


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
