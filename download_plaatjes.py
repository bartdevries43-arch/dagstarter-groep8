#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Downloadt gevarieerde line-art tekeningen (OpenMoji, CC BY-SA 4.0) om in te
kleuren, en schrijft ze weg als kleurplaten_data.py voor de generator.
Bron: https://openmoji.org  (zwart-wit 'black' variant)
"""
import json
import urllib.request
import concurrent.futures

BASIS = "https://raw.githubusercontent.com/hfg-gmuend/openmoji/master/black/svg/"

# Gevarieerde, kindvriendelijke selectie (Unicode-codepoints, hoofdletters).
CODES = """
1F408 1F415 1F429 1F416 1F417 1F411 1F410 1F404 1F402 1F403 1F40F 1F40E 1F98C
1F418 1F98F 1F99B 1F42A 1F42B 1F992 1F98D 1F9A7 1F412 1F98E 1F981 1F405 1F406
1F993 1F401 1F400 1F430 1F407 1F43F 1F994 1F987 1F428 1F43C 1F9A5 1F9A6 1F9A8
1F9A1 1F984 1F409 1F996 1F995 1F438 1F40A 1F422 1F40D 1F98E 1F413 1F423 1F424
1F425 1F426 1F427 1F54A 1F985 1F986 1F9A2 1F989 1F99A 1F99C 1F983 1F9A9 1F41F
1F420 1F421 1F988 1F419 1F41A 1F980 1F99E 1F990 1F991 1F42C 1F433 1F40B 1F9AD
1F41C 1F41D 1F41E 1F98B 1F40C 1F997 1F577 1F982 1FAB2 1F99F 1F41B 1F34E 1F34F
1F34C 1F347 1F349 1F353 1F352 1F351 1F350 1F34A 1F34B 1F345 1F955 1F33D 1F344
1F35E 1F9C0 1F373 1F366 1F367 1F368 1F369 1F36A 1F382 1F370 1F36B 1F36C 1F36D
1F9C1 1F355 1F354 1F35F 1F32D 1F37F 1F36F 1F95A 1F373 1F95E 1F32E 1F32F 1F963
1F333 1F332 1F334 1F335 1F340 1F33B 1F337 1F339 1F33C 1F341 1F342 1F33F 1F33E
2600 1F319 2B50 1F31F 2601 1F308 2744 26C4 1F30D 1FA90 2604 1F320 1F327 26A1
1F697 1F695 1F699 1F68C 1F692 1F693 1F691 1F69A 1F69C 1F6B2 1F6F4 1F3CD 1F682
1F683 1F684 2708 1F681 1F680 1F6F8 26F5 1F6A2 1F6F6 2693 1F69C 1F6FA 1F3CE
1F3A8 270F 1F4DA 1F3B8 1F3B7 1F3BA 1F941 1F3B2 1F9E9 1F3AE 1F3AF 1F3B3 26BD
1F3C0 1F3C8 26BE 1F3BE 1F3D0 1F3D3 1F94A 1F6F9 1FA81 1F3AA 1F3A1 1F3A2 1F388
1F381 1F3E0 1F3F0 1F5FC 26F2 1F5FA 231B 23F0 1F4A1 1F526 1F52D 1F52C 1F3A9
1F451 1F452 1F45F 1F457 1F45C 1F392 2602 1F3C6 1F514 1F916 1F47B 1F47D 2764
1F3B5 1F48E 1F511 1F4E7 1F4F7 1F3B9 1F6CE 1FA82 1F9F8 1F3B0 1F0CF 1F3B1 1F945
26F3 1F3D2 1F94F 1F6F7 1FA83 1FA90 1F9ED 1F9EF 1F9F1 1FA94 1F52E 1F9F2
""".split()


def fetch(code):
    url = BASIS + code + ".svg"
    try:
        with urllib.request.urlopen(url, timeout=20) as r:
            data = r.read().decode("utf-8")
        if "<svg" in data and len(data) > 200:
            return code, data
    except Exception:
        pass
    return code, None


def main():
    uniek = list(dict.fromkeys(CODES))          # dedup, volgorde behouden
    print(f"{len(uniek)} unieke codepoints, downloaden...")
    resultaat = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as ex:
        for code, svg in ex.map(fetch, uniek):
            if svg:
                resultaat[code] = svg
    print(f"{len(resultaat)} tekeningen gelukt.")

    with open("kleurplaten_data.py", "w", encoding="utf-8") as f:
        f.write("# -*- coding: utf-8 -*-\n")
        f.write('"""Line-art tekeningen (OpenMoji, CC BY-SA 4.0) om in te '
                'kleuren. Automatisch gegenereerd door download_plaatjes.py."""\n\n')
        f.write("PLAATJES = ")
        f.write(json.dumps(list(resultaat.values()), ensure_ascii=False))
        f.write("\n")
    print("kleurplaten_data.py geschreven.")


if __name__ == "__main__":
    main()
