# A list of common file extensions that we might want to exclude from crawling
UNDESIRED_EXTENSIONS = (
    # Documents
    ".pdf",
    ".doc",
    ".docx",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".odt",
    ".rtf",
    # Archives
    ".zip",
    ".rar",
    ".7z",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    # Images
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".tiff",
    ".svg",
    ".ico",
    # Audio
    ".mp3",
    ".wav",
    ".flac",
    ".aac",
    ".ogg",
    # Video
    ".mp4",
    ".avi",
    ".mkv",
    ".mov",
    ".wmv",
    ".flv",
    ".webm",
    # Executables
    ".exe",
    ".msi",
    ".bat",
    ".sh",
    ".app",
    ".jar",
    ".com",
    ".cmd",
    # Compressed Files
    ".7z",
    ".rar",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    # Fonts
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
    ".eot",
    # Data Formats
    ".csv",
    ".json",
    ".xml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    # Markup and Text
    ".css",
    ".js",
    ".txt",
    ".md",
    ".log",
    ".xml",
    # Backup and Temporary Files
    ".bak",
    ".swp",
    ".tmp",
    ".temp",
    ".old",
    # Miscellaneous
    ".dat",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".dbf",
    ".ini",
    # CAD and 3D Model Formats
    ".obj",
    ".stl",
    ".fbx",
    ".dxf",
    ".dwg",
    ".step",
    ".iges",
    # Game Files
    ".unitypackage",
    ".blend",
    ".gltf",
    ".glb",
    ".3ds",
    ".obj",
    ".fbx",
    # Office Files
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
    ".pps",
    ".pot",
    ".pub",
    ".vsd",
    # Configuration Files
    ".config",
    ".conf",
    ".cfg",
    ".json",
    ".yml",
    ".yaml",
    ".xml",
    ".ini",
    # Vector Graphics
    ".svg",
    ".ai",
    ".eps",
    ".cdr",
    # Virtual Machine Files
    ".vmdk",
    ".ova",
    ".ovf",
    ".vmx",
    ".qcow2",
    # eBooks and ePubs
    ".epub",
    ".mobi",
    ".azw",
    ".azw3",
    ".fb2",
    # GIS and Map Files
    ".shp",
    ".kml",
    ".kmz",
    ".gpx",
    ".geojson",
    # Project Files
    ".project",
    ".workspace",
    ".sln",
    ".vcxproj",
)

# Covers many common schemes that are typically not desirable for web crawling
UNDESIRED_SCHEMES = ("mailto", "javascript", "tel", "data", "ftp", "file")