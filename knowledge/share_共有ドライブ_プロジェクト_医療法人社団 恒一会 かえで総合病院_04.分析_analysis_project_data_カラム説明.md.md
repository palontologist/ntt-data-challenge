---
project: "\u533B\u7642\u6CD5\u4EBA\u793E\u56E3 \u6052\u4E00\u4F1A \u304B\u3048\u3066\
  \u3099\u7DCF\u5408\u75C5\u9662"
source: "/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive/share/\u5171\
  \u6709\u30C9\u30E9\u30A4\u30D6/\u30D7\u30ED\u30B8\u30A7\u30AF\u30C8/\u533B\u7642\
  \u6CD5\u4EBA\u793E\u56E3 \u6052\u4E00\u4F1A \u304B\u3048\u3066\u3099\u7DCF\u5408\
  \u75C5\u9662/04.\u5206\u6790/analysis_project/data/\u30AB\u30E9\u30E0\u8AAC\u660E\
  .md"
tags:
- drive_extraction
- "\u533B\u7642\u6CD5\u4EBA\u793E\u56E3 \u6052\u4E00\u4F1A \u304B\u3048\u3066\u3099\
  \u7DCF\u5408\u75C5\u9662"
timestamp: '2026-07-03T09:16:20.898380'
title: "\u30AB\u30E9\u30E0\u8AAC\u660E.md"
type: material

---

### train.csv

| カラム | ヘッダ名称 | データ型 | 説明 |
| --- | --- | --- | --- |
| 0 | id | int | インデックスとして使用 |
| 1 | Age | int | 年齢 |
| 2 | Gender | char | 性別 |
| 3 | T_Bil | float | 検査項目1： 総ビリルビン (Total Bilirubin) |
| 4 | D_Bil | float | 検査項目2： 直接ビリルビン (Direct Bilirubin) |
| 5 | ALP | float | 検査項目3： アルカリフォスファターゼ (Alkaline Phosphotase) |
| 6 | ALT_GPT | float | 検査項目4： アラニンアミノトランスフェラーゼ (Alanine Transaminase) |
| 7 | AST_GOT | float | 検査項目5： アスパラギン酸アミノトランスフェラーゼ (Aspartate Aminotransferase) |
| 8 | TP | float | 検査項目6： 総タンパク (Total Protiens) |
| 9 | Alb | float | 検査項目7： アルブミン (Albumin) |
| 10 | AG_ratio | float | 検査項目8： アルブミン/グロブリン比 |
| 11 | **disease** | int | 肝疾患の有無（0:無, 1:有） |

※黄色く色付けされた変数（上記表の **disease**）が目的変数です（評価用データには含まれません）。