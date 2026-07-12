---
project: "\u4EAC\u6A4B\u4FE1\u7528\u30BD\u30EA\u30E5\u30FC\u30B7\u30E7\u30F3\u30B9\
  \u3099\u682A\u5F0F\u4F1A\u793E"
source: "/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive/share/\u5171\
  \u6709\u30C9\u30E9\u30A4\u30D6/\u30D7\u30ED\u30B8\u30A7\u30AF\u30C8/\u4EAC\u6A4B\
  \u4FE1\u7528\u30BD\u30EA\u30E5\u30FC\u30B7\u30E7\u30F3\u30B9\u3099\u682A\u5F0F\u4F1A\
  \u793E/03.\u30C6\u3099\u30FC\u30BF/\u30AB\u30E9\u30E0\u8AAC\u660E.md"
tags:
- drive_extraction
- "\u4EAC\u6A4B\u4FE1\u7528\u30BD\u30EA\u30E5\u30FC\u30B7\u30E7\u30F3\u30B9\u3099\u682A\
  \u5F0F\u4F1A\u793E"
timestamp: '2026-07-03T09:16:20.327314'
title: "\u30AB\u30E9\u30E0\u8AAC\u660E.md"
type: material

---

| カラム名 | データ型 | 説明 | データの例 |
| --- | --- | --- | --- |
| **id** | 整数 | 顧客の一意の識別ID | `1`, `2` |
| **age** | 整数 | 顧客の年齢 | `39`, `51` |
| **job** | 文字列 | 職業 | `blue-collar`, `management` |
| **marital** | 文字列 | 婚姻状況 | `married`, `single` |
| **education** | 文字列 | 学歴 | `secondary`, `tertiary` |
| **default** | 文字列 | 債務不履行（デフォルト）の有無 | `no`, `yes` |
| **balance** | 整数 | 年間平均残高（口座残高） | `1756`, `436` |
| **housing** | 文字列 | 住宅ローンの有無 | `yes`, `no` |
| **loan** | 文字列 | 個人ローンの有無 | `no`, `yes` |
| **contact** | 文字列 | 連絡手段 | `cellular`, `telephone` |
| **day** | 整数 | 最後に連絡した日（日にち） | `3`, `18` |
| **month** | 文字列 | 最後に連絡した月 | `apr`, `feb` |
| **duration** | 整数 | 最後の連絡の通話時間（秒） | `939`, `172` |
| **campaign** | 整数 | 今回のキャンペーンにおける連絡回数 | `1`, `10` |
| **pdays** | 整数 | 前回のキャンペーンで最後に連絡してからの経過日数（-1は未連絡） | `-1`, `595` |
| **previous** | 整数 | 今回のキャンペーンより前に行われた連絡回数 | `0`, `2` |
| **poutcome** | 文字列 | 前回のキャンペーンの結果 | `unknown`, `success` |
| **y** | 整数 | (目的変数)定期預金などを契約したかどうか（目的変数 / 1: 契約, 0: 未契約など） | `1`, `0` |
