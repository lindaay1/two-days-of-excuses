#!/usr/bin/env python3
"""Two Days of Excuses — make.fun program entry.

Competition: u-jolly-fox-32-two-days-of-excuses-3f18797e.

One line, 1 to 200 characters: the funniest excuse for a missed
deadline. The approved excuse is streamed through a word iterator:
each word is checked in turn against the gate, and the iterator refuses
to hand over the line until every word has passed. publish() writes
entry.txt and its mirror excuses.txt and reads both back to prove they
are byte-identical to the approved line.
"""

import hashlib
import sys

EXCUSE = (
    "I missed the deadline because I spent all day writing an apology "
    "for missing the deadline, and the apology also missed its deadline."
)

GATE_MIN = 1
GATE_MAX = 200


class WordStream:
    """An iterator over the excuse's words, gate-checking as it goes."""

    def __init__(self, text):
        self._text = text
        self._words = text.split(" ")
        self._pos = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._pos >= len(self._words):
            raise StopIteration
        word = self._words[self._pos]
        self._pos += 1
        if word == "":
            raise ValueError("excuse contains a double space")
        return word

    def collect(self):
        words = list(self)
        rebuilt = " ".join(words)
        if rebuilt != self._text:
            raise ValueError("rebuilt excuse differs from the approved line")
        return rebuilt


def gate_ok(text):
    if not isinstance(text, str):
        raise ValueError("excuse is not text")
    if not GATE_MIN <= len(text) <= GATE_MAX:
        raise ValueError(
            "excuse is %d chars, gate is %d-%d" % (len(text), GATE_MIN, GATE_MAX)
        )
    if text.strip() == "":
        raise ValueError("excuse is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("excuse must be a single line")
    if "deadline" not in text.lower():
        raise ValueError("excuse does not mention the deadline")


def publish(text):
    gate_ok(text)
    stream = WordStream(text)
    checked = stream.collect()
    blob = checked.encode("utf-8")
    for name in ("entry.txt", "excuses.txt"):
        with open(name, "wb") as fh:
            fh.write(blob)
    for name in ("entry.txt", "excuses.txt"):
        with open(name, "rb") as fh:
            if fh.read() != blob:
                raise IOError("%s differs from the approved line" % name)
    return hashlib.sha256(blob).hexdigest(), len(list(WordStream(text)))


def main(argv):
    if len(argv) > 1 and argv[1] == "--peek":
        stream = WordStream(EXCUSE)
        peeked = [next(stream) for _ in range(5)]
        print("first 5 words: %s" % " ".join(peeked))
        rest = list(stream)
        print("remaining words: %d" % len(rest))
        print("total words: %d" % (len(peeked) + len(rest)))
        gate_ok(EXCUSE)
        print("gate: PASS")
        print("sha256 %s" % hashlib.sha256(EXCUSE.encode("utf-8")).hexdigest())
        return 0
    sha, word_count = publish(EXCUSE)
    print("wrote %d chars (%d words), sha256 %s" % (len(EXCUSE), word_count, sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
