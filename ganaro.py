import argparse
from inspect import trace
import re
from telnetlib import GA


class GanaToRoman(object):


    def __init__(self, **kwargs):

        self.options = {
            'capital': False,
            'hiragana': False,
            'katagana': False
        }

        self.reconfigure(kwargs)

        self.gana_roman = {
            'あ':'a',  'い':'i',  'う':'u',  'え':'e',  'お':'o', 
            'か':'ka', 'き':'ki', 'く':'ku', 'け':'ke', 'こ':'ko', 
            'が':'ga', 'ぎ':'gi', 'ぐ':'gu', 'げ':'ge', 'ご':'go', 
            'さ':'sa', 'し':'shi', 'す':'su', 'せ':'se', 'そ':'so', 
            'ざ':'za', 'じ':'ji', 'ず':'zu', 'ぜ':'ze', 'ぞ':'zo', 
            'た':'ta', 'ち':'chi', 'つ':'tsu', 'て':'te', 'と':'to', 
            'だ':'da', 'ぢ':'ji', 'づ':'zu', 'で':'de', 'ど':'do', 
            'な':'na', 'に':'ni', 'ぬ':'nu', 'ね':'ne', 'の':'no', 
            'は':'ha', 'ひ':'hi', 'ふ':'fu', 'へ':'he', 'ほ':'ho', 
            'ば':'ba', 'び':'bi', 'ぶ':'bu', 'べ':'be', 'ぼ':'bo', 
            'ぱ':'pa', 'ぴ':'pi', 'ぷ':'pu', 'ぺ':'pe', 'ぽ':'po', 
            'ま':'ma', 'み':'mi', 'む':'mu', 'め':'me', 'も':'mo', 
            'ら':'ra', 'り':'ri', 'る':'ru', 'れ':'re', 'ろ':'ro',
            'わ':'wa', 'を':'wo', 
            'ん':'NN', 
            'や':'!ya', 'ゆ':'!yu', 'よ':'!yo',
            'ゃ':'!ya', 'ゅ':'!yu', 'ょ':'!yo',
            'っ':'KK', 
            'ア':'a', 'イ':'i', 'ウ':'u', 'エ':'e', 'オ':'o', 
            'ィ':'I',
            'カ':'ka', 'キ':'ki', 'ク':'ku', 'ケ':'ke', 'コ':'ko',
            'ガ':'ga', 'ギ':'gi', 'グ':'gu', 'ゲ':'ge', 'ゴ':'go',
            'サ':'sa', 'シ':'shi', 'ス':'su', 'セ':'se', 'ソ':'so',
            'ザ':'za', 'ジ':'ji', 'ズ':'zu', 'ゼ':'ze', 'ゾ':'zo',
            'タ':'ta', 'チ':'chi', 'ツ':'tsu', 'テ':'te', 'ト':'to',
            'ダ':'da', 'ヂ':'ji', 'ヅ':'zu', 'デ':'de', 'ド':'do',
            'ナ':'na', 'ニ':'ni', 'ヌ':'nu', 'ネ':'ne', 'ノ':'no',
            'ハ':'ha', 'ヒ':'hi', 'フ':'fu', 'ヘ':'he', 'ホ':'ho',
            'バ':'ba', 'ビ':'bi', 'ブ':'bu', 'ベ':'be', 'ボ':'bo',
            'パ':'pa', 'ピ':'pi', 'プ':'pu', 'ペ':'pe', 'ポ':'po',
            'マ':'ma', 'ミ':'mi', 'ム':'mu', 'メ':'me', 'モ':'mo',
            'ラ':'ra', 'リ':'ri', 'ル':'ru', 'レ':'re', 'ロ':'ro',
            'ワ':'wa', 'ヲ':'wo',
            'ン':'NN', 
            'ヤ':'!ya', 'ユ':'!yu', 'ヨ':'!yo',
            'ャ':'!ya', 'ュ':'!yu', 'ョ':'!yo',
            'ッ':'KK'} 

        self.hiragana = {
            'a':'あ',  'i':'い',  'u':'う',  'e':'え',  'o':'お', 
            'ka':'か', 'ki':'き', 'ku':'く', 'ke':'け', 'ko':'こ', 
            'ga':'が', 'gi':'ぎ', 'gu':'ぐ', 'ge':'げ', 'go':'ご', 
            'sa':'さ', 'shi':'し', 'su':'す', 'se':'せ', 'so':'そ', 
            'za':'ざ', 'ji':'じ', 'zu':'ず', 'ze':'ぜ', 'zo':'ぞ', 
            'ta':'た', 'chi':'ち', 'tsu':'つ', 'te':'て', 'to':'と', 
            'da':'だ', 'Ji':'ぢ', 'zu':'づ', 'de':'で', 'do':'ど', 
            'na':'な', 'ni':'に', 'nu':'ぬ', 'ne':'ね', 'no':'の', 
            'ha':'は', 'hi':'ひ', 'fu':'ふ', 'he':'へ', 'ho':'ほ', 
            'ba':'ば', 'bi':'び', 'bu':'ぶ', 'be':'べ', 'bo':'ぼ', 
            'pa':'ぱ', 'pi':'ぴ', 'pu':'ぷ', 'pe':'ぺ', 'po':'ぽ', 
            'ma':'ま', 'mi':'み', 'mu':'む', 'me':'め', 'mo':'も', 
            'ra':'ら', 'ri':'り', 'ru':'る', 're':'れ', 'ro':'ろ',
            'wa':'わ', 'wo':'を', 
            'n':'ん',
            'ya':'や', 'yu':'ゆ', 'yo':'よ',
            'k':'っ'}

        self.katagana = {
            'a':'ア', 'i':'イ', 'u':'ウ', 'e':'エ', 'o':'オ', 
            'ka':'カ', 'ki':'キ', 'ku':'ク', 'ke':'ケ', 'ko':'コ',
            'ga':'ガ', 'gi':'ギ', 'gu':'グ', 'ge':'ゲ', 'go':'ゴ',
            'sa':'サ', 'shi':'シ', 'su':'ス', 'se':'セ', 'so':'ソ',
            'za':'ザ', 'ji':'ジ', 'zu':'ズ', 'ze':'ゼ', 'zo':'ゾ',
            'ta':'タ', 'chi':'チ', 'tsu':'ツ', 'te':'テ', 'to':'ト',
            'da':'ダ', 'Ji':'ヂ', 'zu':'ヅ', 'de':'デ', 'do':'ド',
            'na':'ナ', 'ni':'ニ', 'nu':'ヌ', 'ne':'ネ', 'no':'ノ',
            'ha':'ハ', 'hi':'ヒ', 'fu':'フ', 'he':'ヘ', 'ho':'ホ',
            'ba':'バ', 'bi':'ビ', 'bu':'ブ', 'be':'ベ', 'bo':'ボ',
            'pa':'パ', 'pi':'ピ', 'pu':'プ', 'pe':'ペ', 'po':'ポ',
            'ma':'マ', 'mi':'ミ', 'mu':'ム', 'me':'メ', 'mo':'モ',
            'ra':'ラ', 'ri':'リ', 'ru':'ル', 're':'レ', 'ro':'ロ',
            'wa':'ワ', 'wo':'ヲ',
            'n':'ン', 
            'ya':'ヤ', 'yu':'ユ', 'yo':'ヨ',
            'k':'ッ'}

        self.gana = self.gana_roman.keys()
        self.roman = self.hiragana.keys()

    def reconfigure(self, options) -> None:

        for key in self.options.keys():
            if key in options:
                self.options[key] = options.get(key)


    def get_hiragana(self, sounds) -> str:

        sounds = sounds.split(' ')
        word = ''
        for sound in sounds:
            if sound in self.roman:
                word += self.hiragana[sound]
            else:
                word += sound
        return word


    def get_katagana(self, sounds) -> str:

        sounds = sounds.split(' ')
        word = ''
        for sound in sounds:
            if sound in self.roman:
                word += self.katagana[sound]
            else:
                word += sound
        return word


    def transliterate(self, word, **options) -> str:

        self.reconfigure(options)

        transliterated = ''
        for c in word:
            if c in self.gana:
                transliterated += self.gana_roman[c]
            else:
                transliterated += c

        # return transliterated
        # self.transcribed= re.sub('(?<!n)g(?=/[gkndlmbsjcktph]|$)', 'k', self.transcribed)

        # 拗音 ようおん yōoñ
        transliterated = re.sub('[aiueo]I', 'i', transliterated)
        transliterated = re.sub('[i]*!y', 'y', transliterated)
        # 長音 ちょうおん chyōoñ
        transliterated = re.sub('ei', 'ē', transliterated)
        transliterated = re.sub('ou', 'ō', transliterated)
        transliterated = re.sub('aa', 'ā', transliterated)
        transliterated = re.sub('ii', 'ī', transliterated)
        transliterated = re.sub('uu', 'ū', transliterated)
        transliterated = re.sub('ee', 'ē', transliterated)
        transliterated = re.sub('oo', 'ō', transliterated)
        # 促音 そくおん sokuoñ
        transliterated = re.sub('KK([kstp])', '\\1\\1', transliterated)
        transliterated = re.sub('KK', 'tsu', transliterated)
        # 発音 はつおん hatsuoñ
        transliterated = re.sub('NN$', 'ñ', transliterated)
        transliterated = re.sub('NN([aiueohwy])', 'ñ\\1', transliterated)
        transliterated = re.sub('NN([kg])', 'ng\\1', transliterated)
        transliterated = re.sub('NN([bpm])', 'm\\1', transliterated)
        transliterated = re.sub('NN', 'n', transliterated)

        if self.options['capital']:
            transliterated = transliterated.upper()

        return transliterated


    def determine_task(self, words) -> None:

        output = []
        if self.options['hiragana']:
            for word in words:
                output.append(self.get_hiragana(word))
        elif self.options['katagana']:
            for word in words:
                output.append(self.get_katagana(word))
        else:
            for word in words:
                output.append(self.transliterate(word))
        print(''.join(output))


def parse_args() -> argparse.Namespace:

    parser = argparse.ArgumentParser(
        description = 'Romanize Hiragana and Katakana words, or vice versa.'
    )

    parser.add_argument(
        'words',
        nargs = '+',
        help = 'Enter one or more Japanese or English words.'
    )
    parser.add_argument(
        '-c',
        dest = 'capital',
        action = 'store_true',
        default = False,
        help = 'Capitalize the output when transliterating into Roman.'
    )
    parser.add_argument(
        '-g',
        dest = 'hiragana',
        action = 'store_true',
        default = False,
        help = 'Show Hiragana characters for given sounds.'
    )
    parser.add_argument(
        '-k',
        dest = 'katagana',
        action = 'store_true',
        default = False,
        help = 'Show Katagana characters for given sounds.'
    )


    return parser.parse_args()


if __name__ == '__main__':

    args = parse_args()
    GTR = GanaToRoman(capital=args.capital, hiragana=args.hiragana, katagana=args.katagana)
    GTR.determine_task(args.words)
