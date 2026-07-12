---
project: "\u533B\u7642\u6CD5\u4EBA\u793E\u56E3 \u84BC\u6CC9\u4F1A \u3072\u304B\u3099\
  \u3057\u4E18\u7DCF\u5408\u75C5\u9662"
source: "/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive/share/\u5171\
  \u6709\u30C9\u30E9\u30A4\u30D6/\u30D7\u30ED\u30B8\u30A7\u30AF\u30C8/\u533B\u7642\
  \u6CD5\u4EBA\u793E\u56E3 \u84BC\u6CC9\u4F1A \u3072\u304B\u3099\u3057\u4E18\u7DCF\
  \u5408\u75C5\u9662/03.\u30C6\u3099\u30FC\u30BF/\u30AB\u30E9\u30E0\u8AAC\u660E.md"
tags:
- drive_extraction
- "\u533B\u7642\u6CD5\u4EBA\u793E\u56E3 \u84BC\u6CC9\u4F1A \u3072\u304B\u3099\u3057\
  \u4E18\u7DCF\u5408\u75C5\u9662"
timestamp: '2026-07-03T09:16:20.103138'
title: "\u30AB\u30E9\u30E0\u8AAC\u660E.md"
type: material

---

### train.csv

| カラム | ヘッダ名称 | データ型 | 説明 |
| --- | --- | --- | --- |
| 0 | id | int | インデックスとして使用 |
| 1 | age | int | 年齢 |
| 2 | sex | category | 性別 |
| 3 | bmi | float | BMI |
| 4 | children | int | 子供の数 |
| 5 | smoker | category | 喫煙しているか |
| 6 | region | category | 地域 |
| 7 | **charges** | int | 価格帯0（低）、1（中）、2（高） |

※黄色く色付けされた変数（上記表の **charges**）が目的変数です（評価用データには含まれません）。