import math
import re
import argparse


class ConvertUnit(object):

    def __init__(self, numerals=[], **kwargs):

        self.options = {
            'decimal_place': 2,
            'color': False,
            'height': False,
            'hexadecimal': False
        }

        self.units = {
            'acre': ['acres', 'm²', 4046.86],
            'cubic foot': ['cubic feet', 'liters', 28.3168],
            'degree': ['°', '%', 'self.gradient'],
            'fahrenheit': ['F°', 'C°', 'self.temperature'],
            'feet': ['feet', 'm', 0.3048],
            'gallon': ['gallons', 'liters', 0.26417],
            'hp': ['hp', 'kW', 0.7457],
            'inch': ['inches', 'mm', 25.4],
            'km/h': ['km/h', 'm/s', 0.277778],
            'knot': ['knots', 'km/h', 1.852],
            'mile': ['miles', 'km', 1.609344],
            'm/s': ['m/s', 'km/h', 3.6],
            'Newton': ['N', 'kg', 0.10197],
            'ounce': ['oz', 'g', 28.3495],
            'pascal': ['kg/cm²', 'Pa', 98066.5],
            'pint': ['pints', 'liters', 0.47317],
            'point': ['points', 'mm', 0.352778],
            'pound': ['lb', 'kg', 0.453592],
            'ppi': ['ppi', 'pixel/cm', 0.393701],
            'psi': ['PSI', 'kPa', 6.89476],
            'pyeong': ['pyeong', 'm²', 3.305785],
            'quart': ['quarts', 'liters', 0.95],
            'yard': ['yards', 'm', 0.9144]
        }

        self.unit_types = []
        for i in self.units.keys():
            self.unit_types.append(i)
        self.unit_types = sorted(self.unit_types, key=str.lower)

        self.numerals = numerals
        for key in self.options.keys():
            if key in kwargs:
                self.options[key] = kwargs.get(key)

        # determine which to do
        if self.options["color"]:
            ColorModel(self.numerals)
        else:
            if self.options["height"]:
                self.height(self.numerals[0])
            elif self.options["hexadecimal"]:
                self.hexadecimal(self.numerals[0])
            else:
                if len(self.numerals) < 2:
                    print('Specify a unit type:')
                    self.show_unit_list()
                else:
                    self.numeral = float(self.numerals[0].replace(',', ''))
                    self.unit_type = self.numerals[1]
                    if len(self.numerals) == 3:
                        self.until = float(self.numerals[2].replace(',', ''))
                    else:
                        self.until = None
                    self.convert()


    def show_unit_list(self) -> None:

        print(', '.join(self.unit_types))


    def verify_unit(self) -> bool:

        if self.unit_type in self.unit_types:
            return True
        else:
            for i in self.unit_types:
                if self.unit_type in i:
                    self.unit_type = i
                    return True
            print('%s is an unknown unit' % (self.unit_type))
            return False


    def gradient(self, numeral=0) -> tuple[float, float]:

        degree = math.degrees(math.atan(numeral/100))
        percent = math.tan(math.radians(numeral)) * 100
        return degree, percent


    def temperature(self, numeral=0) -> tuple[float, float]:

        fahrenheit = numeral * 9/5 + 32
        celsius = (numeral - 32) * 5/9
        return fahrenheit, celsius


    def hexadecimal(self, numeral) -> None:

        if bool(re.search('[a-fA-F]', numeral)):
            hexadecimal = int(numeral, 16)
            decimal = int(hexadecimal)
            print('0x{:X} = {}'.format(hexadecimal, decimal))
        else:
            decimal = int(numeral)
            print('{} = 0x{:X}'.format(decimal, decimal))
            hexadecimal = int(numeral, 16)
            decimal = int(hexadecimal)
            print('0x{:X} = {}'.format(hexadecimal, decimal))



    def height(self, numeral) -> None:

        if '-' in numeral:
            fi = numeral.split('-')
            feet = int(fi[0])
            inch = float(fi[1])
            cm = feet * 30.48 + inch * 2.54
            inch = self.check_decimal(inch)
            cm = self.check_decimal(cm)
            print('{} feet {} inches = {} cm'.format(feet, inch, cm)) 
        else:
            if float(numeral) < 10.0:
                cm = float(numeral) * 30.48
                cm = self.check_decimal(cm)
                print('{} feet = {} cm'.format(numeral, cm))
            else:
                cm = float(numeral)
                feet = int(cm / 30.48) 
                inch = ((cm % 30.48) / 2.54)
                inch = self.check_decimal(inch)
                print('{} cm = {} feet {} inches'.format(numeral, feet, inch))


    def convert(self) -> None:

        if not self.verify_unit():
            return False
        self.nonmetric_unit = self.units[self.unit_type][0]
        self.metric_unit = self.units[self.unit_type][1]
        self.coefficient = self.units[self.unit_type][2]
        if type(self.coefficient) is float:
            self.coefficient_bool = True
        else:
            self.coefficient_bool = False
        if self.until is not None:
            self.convert_until(self.numeral, self.until)
        else:
            self.calculate(self.numeral)


    def convert_until(self, lower, upper) -> None:

        if lower > upper:
            print('Specify a higher value for the upper limit.')
            return

        longest = 0
        tmp = lower
        # to get the length of the lognest between the results of the first calculation
        while tmp <= upper:
            length = self.calculate(tmp, padding=-1)
            tmp += 1
            if longest < length:
                longest = length
        while lower <= upper:
            length = self.calculate(lower, padding=longest)
            lower += 1


    def check_decimal(self, num) -> str:

        num_str = '{}'.format(num)
        if int(num_str.split('.')[1]) == 0:
            return '{:,}'.format(int(num))
        else:
            return '{:,.{d}f}'.format(num, d=self.options["decimal_place"])


    def calculate(self, numeral, padding=0) -> None:

        if self.coefficient_bool:
            nonmetric_coefficient = 1 / self.coefficient
            nonmetric_value = numeral * nonmetric_coefficient
            metric_value = numeral * self.coefficient
        else:
            func = self.coefficient + '(' + str(numeral) + ')'
            nonmetric_value, metric_value = eval(func)

        numeral = self.check_decimal(numeral)
        metric_value = self.check_decimal(metric_value)
        nonmetric_value = self.check_decimal(nonmetric_value)
        result1 = "{} {} = {} {}".format(numeral, self.nonmetric_unit, metric_value, self.metric_unit)
        result2 = "{} {} = {} {}".format(numeral, self.metric_unit, nonmetric_value, self.nonmetric_unit)
        if padding == -1:
            return len(result1)
        else:
            if padding == 0:
                result = "{: <{p}}{}".format(result1, result2, p=len(result1)+4)
            else:
                result = "{: <{p}}{}".format(result1, result2, p=padding+4)
            print(result)


