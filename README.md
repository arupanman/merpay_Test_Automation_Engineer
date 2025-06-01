## 概要
このリポジトリはmerpayQA summer internship向けのTest Automation Engineer選考課題の回答です。ホテル予約システムのWeb UIテスト自動化フレームワークとして、Seleniumと Page Object Model (POM) パターンを使用して実装しています。

## 設計方針
- **Page Object Model**: 各画面ごとにページオブジェクトを作成し、画面操作と検証をカプセル化
- **再利用性**: 共通機能は基底クラス（BasePage）に実装し継承で再利用
- **メンテナンス性**: セレクタはページクラスにロケーターとして一元管理
- **読みやすさ**: メソッドチェーンで操作の流れを直感的に表現

# 課題1実行コマンド
python Assignment_1_test.py

# 課題2実行コマンド
python Assignment_2_test.py