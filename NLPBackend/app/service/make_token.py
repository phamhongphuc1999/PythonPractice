import os
import subprocess

PAD = 0
UNK = 1
START = 2
END = 3

dm_single_close_quote = "\u2019"  # unicode
dm_double_close_quote = "\u201d"
# acceptable ways to end a sentence
END_TOKENS = [
    ".",
    "!",
    "?",
    "...",
    "'",
    "`",
    '"',
    dm_single_close_quote,
    dm_double_close_quote,
    ")",
]


def tokenize_stories(story: str):
    with open("story/story.txt", "w") as f:
        f.write(story)
    stories = os.listdir("story")
    with open("mapping.txt", "w") as f:
        for s in stories:
            f.write(
                "{} \t {}\n".format(os.path.join("story", s), os.path.join("story1", s))
            )
    command = [
        "java",
        "edu.stanford.nlp.process.PTBTokenizer",
        "-ioFileList",
        "-preserveLines",
        "mapping.txt",
    ]
    subprocess.call(command)
    os.remove("mapping.txt")
    f = open("story1/story.txt", "r")
    _data = f.read()
    f.close()
    return _data


def fix_missing_period(line):
    """Adds a period to a line that is missing a period"""
    if line == "":
        return line
    if line[-1] in END_TOKENS:
        return line
    return line + " ."


def get_article(story: str):
    article_list = story.split("\n")
    lines = []
    for _article in article_list:
        lines += _article.split(". ")
    lines = [" ".join(line.lower().strip().split()) for line in lines]
    lines = [fix_missing_period(line) for line in lines]
    return lines
