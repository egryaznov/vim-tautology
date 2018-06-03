This repository contains sources for a vim plugin that detects and marks recurring words in your text.


## Description
If you like me then you often repeat yourself when writing a piece of English text. The same word can occur multiple times in the same
paragraph, which makes a reader bored and frustrated. For instance, consider the following passage:

I was in school today. School is still the same old, dull place that it always was. Today an old man came to me and asked about my
place. I didn't answer because I was late for school.

Notice that the words "school", "old", "today", "place" are redundant and must be replaced to increase the readability of the text.
Such pesky recurring words can be hard to trace, so I've created this plugin to facilitate the process.

The plugin marks all tautologies in a given piece of text by prefixing them with a specified symbol, '@' by default.


## How To Use
There are two pre-defined commands `TautologyMark` and `TautologyClear`. The former marks all tautologies in selected text, and
latter removes all inserted marks. Step-by-step usage:

0. Set the variable `g:tautology_dir` to the directory of the file `vim-tautology.vim` to ensure that the python script will work. Default is `~/.vim/plugged/vim-tautology`.
1. Select the text you want to snoop for tautologies, for example with `vip`:
2. Run `:TautologyMark`
**I @was in school @today. School is still the same @old, dull @place that it always @was. @Today an @old man came to me and asked
about my @place. I didn't answer because I @was late for school.**
3. Circle through with `/@\w*`, edit, remove or replace them with synonyms, etc...
4. When you done, simply `gv` and run `:TautologyClear`, this will remove all marks that are still left.

## Installation and Prerequisites
Install via your favorite vim plugin manager. I suggest using [vim-plug](https://github.com/junegunn/vim-plug), just place the
following in your `.vimrc`:

`Plug 'egryaznov/vim-tautology'`

You will need the last version of Vim and the third version of python interpreter to run the plugin. Make sure the command `python3` is
available on your system.

**IMPORTANT**
Manually set the path to the directory of this plugin by assigning it to the variable `g:tautology_dir`. For example, default is:
`let g:tautology_dir = ~/.vim/plugged/vim-tautology/`. Change it if you either of Windows or not using vim-plug.


## Configuration
There are 4 main variables that let you control the behaviour of this plugin:
1. `g:tautology_mark`. The string that will be used as a prefix to recurring words. Default value is `@`.
2. `g:tautology_stop_words`. The list of words that are too ubiquitous to consider, like "and", "the", "as" and so on. The words in this list
   will be omitted when marking tautologies. Default is `['I', 'the', 'a', 'an', 'to', 'be', 'of', 'and', 'in', 'that', 'this',
   'as']`.
3. `g:tautology_window_size`. Controls how many words behind the examined word is compared with. Default is `30`.
4. `g:tautology_skip`. Controls how many words directly before the examined word is skipped to prevent overabundance of marks.

Last two variables define the so-called **window** of tautologies. For example, suppose `window_size = 6`, `tautology_skip = 2` and current
word is `dog`, then the window in the following text will be:

The quick **[brown fox jumps over]** the lazy dog.


## Mappings
Of course, typing all these commands is laborious, so you can set `g:tautology_mappings = 1` to use `gz` as `:TautologyMark` and `gZ` as
`:TautologyClear`. Please note that these mappings work only in **visual mode.**

## Issues
Currently a sharp symbol `#` cannot be set as a mark, because Vim treats it as a name of *alternate file* (see `:h alternate-file`).
Avoid it and use `@` instead. This problem may be fixed soon.
