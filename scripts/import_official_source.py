from __future__ import annotations

import argparse
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.config import Settings
from app.database import create_db_engine, init_database
from app.services.importer import discover_import_files, import_documents


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import official source markdown files into the support desk database.")
    parser.add_argument("--file", dest="file_path", help="Single markdown file to import")
    parser.add_argument(
        "--dir",
        dest="directory",
        default=str(REPO_ROOT / "raw_sources" / "incoming"),
        help="Directory containing markdown source files",
    )
    parser.add_argument("--database-url", dest="database_url", help="Override database URL")
    parser.add_argument("--validate-only", action="store_true", help="Parse and validate without writing to the database")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    target = Path(args.file_path) if args.file_path else Path(args.directory)
    files = discover_import_files(target)
    if not files:
        print(f"No importable markdown files found under: {target}")
        return 1

    settings = Settings()
    database_url = args.database_url or settings.database_url
    engine = create_db_engine(database_url)
    init_database(engine)

    result = import_documents(engine, files, dry_run=args.validate_only)
    print(f"Imported files: {', '.join(result.imported_files)}")
    print(f"Entity counts: {result.entity_counts}")
    if result.db_counts:
        print(f"Database counts: {result.db_counts}")
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"- {warning}")
    print("Validation only." if result.dry_run else "Import completed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
