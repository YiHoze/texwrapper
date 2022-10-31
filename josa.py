import os
import sys
import argparse

dirCalled = os.path.dirname(__file__)
sys.path.append(os.path.abspath(dirCalled))
import hanja2hangul

def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description = 'Determine josa (postposition) to match the last sound of the preceding word.'
    )
    parser.add_argument(
        'words',
        nargs = '+',
        help = 'Enter a word or more. For example, "사람\가".'
    )
    parser.add_argument(
        '-a',
        dest = 'allophone',
        action = 'store_true',
        default = False,
        help = 'Enumerate allophones of a Chinese character.'
    )
    parser.add_argument(
        '-s',
        dest = 'sound',
        action = 'store_true',
        default = False,
        help = 'Get sounds of Hanja characters.'
    )
    parser.add_argument(
        '-p',
        dest = 'homophone',
        action = 'store_true',
        default = False,
        help = 'Enumerate Hanja characters having given sounds.'

    )
    return parser.parse_args()


class JosaChecker(object):

    def __init__(self, allophone=False):

        self.allophone = allophone

        # 종성 28 자
        # self.Ts = ['', 'ㄱ','ㄲ','ㄳ','ㄴ','ㄵ','ㄶ','ㄷ','ㄹ','ㄺ','ㄻ','ㄼ','ㄽ','ㄾ','ㄿ','ㅀ','ㅁ','ㅂ','ㅄ','ㅅ','ㅆ','ㅇ','ㅈ','ㅊ','ㅋ','ㅌ','ㅍ','ㅎ']

        self.josas = {
            '이':['가', '이'],
            '가':['가', '이'],
            '을':['를', '을'],
            '를':['를', '을'],
            '은':['는', '은'],
            '는':['는', '은'],
            '와':['와', '과'],
            '과':['와', '과'],
            '로':['로', '으로'],
            '으로':['로', '으로'],
            '라':['라', '이라'],
            '이라':['라', '이라']
        }
        self.numerals = {
            '1':'일',
            '2':'이',
            '3':'삼',
            '4':'사',
            '5':'오',
            '6':'육',
            '7':'칠',
            '8':'팔',
            '9':'구',
            '0':'영'
        }


    def parse_word(self, word:str, apart=False) -> str:

        chars = word.split('\\')
        if len(chars) == 1:
            substantive = chars[0]
            josa = substantive[-1]
            substantive = substantive[0:-1]
        else:
            substantive = chars[0]
            josa = chars[1]
        last_char = substantive[-1]

        if josa in self.josas.keys():
            char_range = self.determine_char_range(last_char)
            if char_range == 'numeric':
                Josa = self.determine_josa(self.numerals[last_char], josa)
            elif char_range == 'roman':
                Josa = self.determine_josa(self.determine_roman_sound(last_char), josa)
            elif char_range == 'hangul':
                Josa = self.determine_josa(last_char, josa)
            elif char_range == 'hanja':
                Josa = self.determine_hanja_josa(last_char, josa)
            else:
                Josa = ''
        else:
            Josa = ''

        if apart:
            return substantive, Josa
        else:
            return substantive+Josa

        # if Josa == '':
        #     result = word
        # else:
        #     if isinstance(Josa, list):
        #         result = []
        #         for J in Josa:
        #             result.append(substantive + J)
        #         result = ' '.join(result)
        #     else:
        #         result = substantive + Josa


    def determine_char_range(self, character:str) -> str:

        if character >= '0' and character <= '9':
            return 'numeric'
        elif (character >= 'a' and character <= 'z') or (character >= 'A' and character <= 'Z'):
            return 'roman'
        elif character >= '가' and character <= '힣':
            return 'hangul'
        elif character >= '㐀' and character <= '﨩':
            return 'hanja'
        else:
            None


    def determine_josa(self, last_char:str, josa:str) -> str:

            T = self.determine_jongseong(last_char)
            if josa == '로' or josa == '으로':
                if T == 0 or T == 8: 
                    josa_index = 0 
                else: 
                    josa_index = 1
            else:
                if T == 0: 
                    josa_index = 0
                else: 
                    josa_index = 1
            return self.josas[josa][josa_index]


    def determine_jongseong(self, character: str) -> int:

        code_point =  ord(character) - 0xAC00
        L = int(code_point / (21*28))
        V = int(code_point % (21*28) / 28) 
        T = code_point % 28
        return T


    def determine_roman_sound(self, letter:str) -> str:

        letter = letter.lower()
        if letter == 'l':
            return '갈'
        elif letter == 'm' or letter == 'n':
            return '감'
        else:
            return '가'


    def determine_hanja_josa(self, hanja:str, josa) -> str:

        hanja_code = int(ord(hanja))
        hangul_code = hanja2hangul.sound[hanja_code]

        if isinstance(hangul_code, list):
            if self.allophone:
                Josa = []
                for  c in hangul_code:
                    Josa.append('({}){}'.format(chr(c), self.determine_josa(chr(c), josa)))
            else:
                Josa = self.determine_josa(chr(hangul_code[0]), josa)
        else:
            Josa = self.determine_josa(chr(hangul_code), josa)
        return Josa


    def get_hanja_sound(self, hanjas:str) -> None:

        hanguls = ''
        for hanja in hanjas:
            hanja_code = int(ord(hanja))
            if hanja2hangul.sound.get(hanja_code):
                hangul_code = hanja2hangul.sound[hanja_code]
                if isinstance(hangul_code, list):
                    hanguls += chr(hangul_code[0])
                else:
                    hanguls += chr(hangul_code)
            else:
                hanguls += hanja
        print(hanguls)


    def get_hanja_homophones(self, hanguls:str) -> None:

        for hangul in hanguls:
            hangul_code = int(ord(hangul))
            hanja_codes = [k for k, v in hanja2hangul.sound.items() if v == hangul_code]
            hanjas = [chr(c) for c in hanja_codes]
            print("{}: {}".format(hangul, ''.join(hanjas)))


if __name__ == '__main__':
    args = parse_args()
    jc = JosaChecker(args.allophone)
    for word in args.words:
        if args.sound:
            jc.get_hanja_sound(word)
        elif args.homophone:
            jc.get_hanja_homophones(word)
        else:
            result = jc.parse_word(word)
            print(result)
