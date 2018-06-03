# vim: set fileencoding=utf-8
import sys # we only use sys.stdin in this script
import argparse # we use only ArgumentParser class from this module


# Define some global constants
DEFAULT_MARK        = '@'
DEFAULT_WINDOW_SIZE = 30
SKIP_DEFAULT        = 0
BAN_DEFAULT         = ['I', 'the', 'a', 'an', 'to', 'be', 'of', 'and', 'in', 'that', 'this', 'as']
# End of global constants definitions


def prune(word):
    """ Removes all non-letter symbols from the start and the end of a `word` and lowercase it."""
    punctiation_signs = '!?.,#''"`%()_*@\n'
    pruned = ''
    for char in word:
        if not char in punctiation_signs:
            pruned = pruned + char
    return pruned.lower()


def tautology(w, v, second_pruned=False):
    """ Checks whether a word `w` is a tautology of a word `v`. A tautology is either literally the same word or a word with the same
    stem. For example, 'move' is a tautology of a word 'moving' and so on. If `second_pruned`, then we run method `prune` only on the
    first argument."""
    if second_pruned:
        return prune(w) == v
    else:
        return prune(w) == prune(v)


def empty(list):
    """ Checks whether the `list` is empty. Returns `true` or `false` accordingly."""
    return len(list) == 0


def marked(word, mark):
    """ Return `true` iff `word` has a `mark` in front of it."""
    return word[0] == mark


def mark(words, index, stain):
    """ Prefixes the word in `words` at `index` with `stain` only once."""
    if not marked(words[index], stain):
        words[index] = stain + words[index]


def detect_tautologies(words, stain=DEFAULT_MARK, window=DEFAULT_WINDOW_SIZE, skip=SKIP_DEFAULT, ban_list=BAN_DEFAULT):
    """ Marks all tautologies in `words` with `stain`. The option `window` specifies the size of a 'tautology window', e.g. how many
        words backwards are examined when searching for similar words."""
    if len(words) == 1:
        return
    #
    for i in range(1, len(words)):
        # We don't process words that are in stop list
        pruned_next_word = prune(words[i])
        if pruned_next_word in ban_list:
            continue
        # Gather all indices of words that are considered to be tautologies of the current `pruned_next_word`
        window_start = max(i - window, 0)
        window_end   = max(0, i - skip)
        tautology_indices = [j for j in range(window_start, window_end) if tautology(words[j], pruned_next_word, second_pruned=True)]
        if not empty(tautology_indices):
            mark(words, i, stain)
            for index in tautology_indices:
                mark(words, index, stain)


def echo(words):
    """ Prints `words` to the standart output accounting for line breaks. """
    next_line = ''
    for word in words:
        next_line = next_line + word
        last_char = word[-1:]
        if last_char == '\n':
            print(next_line, end='')
            next_line = ''
        else:
            next_line = next_line + ' '


def clean_marks(words, mark=DEFAULT_MARK):
    """ Removes all `mark`s from `words`. """
    for i in range(0, len(words)):
        first_letter = words[i][:1]
        if first_letter == mark:
            words[i] = words[i][1:]


# python3 script.py -m # -w 10 -u --skip (-s) 3 --banlist (-b) this is text
parser = argparse.ArgumentParser(description='Mark tautologies in a text')
parser.add_argument('-m', '--mark', default=DEFAULT_MARK, help='The mark that will be used as a prefix in tautologies.', metavar='mark')
parser.add_argument('-s', '--skip', default=SKIP_DEFAULT, help='How many words to skip backwards', metavar='skip', type=int)
parser.add_argument('-w', '--window', default=DEFAULT_WINDOW_SIZE, help='Size of a tautology window', type=int, metavar='window')
parser.add_argument('-b', '--ban-list', default=BAN_DEFAULT, help='List of stop-words that will be skipped', metavar='stop words',
        nargs='+')
parser.add_argument('-u', '--undo', help='Clear all marks from text', action='store_true')
args = parser.parse_args()
# Get selected text from stdin
words = []
for line in sys.stdin:
    words = words + line.split(' ')
# Decide what to do next
if args.undo:
    # User chose to remove all marks from the text
    clean_marks(words, mark=args.mark)
else:
    # User chose to detect and mark tautologies
    detect_tautologies(words, stain=args.mark, window=args.window, skip=args.skip, ban_list=args.ban_list)
# Now, when we have processed list of `words`,
# We can print them line by line
echo(words)
