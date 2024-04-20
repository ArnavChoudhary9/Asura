import os, sys
import pathlib

toBuild = sys.argv[1]
config = "r"

if len(sys.argv) == 3:
    config = sys.argv[2]

toCollect = [
    "Asura", toBuild,
    "PIL", "imgui",
    "OpenGL", "tkinter", "debugpy",
    "xmlrpc"
]

hiddenImports = (
    "spdlog", "yaml", "pywavefront",
    "dataclasses", "esper", "pyrr",
    "cProfile", "pstats", "uuid"
)

currdir = pathlib.Path(sys.path[0]).parent
collects = " ".join([f"--collect-all {package}" for package in toCollect])
hiddenImports = " ".join([f"--hidden-import {package}" for package in hiddenImports])

additionals = " ".join([
    "--noconsole" if config == "r" else ""
])

commands = [
    f"PyInstaller --path \"{currdir}\" {collects} {hiddenImports} {additionals} \"{toBuild}\\{toBuild}\".py",

    f"xcopy /s \"Build\\Essentials\" \"dist\\{toBuild}\"",
    f"copy \".\\imgui.ini\" \"dist\\{toBuild}\\\"",

    f"mkdir \"dist\\{toBuild}\\Asura\\InternalAssets\"",
    f"xcopy /s /i \"Asura\\InternalAssets\" \"dist\\{toBuild}\\Asura\\InternalAssets\"",

    f"mkdir \"dist\\{toBuild}\\Resources\"",
    f"xcopy /s /i \"{toBuild}\\Resources\" \"dist\\{toBuild}\\Resources\"",

    f"@rd /S /Q \"Build\\{toBuild}\"",
    f"del \"{toBuild}.spec\"",
]

for command in commands: os.system(command)
