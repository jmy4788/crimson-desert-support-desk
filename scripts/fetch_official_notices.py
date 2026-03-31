from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import Settings
from app.database import create_db_engine, init_database
from app.services.importer import import_documents, parse_import_document
from app.services.official_notice_fetcher import (
    SUPPORTED_TYPES,
    fetch_notice_detail,
    fetch_notice_summaries,
    generate_documents,
    write_documents,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch official Crimson Desert notices and turn them into importable markdown drafts."
    )
    parser.add_argument("--locale", default="ko-KR", help="Official site locale, e.g. ko-KR or en-US")
    parser.add_argument("--pages", type=int, default=4, help="How many notice pages to scan")
    parser.add_argument("--max-items", type=int, help="Maximum number of notices to fetch after filtering")
    parser.add_argument(
        "--source-type",
        action="append",
        choices=sorted(SUPPORTED_TYPES),
        help="Limit fetched notices to one or more source types",
    )
    parser.add_argument(
        "--output-dir",
        default=str(REPO_ROOT / "raw_sources" / "incoming" / "auto"),
        help="Directory where draft markdown files will be written",
    )
    parser.add_argument("--clean-output", action="store_true", help="Delete existing markdown drafts in output-dir first")
    parser.add_argument("--database-url", dest="database_url", help="Override database URL")
    parser.add_argument("--validate-only", action="store_true", help="Write drafts and validate them only")
    parser.add_argument("--import-after-write", action="store_true", help="Import the generated drafts into the database")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    source_types = set(args.source_type or SUPPORTED_TYPES)
    notices = fetch_notice_summaries(locale=args.locale, pages=args.pages, source_types=source_types)
    if args.max_items:
        notices = notices[: args.max_items]

    if not notices:
        print("No matching official notices were found.")
        return 1

    documents = []
    for notice in notices:
        detail = fetch_notice_detail(notice)
        documents.extend(generate_documents(detail))

    if not documents:
        print("Notices were fetched, but no importable drafts were generated.")
        return 1

    output_dir = Path(args.output_dir).resolve()
    if args.clean_output and output_dir.exists():
        for existing in output_dir.glob("*.md"):
            existing.unlink()

    written_paths = write_documents(documents, output_dir)
    print(f"Fetched notices: {len(notices)}")
    print(f"Generated drafts: {len(written_paths)}")
    for path in written_paths:
        try:
            display_path = path.relative_to(REPO_ROOT)
        except ValueError:
            display_path = path
        print(f"- {display_path}")

    for path in written_paths:
        parse_import_document(path)
    print("Draft validation passed.")

    if args.validate_only and not args.import_after_write:
        return 0

    if args.import_after_write:
        settings = Settings()
        database_url = args.database_url or settings.database_url
        engine = create_db_engine(database_url)
        init_database(engine)
        result = import_documents(engine, written_paths, dry_run=False)
        print(f"Imported files: {', '.join(result.imported_files)}")
        print(f"Database counts: {result.db_counts}")
        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"- {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
