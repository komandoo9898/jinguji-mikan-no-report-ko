"""PPF 3.0 패치 적용기(PPF-O-Matic 대신 쓸 수 있는 파이썬 판).

사용: python apply_ppf.py <원본.bin> <패치.ppf> <출력.bin>
원본은 건드리지 않고 복사본에 적용한다.
"""
from __future__ import annotations

import shutil
import sys


def main():
    src, ppf, out = sys.argv[1:4]
    data = open(ppf, 'rb').read()
    if data[:5] != b'PPF30':
        raise SystemExit('PPF 3.0 파일이 아닙니다')
    blockcheck, undo = data[57], data[58]
    pos = 60 + (1024 if blockcheck else 0)
    end = len(data)
    if data[-4:] == b'.DIZ':  # 파일 설명 블록이 있으면 제외
        end -= 4 + int.from_bytes(data[-6:-4], 'little') + 18 + 2
    shutil.copyfile(src, out)
    count = 0
    with open(out, 'r+b') as f:
        while pos < end:
            off = int.from_bytes(data[pos:pos + 8], 'little')
            n = data[pos + 8]
            f.seek(off)
            f.write(data[pos + 9:pos + 9 + n])
            pos += 9 + n + (n if undo else 0)
            count += 1
    print(f'적용 완료: {count}개 기록 -> {out}')


if __name__ == '__main__':
    main()