class ColorModel(object):

    def __init__(self, color=None):

        self.color = color
        for i in self.color:
            self.identify_color_model(i)


    def error_message(self) -> None:

        print('The arguments are formatted wrong.')


    def identify_color_model(self, color: str) -> None:

        color = color.replace(' ', '')
        if color.count(',') >= 3:
            C, M, Y, K = self.parse_CMYK(color)
            if C is False:
                self.error_message()
            else:
                # check if between 0 and 1
                if not all(map(lambda x: x >= 0. and x <= 1., [C, M, Y, K])):
                    self.error_message()
                else:
                    self.CMYK_to_RGB(C, M, Y, K)
        else:
            R, G, B = self.parse_RGB(color)
            if R is False:
                self.error_message()
            else:
                # check if between 0 and 255
                if not all(map(lambda x: x in range(256), [R, G, B])):
                    self.error_message()
                else:
                    self.RGB_to_CMYK(R, G, B)


    def parse_CMYK(self, color: str) -> tuple[float, float, float, float] or tuple[False, False, False, False]:

        color = color.split(',')
        if len(color) == 4:
            try:
                C = float(color[0])
                M = float(color[1])
                Y = float(color[2])
                K = float(color[3])
            except:
                C, M, Y, K = False, False, False, False
        else:
            C, M, Y, K = False, False, False, False

        return C, M, Y, K


    def parse_RGB(self, color: str) -> tuple[int, int, int] or tuple[False, False, False]:

        if color.count(',') == 0:
            if len(color) == 6:
                try:
                    R = int(color[0:2], 16)
                    G = int(color[2:4], 16)
                    B = int(color[4:6], 16)
                except:
                    R, G, B = False, False, False

        if color.count(',') == 2:
            color = color.split(',')
            try:
                R = int(color[0])
                G = int(color[1])
                B = int(color[2])
            except:
                R, G, B = False, False, False

        return R, G, B


    def RGB_hex(self, R, G, B) -> str:

        RGB = [R, G, B]
        for i in range(len(RGB)):
            j = '{:3.0f}'.format(RGB[i])
            j = hex(int(j))
            j = j[2:]
            j = j.upper()
            j = j.zfill(2)
            RGB[i] = j
        RGB = ''.join(RGB)
        return RGB


    def RGB_to_CMYK(self, R, G, B) -> str:

        Rp = R/255
        Gp = G/255
        Bp = B/255
        K = 1 - max(Rp, Gp, Bp)
        C = (1 - Rp - K) / (1 - K)
        M = (1 - Gp - K) / (1 - K)
        Y = (1 - Bp - K) / (1 - K)

        # 255,255,255
        RGBd = '{:3d}, {:3d}, {:3d}'.format(R, G, B)
        # 1.0,1.0,1.0
        RGBp = '{:1.2f}, {:1.2f}, {:1.2f}'.format(Rp, Gp, Bp)
        # FFFFFF
        RGBh = self.RGB_hex(R, G, B)

        result = '{} ({} / {}) = {:1.2f}, {:1.2f}, {:1.2f}, {:1.2f}'.format(RGBd, RGBp, RGBh, C, M, Y, K)
        print(result)


    def CMYK_to_RGB(self, C, M, Y, K) -> str:

        R = 255 * (1 - C) * (1 - K)
        G = 255 * (1 - M) * (1 - K)
        B = 255 * (1 - Y) * (1 - K)
        Rp = R/255
        Gp = G/255
        Bp = B/255

        CMYK = map(lambda x: '{:3.2f}'.format(x), [C, M, Y, K])
        CMYK = ', '.join(CMYK)
        # 1.0,1.0,1.0
        RGBp = '{:1.2f}, {:1.2f}, {:1.2f}'.format(Rp, Gp, Bp)
        # FFFFFF
        RGBh = self.RGB_hex(R, G, B)

        result = '{} = {:3.0f}, {:3.0f}, {:3.0f} ({} / {})'.format(CMYK, R, G, B, RGBp, RGBh)
        print(result)


