#!/usr/bin/env python3
"""Search the embedded-design practices and print selected sections."""

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import math
import re
import unicodedata


CORPUS = Path(__file__).resolve().parents[1] / "references" / "saho"
SECTIONS = {
    "basis": "判断の根拠",
    "checks": "確認事項",
    "notes": "留意点",
    "related": "関連作法",
    "diagram": "作図の観点",
    "figures": "原典の図表",
}
ID_PATTERN = re.compile(r"[A-D]-[1-9][0-9]*")
METADATA = ("適用場面", "検索語", "出典")


@dataclass
class Practice:
    path: Path
    title: str
    summary: str
    keywords: str
    source: str
    sections: dict

    @classmethod
    def read(cls, path):
        head, *sections = re.split(r"^## ", path.read_text(encoding="utf-8"), flags=re.M)
        heading, *lines = head.strip().splitlines()
        prefix = f"# {path.stem} "
        if not heading.startswith(prefix):
            raise ValueError(f"{path.name}: 作法IDと見出しが一致しません")
        fields = dict(line[2:].split("｜", 1) for line in lines if line.startswith("- "))
        content = {}
        for section in sections:
            title, _, body = section.partition("\n")
            content[title] = body.strip()
        return cls(path, heading[len(prefix):], *(fields[key] for key in METADATA), content)

    @property
    def search_fields(self):
        headings = (SECTIONS[key] for key in ("basis", "checks", "notes", "diagram"))
        body = " ".join(self.sections.get(heading, "") for heading in headings)
        return (
            (self.title, 6),
            (self.keywords, 5),
            (self.summary, 3),
            (body, 1),
        )


def normalize(text):
    return unicodedata.normalize("NFKC", text).casefold()


def words(text):
    return re.findall(r"[a-z0-9]+|[^\W_a-z0-9]+", normalize(text))


def grams(term):
    if term.isascii() or len(term) == 1:
        return {term}
    return {term[i:i + 2] for i in range(len(term) - 1)}


def rank(practices, query):
    terms = set(words(query))
    if not terms:
        return []

    # Use document frequency across the entire Markdown corpus to downweight
    # common fragments such as 「する」 in longer queries.
    index = []
    frequency = Counter()
    for practice in practices:
        weights = {}
        for field, weight in practice.search_fields:
            for word in words(field):
                for gram in grams(word):
                    weights[gram] = max(weights.get(gram, 0), weight)
        index.append(weights)
        frequency.update(weights.keys())

    query_grams = {term: grams(term) for term in terms}
    inverse_frequency = {
        gram: math.log1p(len(practices) / (1 + frequency[gram]))
        for keys in query_grams.values()
        for gram in keys
    }
    matches = []
    for practice, weights in zip(practices, index):
        score = 0.0
        for term in sorted(terms):
            keys = query_grams[term]
            exact_weight = max(
                (weight for field, weight in practice.search_fields if
                 (term in words(field) if term.isascii() else term in normalize(field))),
                default=0,
            )
            shared = keys & weights.keys()
            covered = sum(inverse_frequency[key] for key in sorted(shared))
            total = sum(inverse_frequency[key] for key in sorted(keys))
            if exact_weight or (len(shared) >= 2 and covered / total >= 0.32):
                score += 2 * exact_weight + sum(
                    weights[key] * inverse_frequency[key] for key in sorted(shared)
                ) / total
        if score:
            part, number = practice.path.stem.split("-")
            matches.append((-score, part, int(number), practice))
    return [practice for _, _, _, practice in sorted(matches)]


def serve_search(args):
    query = " ".join(args.query).strip()
    practice_id = normalize(query).upper()
    if ID_PATTERN.fullmatch(practice_id):
        path = CORPUS / f"{practice_id}.md"
        candidates = [Practice.read(path)] if path.is_file() else []
    else:
        practices = [Practice.read(path) for path in CORPUS.glob("*.md")
                     if ID_PATTERN.fullmatch(path.stem)]
        if not practices:
            raise ValueError("作法MDが見つかりません")
        candidates = rank(practices, query)

    page = candidates[args.offset:args.offset + 3]
    if not page:
        print("該当する候補はありません。" if not args.offset else "追加の候補はありません。")
    for practice in page:
        print(f"{practice.path.stem} {practice.title}｜{practice.summary}")


def serve_show(args):
    practice_id = normalize(args.id).strip().upper()
    if not ID_PATTERN.fullmatch(practice_id):
        raise ValueError(f"作法IDの形式が無効です: {args.id}")
    path = CORPUS / f"{practice_id}.md"
    if not path.is_file():
        raise ValueError(f"{practice_id} の作法MDが見つかりません")
    practice = Practice.read(path)
    relative_path = path.relative_to(CORPUS.parents[4])
    print(f"# {practice_id} {practice.title}")
    print(f"{practice.source}｜{relative_path.as_posix()}")
    if not args.section:
        print(f"適用場面｜{practice.summary}")
        if SECTIONS["diagram"] in practice.sections:
            print("作図の観点あり（--section diagram）")
    for key in dict.fromkeys(args.section or ("basis", "checks")):
        heading = SECTIONS[key]
        print(f"\n## {heading}\n{practice.sections.get(heading, 'この節の記載なし。')}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    command = parser.add_subparsers(required=True)
    search = command.add_parser("search", help="検索結果を最大3件表示")
    search.add_argument("query", nargs="+")
    search.add_argument("--offset", type=int, default=0)
    search.set_defaults(run=serve_search)
    show = command.add_parser("show", help="指定した作法の必要な節を表示")
    show.add_argument("id")
    show.add_argument("--section", action="append", choices=SECTIONS)
    show.set_defaults(run=serve_show)
    args = parser.parse_args()
    if getattr(args, "offset", 0) < 0:
        parser.error("--offset は0以上を指定してください")
    try:
        args.run(args)
    except (OSError, KeyError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    main()
