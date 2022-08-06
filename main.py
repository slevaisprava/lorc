from lorc.orchestra import orchestra


if __name__ == "__main__":
    with open("lorc/csound/sample.csp", "r") as f:
        source = f.read()
        orc: list[str] = orchestra.Orchestra.parse_instruments(source, 1)
    with open("lorc/csound/sample.orc", "w") as f:
        f.writelines(orc)
