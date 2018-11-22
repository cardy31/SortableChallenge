from fuzzywuzzy import fuzz
from fuzzywuzzy import process

def main():
    string1 = 'led flash macro ring light (48 x led) with 6 adapter rings for for canon/sony/nikon/sigma lenses'
    string2 = 'dp1x'

    print(fuzz.ratio(string1, string2))


if __name__ == '__main__':
    main()
