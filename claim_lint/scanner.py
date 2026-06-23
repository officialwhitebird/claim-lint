from dataclasses import dataclass, asdict

@dataclass
class Finding:
    severity: str
    code: str
    line: int
    matched_text: str
    rule_source: str
    repair_guidance: str

    def to_dict(self):
        return asdict(self)

def scan_file(file_path, config):
    findings = []
    
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    prohibited_claims = config.get("prohibited_claims", [])
    internal_names = config.get("internal_names", [])

    for idx, line in enumerate(lines, start=1):
        line_lower = line.lower()
        
        # prohibited_claims のマッチング
        for claim in prohibited_claims:
            if not claim:
                continue
            if claim.lower() in line_lower:
                # 実際の元テキストでのマッチ箇所を抽出（正確な表現のため）
                # 簡易のため、line_lower.find(claim.lower()) を使い、元の大文字小文字を維持したテキストを切り取る
                start_pos = line_lower.find(claim.lower())
                matched_text = line[start_pos : start_pos + len(claim)]
                
                findings.append(Finding(
                    severity="ERROR",
                    code="claim.prohibited",
                    line=idx,
                    matched_text=matched_text,
                    rule_source="prohibited_claims",
                    repair_guidance="Remove unevidenced performance claim."
                ))

        # internal_names のマッチング
        for name in internal_names:
            if not name:
                continue
            if name.lower() in line_lower:
                start_pos = line_lower.find(name.lower())
                matched_text = line[start_pos : start_pos + len(name)]
                
                findings.append(Finding(
                    severity="ERROR",
                    code="internal-name.detected",
                    line=idx,
                    matched_text=matched_text,
                    rule_source="internal_names",
                    repair_guidance="Remove internal project name leak."
                ))

    return findings
