---
project: "\u533B\u7642\u6CD5\u4EBA\u793E\u56E3 \u84BC\u6A39\u4F1A \u307F\u306A\u307F\
  \u91CE\u5973\u6027\u533B\u7642\u30BB\u30F3\u30BF\u30FC"
source: "/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive/share/\u5171\
  \u6709\u30C9\u30E9\u30A4\u30D6/\u30D7\u30ED\u30B8\u30A7\u30AF\u30C8/\u533B\u7642\
  \u6CD5\u4EBA\u793E\u56E3 \u84BC\u6A39\u4F1A \u307F\u306A\u307F\u91CE\u5973\u6027\
  \u533B\u7642\u30BB\u30F3\u30BF\u30FC/04.\u5206\u6790/analysis_project/data/\u30AB\
  \u30E9\u30E0\u8AAC\u660E.md"
tags:
- drive_extraction
- "\u533B\u7642\u6CD5\u4EBA\u793E\u56E3 \u84BC\u6A39\u4F1A \u307F\u306A\u307F\u91CE\
  \u5973\u6027\u533B\u7642\u30BB\u30F3\u30BF\u30FC"
timestamp: '2026-07-03T09:16:20.953007'
title: "\u30AB\u30E9\u30E0\u8AAC\u660E.md"
type: material

---

### train.csv

| カラム | ヘッダ名称 | データ型 | 説明 |
| --- | --- | --- | --- |
| 0 | index | int | インデックスとして使用 |
| 1 | Pregnancies | int | 妊娠した回数 |
| 2 | Glucose | int | 経口ブドウ糖負荷試験における2時間の血漿ブドウ糖濃度 |
| 3 | BloodPressure | int | 拡張期血圧 |
| 4 | SkinThickness | int | 皮膚のひだの厚さ |
| 5 | Insulin | int | 血清インスリン |
| 6 | BMI | float | BMI |
| 7 | Age | int | 年齢 |
| 8 | DiabetesPedigreeFunction | float | 糖尿病血統（家族歴に基づいて糖尿病にかかる可能性をスコアリングした数値） |
| 9 | **Outcome** | int | 糖尿病であるか（糖尿病の場合1、でない場合0） |

※黄色く色付けされた変数（上記表の **Outcome**）が目的変数です（評価用データには含まれません）。