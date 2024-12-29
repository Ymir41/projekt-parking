import sys
import re

# Funkcja przekształca prostokąt z formatu [x1, y1, x2, y2] na [x1, y1, x3, y3, x2, y2, x4, y4]
def convert_rectangle_format(line):
    def replace_match(match):
        x1, y1, x2, y2 = map(int, match.groups())
        x3, y3 = x2, y1  # Prawy górny róg
        x4, y4 = x1, y2  # Lewy dolny róg
        return f'[{x1}, {y1}, {x3}, {y3}, {x2}, {y2}, {x4}, {y4}]'

    # Zamień wszystkie wystąpienia patternu w linii
    new_line = re.sub(r'\[(\d+),\s*(\d+),\s*(\d+),\s*(\d+)\]', replace_match, line)
    print(f"DEBUG: Original line: '{line}' => Converted line: '{new_line}'")  # Debugowanie
    return new_line

def process_file(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            converted_line = convert_rectangle_format(line)
            outfile.write(converted_line)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Użycie: python script.py input.txt output.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    process_file(input_file, output_file)

