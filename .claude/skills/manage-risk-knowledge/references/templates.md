# Templates for Risk Knowledge Files

Use these templates when creating new files. Follow the structure exactly.

## spec.md Template

```markdown
# [ドメイン名]ドメイン仕様

## 概要

[このドメインの目的とスコープを1-2文で記述]

## コアコンポーネント

### 1. [コンポーネント名]

- [コンポーネントに関する重要なポイント]
- [別の重要なポイント]

### 2. [コンポーネント名]

- [コンポーネントに関する重要なポイント]

## APIエンドポイント

| エンドポイント | メソッド | 説明 |
|----------|--------|-------------|
| /api/... | POST | ... |
| /api/... | GET | ... |

## 依存関係

- [外部サービスまたはシステム]
- [データベースまたはストレージ]
```

## risks.md Template

```markdown
# [ドメイン名]ドメインのリスク

[ドメイン名]システムのアーキテクチャと実装に固有のリスク。

## 1. [リスク名]

- **詳細**: [何が問題になるか、なぜ発生するか]
- **対策**:
  - [対策手順1]
  - [対策手順2]
- **重要度**: [重大/高/中/低]
- **関連インシデント**: `incidents/YYYY-incident-name.md` (該当する場合)

## 2. [リスク名]

- **詳細**: [何が問題になるか、なぜ発生するか]
- **対策**:
  - [対策手順1]
- **重要度**: [重大/高/中/低]
```

## incidents/ File Template

```markdown
# インシデント: [短い説明的なタイトル]

## サマリー

- **日時**: YYYY-MM-DD
- **継続時間**: X時間（HH:MM - HH:MM TZ）
- **重要度**: [重大/高/中/低]
- **影響を受けたユーザー**: [数または割合]

## インシデント説明

[ユーザー視点で何が起こったかを2-3文で記述]

## 根本原因

[なぜこれが発生したかの技術的説明]

## タイムライン

| 時刻 | イベント |
|------|-------|
| HH:MM | [イベントの説明] |
| HH:MM | [イベントの説明] |

## 影響

- [ビジネス影響1]
- [ビジネス影響2]

## 学んだ教訓

1. [重要なポイント1]
2. [重要なポイント2]

## 関連リスク

- `domains/[domain]/risks.md` - [Risk name]
- `common-risks/[category].md` - [Risk name]

## Action Items

- [ ] [Action 1]
- [ ] [Action 2]
```

## knowledge-map.yml Entry Template

```yaml
  - domain_name: "[Domain Name in Japanese] ([English Name])"
    description: "[What this domain covers]"
    keywords:
      - "keyword1"
      - "keyword2"
      - "keyword3"
    related_files:
      common_risks:
        - "common-risks/[relevant].md"
      domain_knowledge:
        - "domains/[domain-name]/spec.md"
        - "domains/[domain-name]/risks.md"
```
