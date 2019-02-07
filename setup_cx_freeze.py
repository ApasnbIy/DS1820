from cx_Freeze import setup, Executable

exe = Executable(
    script="_main_.pyw",
    base="Win32GUI",
    )

setup(
    name = "DS18*20",
    version = "0.1",
    description = "DS18*20",
    executables = [exe]
)