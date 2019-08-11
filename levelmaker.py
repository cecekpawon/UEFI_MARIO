#!/usr/bin/python3
import sys, struct, argparse

PY3 = sys.version_info[0] == 3

def to_bytes(n):
    return struct.pack('<I', n)

def converter(level, binary):
    with open(level, "r") as inputFile, open(binary, "wb") as outputFile:
        data = inputFile.read().splitlines()

        if PY3:
            outputFile.write(len(data).to_bytes(4, "little"))
            outputFile.write(len(data[0]).to_bytes(4, "little"))
        else:
            outputFile.write(to_bytes(len(data)))
            outputFile.write(to_bytes(len(data[0])))

        tiles = 0
        coins = 0
        enemies = 0
        for d in data:
            t = d.upper().count("P") + d.upper().count("G") + d.upper().count("C")
            x = d.upper().count("S") + d.upper().count("M")
            coins += d.upper().count("C")
            enemies += (len(d) - d.upper().count(".") - t - x) // 2
            tiles += t

        if PY3:
            outputFile.write(tiles.to_bytes(4, "little"))
            outputFile.write(enemies.to_bytes(4, "little"))
            outputFile.write(coins.to_bytes(4, "little"))
        else:
            outputFile.write(to_bytes(tiles))
            outputFile.write(to_bytes(enemies))
            outputFile.write(to_bytes(coins))

        for d in data:
            if PY3:
                outputFile.write(bytes(d.upper(), "ascii"))
            else:
                outputFile.write(bytes(d.upper()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="Poziom w formacie tekstowym do konwersji - plik wejsciowy")
    parser.add_argument("output", type=str, help="Poziom w wersji binarnej - plik wynikowy")
    args = parser.parse_args()
    converter(args.input, args.output)
