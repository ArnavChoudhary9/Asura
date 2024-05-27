import os, sys
import pathlib

toBuild = sys.argv[1]
config = "d" if len(sys.argv) == 2 else sys.argv[2]

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
    "--noconsole --onefile" if config == "r" else ""
])

commands = [
    f"PyInstaller --path \"{currdir}\" {collects} {hiddenImports} {additionals} \"{toBuild}\\{toBuild}\".py",

    f"mkdir \"dist\\{toBuild}\"" if config == "r" else "",

    f"xcopy /s \"Build\\Essentials\" \"dist\\{toBuild}\"",
    f"copy \".\\imgui.ini\" \"dist\\{toBuild}\\\"",

    f"mkdir \"dist\\{toBuild}\\Asura\\InternalAssets\"",
    f"xcopy /s /i \"Asura\\InternalAssets\" \"dist\\{toBuild}\\Asura\\InternalAssets\"",

    f"mkdir \"dist\\{toBuild}\\{toBuild}\\Resources\"",
    f"xcopy /s /i \"{toBuild}\\Resources\" \"dist\\{toBuild}\\{toBuild}\\Resources\"",

    f"copy \"dist\\{toBuild}.exe\" \"dist\\{toBuild}\"" if config == "r" else "",
    f"del \"dist\\{toBuild}.exe\"" if config == "r" else "",

    f"@rd /S /Q \"Build\\{toBuild}\"",
    f"del \"{toBuild}.spec\"",
]

for command in commands: os.system(command)
