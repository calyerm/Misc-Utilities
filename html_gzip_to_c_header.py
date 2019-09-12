# webserver utility for embedded development
#
# Date: 06/24/2017
# Author: mcalyer
# Python 3.7

# Description:
#    Converts html index page to gzip format
#    Then creates a c header file with this structure:
#    #define file_name_html_gz_len NNNN
#    const uint8_t index_html_gz[] = { 0x1F, 0x8B, 0x08, 0x08, 0x50, .... };
#
#

import gzip
import shutil
import os
import sys
import argparse


def c_header_file(fn):

    input_file_name  = fn + '.html'
    gz_file_name     = fn + '.html.gz'
    header_file      = fn
    header_file_name = fn + '.h'

    print("Generating C header file containing html gzip byte array")
    print("Default input file name is index.html or input file name")
    print("Date: 06/25/2019 , Version 1.00 \n")

    print("Input file  : "  + input_file_name)
    print("gzip  file  : "  + gz_file_name)
    print("header file : "  + header_file_name)
    print("\n")

    # Convert html file to a gzip file
    try:
        with open(input_file_name, 'rb') as f_in:
            with gzip.open(gz_file_name, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except IOError:
        print("Error , Can not open file  : " +  input_file_name + "\n")
        exit(0)


    # Open gzip file and extract gzip data and then
    # create desired c header file with the desired format

    f_in  = open(gz_file_name, 'rb')
    f_in.seek(0, os.SEEK_END)
    f_in_size = f_in.tell()
    f_in_last = f_in_size - 1
    f_in.seek(0)
    print('File in size: ' , f_in_size )

    f_out = open(header_file_name, 'w')
    f_out.write("#define " + header_file + "_len  " + str(f_in_size)+ '\n')
    f_out.write("const uint8_t  "  + header_file + "_html_gz[] = {\n")

    # Extract gzip data and convert to string hex and write into file
    f_in_buf = f_in.read()
    f_in.close()

    #d = hex(f_in_buf[0])
    #print(d)

    line_string = ''
    item_count = 0
    for i,d in enumerate(f_in_buf):
        fd = f"{d:#0{4}x}"
        line_string += '   ' + fd
        if i != f_in_last:
            line_string += ','
        if (item_count == 0) or (item_count % 15) :
            item_count += 1
            continue
        line_string += '\n'
        f_out.write(line_string)
        line_string = ''
        item_count = 0
    if item_count:
        line_string += '\n'
        f_out.write(line_string)

    # file out last line
    f_out.write("};")

    # Close output file
    f_out.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file",
                        type=str,
                        nargs='?',
                        default="index",
                        help="html file to convert to c header ,  no suffix , default = index")

    args = parser.parse_args()
    c_header_file(args.input_file)


if __name__=="__main__":
    main()
    exit(0)