def parse_args() -> argparse.Namespace:

#     example = '''examples:
# unit.py
#     Supported units are displayed.
# unit.py 10 mi 20
#     10 to 20 miles are converted to kilometers.
# unit.py 99 fah
#     A temperature in Fahrenheit is converted to Celsius.
# unit.py -H 5-11.25
#     A height of 5 feet 11.25 inches is converted to centimeters.
# unit.py -c 0000FF
#     This type of RGB value is converted to CMYK.
# unit.py -c 240,120,99
#     This type of RGB value is converted to CMYK.
# unit.py -c 0,0.1,0.33,0.01
#     This type of CMYK value is converted to RGB.

# To use comma as thousand separator in PowerShell,
# wrap the number with quotes or use the escape character.

# unit.py "100,000" pa
# unit.py 100`,000 pa
# '''

    # parser = argparse.ArgumentParser(
    #     epilog = example,
    #     formatter_class = argparse.RawDescriptionHelpFormatter,
    #     description = 'Convert non-metric units to the metric system.'
    # )

    parser = argparse.ArgumentParser(
        description = "Convert non-metric units to the metric system."
    )
    parser.add_argument(
        'numerals',
        nargs = '*',
        help = 'Enter a numeric value with the full word or the first some letters of a non-metric unit.'
    )
    parser.add_argument(
        '-d',
        dest = 'decimal_place',
        type = int,
        default = 2,
        help = 'Specify the decimal place for the results. (Defualt: 2)'
    )
    parser.add_argument(
        '-c',
        dest = 'color',
        action = 'store_true',
        default = False,
        help = 'With this option, specify one or more RGB or CMYK values to convert between them.'
    )
    parser.add_argument(
        '-H',
        dest = 'height',
        action = 'store_true',
        default = False,
        help = 'With this option, convert heights between feet-inches and centimeters.'
    )
    parser.add_argument(
        '-x',
        dest = 'hexadecimal',
        action = 'store_true',
        default = False,
        help = 'Convert between decimal and hexadecimal.'
    )

    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    ConvertUnit(
        numerals = args.numerals,
        decimal_place = args.decimal_place,
        color = args.color,
        height = args.height,
        hexadecimal = args.hexadecimal)
