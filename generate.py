#!/usr/bin/python
import os
import sys
import optparse

from generators import MarkovChainGenerator, SensitiveMarkovChainGenerator

if __name__=="__main__":
    parser = optparse.OptionParser()
    parser.add_option('-i', action='store_true', help='import data into a database')
    parser.add_option('-g', action='store_true', help='generate a text sample using a database')

    parser.add_option('-d', metavar="datafile", help='file to contain the database (doesn\'t have to exist if importing)')
    parser.add_option('-f', metavar="source", help='file to import the sample text data from')
    parser.add_option('-l', metavar="length", type=int, default=255, help='length of text to generate (in words, default=255)')

    group = optparse.OptionGroup(parser, 'Advanced options')

    group.add_option('--engine',
                     type='choice',
                     choices=('markov', 'markov-sensitive'),
                     default='markov',
                     help="engine to use for importing data and generating text currently supported: markov (default), markov-sensitive")

    group.add_option('--dump',
                     metavar="datafile",
                     help='dump contents of the database supplied as an argument (all other arguments and options are ignored')
    parser.add_option_group(group)

    (options, args) = parser.parse_args()

    if options.engine == 'markov':
        engine = MarkovChainGenerator
    elif options.engine == 'markov-sensitive':
        engine = SensitiveMarkovChainGenerator
    else:
        engine = MarkovChainGenerator

    if options.dump:
        if not os.path.exists(options.dump):
            parser.error('supply an existing database file name to dump')
        generator = engine(options.dump)
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
        generator = engine(options.d)
        print generator.generateText(options.l)

    if options.i:
        if not options.f or not os.path.exists(options.f):
            parser.error('You need to specify existing file to import data from')
        generator = engine(options.d)
        generator.importFile(options.f)
