import argparse

parser = argparse.ArgumentParser(
    description = 'Convert a unit to an another.'
)

parser.add_argument(
    'numeral',
    help = 'Enter a numeric value.'
)
parser.add_argument(
    '-t',
    dest = 'temperature',
    action = 'store_true',
    default = False,
    help = 'Celcius / Fahrenheit'
)
parser.add_argument(
    '-m',
    dest = 'mile',
    action = 'store_true',
    default = False,
    help = 'kilometer / mile'
)
parser.add_argument(
    '-y',
    dest = 'yard',
    action = 'store_true',
    default = False,
    help = 'meter / yard'
)
parser.add_argument(
    '-f',
    dest = 'foot',
    action = 'store_true',
    default = False,
    help = 'meter / foot'
)
parser.add_argument(
    '-i',
    dest = 'inch',
    action = 'store_true',
    default = False,
    help = 'millimeter / inch'
)
parser.add_argument(
    '-pt',
    dest = 'point',
    action = 'store_true',
    default = False,
    help = 'millimeter / point'
)
parser.add_argument(
    '-p',
    dest = 'pound',
    action = 'store_true',
    default = False,
    help = 'kilogram / pound'
)
parser.add_argument(
    '-py',
    dest = 'pyeong',
    action = 'store_true',
    default = False,
    help = 'pyeong / square meter'
)

args = parser.parse_args()

def celsius_fahrenheit(temperature): 
    fahrenheit = float(temperature)
    celsius = (fahrenheit - 32) * 5 / 9
    print('\n%3.2f Fahrenheit > %3.2f Celsius' %(fahrenheit, celsius))
    celsius = float(temperature)
    fahrenheit = celsius * 9 / 5 + 32
    print('%3.2f Celsius > %3.2f Fahrenheit\n' %(celsius, fahrenheit))

def kilometer_mile(distance): 
    mile = float(distance)
    kilometer = mile * 1.60934
    print('\n%3.2f miles > %3.2f kilometers' %(mile, kilometer))
    kilometer = float(distance)
    mile = kilometer * 0.621371
    print('%3.2f kilometers > %3.2f miles\n' %(kilometer, mile))

def meter_yard(distance): 
    yard = float(distance)
    meter = yard * 0.9144
    print('\n%3.2f yards > %3.2f meters' %(yard, meter))
    meter = float(distance)
    yard = meter * 1.09361
    print('%3.2f meters > %3.2f yards\n' %(meter, yard))

def meter_foot(distance): 
    foot = float(distance)
    meter = foot * 0.3048
    print('\n%3.2f feet > %3.2f meters' %(foot, meter))
    meter = float(distance)
    foot = meter * 3.28084
    print('%3.2f meters > %3.2f feet\n' %(meter, foot))

def millimeter_inch(distance): 
    inch = float(distance)
    millimeter = inch * 25.4
    centimeter = millimeter / 10
    print('\n%3.2f inches > %3.2f millmeters (%3.2f centimeters)' %(inch, millimeter, centimeter))
    millimeter = float(distance)
    centimeter = millimeter / 10
    inch = millimeter * 0.0393701
    print('%3.2f millimeters (%3.2f centimeters) > %3.2f inches\n' %(millimeter, centimeter, inch))

def millimeter_point(distance): 
    point = float(distance)
    millimeter = point * 0.352778
    print('\n%3.2f points > %3.2f millmeters' %(point, millimeter))
    millimeter = float(distance)
    point = millimeter * 2.83465
    print('%3.2f millimeters > %3.2f points\n' %(millimeter, point))

def kilogram_pound(mass): 
    pound = float(mass)
    kilogram = pound * 2.20462
    print('\n%3.2f pounds > %3.2f kilograms' %(pound, kilogram))
    kilogram = float(mass)
    pound = kilogram * 0.453592
    print('%3.2f kilograms > %3.2f pounds\n' %(kilogram, pound))

def kilogram_pound(area): 
    pyeong = float(area)
    squaremeter = pyeong * 3.30579
    print('\n%3.2f pyeongs > %3.2f square meters' %(pyeong, squaremeter))
    squaremeter = float(area)
    pyeong = squaremeter * 0.3025
    print('%3.2f square meters > %3.2f pyeongs\n' %(squaremeter, pyeong))

if args.temperature: 
    celsius_fahrenheit(args.numeral)
elif args.mile: 
    kilometer_mile(args.numeral)
elif args.yard: 
    meter_yard(args.numeral)
elif args.foot: 
    meter_foot(args.numeral)
elif args.inch: 
    millimeter_inch(args.numeral)
elif args.point: 
    millimeter_point(args.numeral)
elif args.pound: 
    kilogram_pound(args.numeral)
elif args.pyeong: 
    kilogram_pound(args.numeral)