import __hpx__ as hpx
import enum
import json

log = hpx.get_logger(__name__)

class DataType(enum.Flag):
    eze = enum.auto()
    hdoujin = enum.auto()
    e_hentai_downloader = enum.auto()

filetypes = ('.json', '.txt')
filenames = {
    "info.json": DataType.eze | DataType.hdoujin,
    "info.txt": DataType.hdoujin | DataType.e_hentai_downloader,
    }

common_data = {
    'titles': None, # [(title, language),...]
    'artists': None, # [(artist, (circle, circle, ..)),...]
    'category': None,
    'tags': None, # [tag, tag, tag, ..] or {ns:[tag, tag, tag, ...]}
    'pub_date': None, # DateTime object
    'language': None,
    'urls': None # [url, ...]
}

extractors = {}

def capitalize_text(text):
    """
    better str.capitalize
    """
    return " ".join(x.capitalize() for x in text.strip().split())

def register_extractor(cls, type):
    assert issubclass(cls, Extractor)
    assert isinstance(type, DataType)
    extractors[type] = cls()

class Extractor:
    """
    """

    def file_to_dict(self, fs: hpx.command.CoreFS) -> dict:
        """
        """
        try:
            d = {}
            log.debug(f"File ext: {fs.ext}")
            kw = {}
            if not fs.inside_archive:
                kw['encoding'] = 'utf-8'
            if fs.ext.lower() == '.json':
                with fs.open("r", **kw) as f:
                    d = json.load(f)
            elif fs.ext.lower() == '.txt':
                with fs.open("r", **kw) as f:
                    for line in f.readlines():
                        l = line.strip()
                        k, v = l.split(b':' if fs.inside_archive else ':', 1 )
                        if k.strip():
                            d[k.strip()] = v.strip()
            else:
                raise NotImplementedError(f"{fs.ext} filetype not supported yet")
        except Exception:
            log.warning("An error occured while trying to parse file into a dict")
            raise ValueError
        return d

    def extract(self, filedata: dict) -> dict:
        """
        """
        raise NotImplementedError