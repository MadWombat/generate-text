#!/usr/bin/python
import os
import sys
import optparse

from generators import MarkovChainGenerator

if __name__=="__main__":
    parser = optparse.OptionParser()
    parser.add_option('-i', action='store_true', help='import data into a database')
    parser.add_option('-g', action='store_true', help='generate a text sample using a database')
    parser.add_option('-d', help='file to contain the database (doesn\'t have to exist if importing)')
    parser.add_option('-f', help='file to import the sample text data from')
    parser.add_option('-l', type=int, default=255, help='length of text to generate (in words, default=255)')
    parser.add_option('--dump', help='dump contents of the database supplied as an argument (all other arguments and options are ignored')

    (options, args) = parser.parse_args()

    if options.dump:
        if not os.path.exists(options.dump):
            parser.error('supply an existing database file name to dump')
        generator = MarkovChainGenerator(options.dump)
        generator.dumpState()
        sys.exit(0)

    # check that we have all required info
    if options.i and options.g:
        parser.error('You should use either -i or -g, but not both')

    if not options.d:
        parser.error('You need to specify database file name')

    if options.g:
        if not os.path.exists(options.d):
            parser.error('You need to specify existing database file to generate text from')
        generator = MarkovChainGenerator(options.d)
        print generator.generateText(options.l)

    if options.i:
        if not options.f or not os.path.exists(options.f):
            parser.error('You need to specify existing file to import data from')
        generator = MarkovChainGenerator(options.d)
        generator.importFile(options.f)
