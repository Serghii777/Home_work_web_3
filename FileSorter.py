import shutil
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import re
import aiofiles
import concurrent.futures

class FileSorter:
    def __init__(self, source_folder):
        self.source_folder = source_folder
        self.file_handlers = []

    def add_handler(self, handler):
        self.file_handlers.append(handler)

    async def scan(self, folder):
        loop = asyncio.get_running_loop()
        with ThreadPoolExecutor() as executor:
            futures = []
            for item in folder.iterdir():
                if item.is_dir():
                    if item.name not in ('архіви', 'відео', 'аудіо', 'документи', 'зображення', 'ІНШЕ'):
                        futures.append(loop.run_in_executor(executor, self.scan, item))
                else:
                    futures.extend(loop.run_in_executor(executor, handler.handle, item, self.source_folder) for handler in self.file_handlers if handler.can_handle(item))
            await asyncio.gather(*futures)

    async def core(self):
        await self.scan(self.source_folder)

class FileHandler:
    def can_handle(self, file):
        raise NotImplementedError

    async def handle(self, file, target_folder):
        raise NotImplementedError

    def get_extension(self, name):
        return Path(name).suffix[1:].upper()

    def normalize(self, name):
        MAP = {}
        CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
        TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                       "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

        for cirilic, latin in zip(CYRILLIC_SYMBOLS, TRANSLATION):
            MAP[ord(cirilic)] = latin
            MAP[ord(cirilic.upper())] = latin.upper()

        string = name.translate(MAP)
        translated_name = re.sub(r'[^a-zA-Z.0-9_]', '_', string)
        return translated_name

class ImageHandler(FileHandler):
    def can_handle(self, file):
        return file.suffix[1:].upper() in ('JPEG', 'JPG', 'PNG', 'SVG')

    async def handle(self, file, target_folder):
        target_folder.mkdir(exist_ok=True, parents=True)
        await self._copy_file(file, target_folder / self.normalize(file.name))

    async def _copy_file(self, source, destination):
        async with aiofiles.open(source, 'rb') as source_file:
            async with aiofiles.open(destination, 'wb') as destination_file:
                await destination_file.write(await source_file.read())

# Аналогічні зміни робляться і для інших FileHandler

if __name__ == "__main__":
    def start():
        folder_process = Path('.')  # Змініть шлях до вашої папки, якщо потрібно
        file_sorter = FileSorter(folder_process)

        file_sorter.add_handler(ImageHandler())
        # Додайте інші обробники за необхідності

        asyncio.run(file_sorter.core())

    start()