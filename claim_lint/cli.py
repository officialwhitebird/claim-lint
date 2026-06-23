import sys
import os
import argparse
import json
from claim_lint.config import load_config, ConfigError
from claim_lint.scanner import scan_file

def main():
    parser = argparse.ArgumentParser(
        description="Local-first deterministic text scanner for unevidenced claims and internal names."
    )
    
    subparsers = parser.add_subparsers(dest="command", required=True)
    scan_parser = subparsers.add_parser("scan", help="Scan a text file for policy violations.")
    
    scan_parser.add_argument("file_path", help="Path to the file to scan.")
    scan_parser.add_argument("--config", help="Path to the .claimlintrc.json config file.")
    scan_parser.add_argument("--json", action="store_true", help="Output findings in JSON format.")
    
    args = parser.parse_args()

    if args.command == "scan":
        # 1. Config ロード
        try:
            config = load_config(args.config)
        except ConfigError as e:
            if args.json:
                print(json.dumps({
                    "ok": False,
                    "summary": {"total_errors": 1},
                    "findings": [{
                        "severity": "ERROR",
                        "code": e.code,
                        "line": 0,
                        "matched_text": "",
                        "rule_source": "config",
                        "repair_guidance": str(e)
                    }]
                }, indent=2))
            else:
                sys.stderr.write(f"ERROR {e.code} [line 0]: {str(e)}\n")
            sys.exit(2)
        except Exception as e:
            sys.exit(2)

        # 2. ファイルスキャン
        if not os.path.exists(args.file_path):
            message = f"File not found: {args.file_path}"
            if args.json:
                print(json.dumps({
                    "ok": False,
                    "summary": {"total_errors": 1},
                    "findings": [{
                        "severity": "ERROR",
                        "code": "file.missing",
                        "line": 0,
                        "matched_text": "",
                        "rule_source": "file",
                        "repair_guidance": message
                    }]
                }, indent=2))
            else:
                sys.stderr.write(f"ERROR file.missing [line 0]: {message}\n")
            sys.exit(2)

        try:
            findings = scan_file(args.file_path, config)
        except Exception as e:
            sys.exit(2)

        # 3. 出力制御
        if args.json:
            output = {
                "ok": len(findings) == 0,
                "summary": {
                    "total_errors": len(findings)
                },
                "findings": [f.to_dict() for f in findings]
            }
            print(json.dumps(output, indent=2))
        else:
            if findings:
                for f in findings:
                    print(f"ERROR {f.code} [line {f.line}]: matched '{f.matched_text}' (rule: {f.rule_source}) -> {f.repair_guidance}")
            else:
                print("No findings.")

        # 4. 終了コード
        if findings:
            sys.exit(1)
        else:
            sys.exit(0)

if __name__ == "__main__":
    main()
