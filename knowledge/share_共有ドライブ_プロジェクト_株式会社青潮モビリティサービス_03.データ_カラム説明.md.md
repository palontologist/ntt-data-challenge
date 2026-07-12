---
project: "\u682A\u5F0F\u4F1A\u793E\u9752\u6F6E\u30E2\u30D2\u3099\u30EA\u30C6\u30A3\
  \u30B5\u30FC\u30D2\u3099\u30B9"
source: "/home/palontologist/Downloads/dev/ntt_data_challenge/raw_drive/share/\u5171\
  \u6709\u30C9\u30E9\u30A4\u30D6/\u30D7\u30ED\u30B8\u30A7\u30AF\u30C8/\u682A\u5F0F\
  \u4F1A\u793E\u9752\u6F6E\u30E2\u30D2\u3099\u30EA\u30C6\u30A3\u30B5\u30FC\u30D2\u3099\
  \u30B9/03.\u30C6\u3099\u30FC\u30BF/\u30AB\u30E9\u30E0\u8AAC\u660E.md"
tags:
- drive_extraction
- "\u682A\u5F0F\u4F1A\u793E\u9752\u6F6E\u30E2\u30D2\u3099\u30EA\u30C6\u30A3\u30B5\u30FC\
  \u30D2\u3099\u30B9"
timestamp: '2026-07-03T09:16:19.748667'
title: "\u30AB\u30E9\u30E0\u8AAC\u660E.md"
type: material

---

### train.tsv

| カラム | ヘッダ名称 | データ型 | 説明 |
| --- | --- | --- | --- |
| 0 | id | int | インデックスとして使用 |
| 1 | dteday | date | 日付（2011-01-01～2012-12-31） |
| 2 | season | int | 季節（1=春, 2=夏, 3=秋, 4=冬） |
| 3 | yr | bit | 年（0=2011, 1=2012） |
| 4 | mnth | int | 月 |
| 5 | hr | int | 時間 |
| 6 | holiday | bit | 祝日（1=祝日） |
| 7 | weekday | int | 曜日（0=日, 1=月...6=土） |
| 8 | workingday | bit | 平日（0=平日, 1=祝日） |
| 9 | weathersit | int | 天気（1=晴,やや曇り, 2=薄い霧+曇り,霧+千切れ曇,霧+やや曇り,薄い霧, 3=小雪,小雨+雷雨+千切れ曇,小雨+千切れ曇, 4=大雨+凍雨+雷雨+霧,雪+濃い霧） |
| 10 | temp | float | 規格化した温度（摂氏）（（t-t_min）/（t_max-t_min）, t_min=-8, t_max=+39） |
| 11 | atemp | float | 規格化した体感温度（摂氏）（（t-t_min）/（t_max-t_min）, t_min=-16, t_max=+50） |
| 12 | hum | float | 規格化した湿度（最大値の100で割った値） |
| 13 | windspeed | float | 規格化した風速（最大値の67で割った値） |
| 14 | **cnt** | int | 利用者数 |

※黄色く色付けされた変数（上記表の **cnt**）が目的変数です（評価用データには含まれません）。