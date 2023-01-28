===========================================
The "EYE" component for Game Ad Automation
===========================================

概要
=====

Game Ad Autometionの目となるコンポーネント。
GAA本体からの画像を入力として、検出した物体とそのscoreを返却する。
現状のバージョンではGame画像を入力として、DetectionResultContainerを返却する。


処理の概要
=============

現状のバージョンでは、pytorch(SSD)とResNet34を統合する。
入力画像を最初にpytorch(SSD)に通して、検出した画像の各種パートを得る。
ここで得られた各画像はclose(や将来的に他の「広告をみる」ボタンなど)の候補だが、SSDではcloseかどうかの判定精度が甘いので、
その次に、各画像に対してResNet34で最終判断をかける。


処理の詳細
=============

1. GameEyeが画像を入力する
2. GameEyeがpytorch(SSD)を呼び出す。その際、1.の画像を入力とする
3. pytorch(SSD)がGameEyeに解析してほしいimage_logのディレクトリ名を返す
4. GameEyeがimage_logを読み込む。ResNet34のlabelsオプションを事前に実行して、ラベルとラベル数値のハッシュ値を作っておく。
5. DetectionResultContainerの内容を列挙する
5-1. エントリにある画像ファイルをResNet34に渡す。
5-2. ResNet34が検出結果を返す。それを上記ハッシュ値からラベルに変換する
5-3. 5-1のエントリのラベルとスコアを5-2で得られたものに置き換える
6. DetectionResultContainerをファイルに書き出す

修正メモ
=============

GameEyeでのpytorch(SSD)とResNet34統合のため、以下の点を修正する必要がある。

1. pytorch(SSD)のimage_logには画像ファイルはあるのだが、DetectionResultContainerにある結果との関連がわからないので、DetectionResultContainerを拡張する必要がある。ラベル、スコア、画像ファイル名。あとは、image_logのディレクトリにDetectionResultContainerも置いておくと良いかも。

2. pytorch(SSD)は最終的なアウトプットとして、GameEyeに解析してほしいimage_logのディレクトリ名を出力する必要がある。

3. 現状のResNet34は人間が見る用途のため少し冗長な出力。GameEye統合のためにはシンプルで良いので、quietオプションを追加する。

4. ResNet34は複数入力して、１つのプロセスの中で複数処理したほうが効率が良さそう。ただ、pytorchがmulticpuに対応しているかよくわからないので、１つのプロセスのなかで処理をシーケンシャルにやる所を最初は考えたほうが良いか。

5. DetectionResultContainerなど至るところで共通で呼び出されるクラスなどが増えてきてので、共通レポジトリにするなどをして整理したい。
