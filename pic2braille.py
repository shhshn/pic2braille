
import argparse, collections, cv2 as cv

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", "-file", required=True)
    parser.add_argument("--size", "-size", type=int, default=160)
    args = parser.parse_args()
    gray, color = cv.imread(args.file, 0), cv.imread(args.file, 1)
    if gray is None:
        return
    height, width = len(gray), len(gray[0])
    if width > args.size:
        scale = width // args.size + min(1, (width % args.size))
        height = height // scale; width = width // scale
        gray = cv.resize(gray, (width, height))
        color = cv.resize(color, (width, height))
    height, width = len(gray) // 4, len(gray[0]) // 2
    for y in range(height):
        for x in range(width):
            vote = []; value = 0
            for dy in range(4):
                for dx in range(2):
                    b, g, r = color[y * 4 + dy][x * 2 + dx]
                    vote.append((r, g, b))
                    if gray[y * 4 + dy][x * 2 + dx] < 128: continue
                    if (dx, dy) == (0, 0): value += 0x1
                    if (dx, dy) == (0, 1): value += 0x2
                    if (dx, dy) == (0, 2): value += 0x4
                    if (dx, dy) == (1, 0): value += 0x8
                    if (dx, dy) == (1, 1): value += 0x10
                    if (dx, dy) == (1, 2): value += 0x20
                    if (dx, dy) == (0, 3): value += 0x40
                    if (dx, dy) == (1, 3): value += 0x80
            best = collections.Counter(vote).most_common(2)
            text, background = (best[1][0], best[0][0]) if len(best) == 2 else (best[0][0], best[0][0])
            print("\033[38;2;%d;%d;%dm" % text, end="")
            print("\033[48;2;%d;%d;%dm" % background, end="")
            print(chr(0x2800 + value), end="")
        print("\033[0m")
    print("\033[0m", end="")

if __name__ == "__main__":
    main()
