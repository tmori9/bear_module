# bear_module

ヒグマ動画抽出プログラムと背景除去・画像切り取りプログラム

## モジュールの説明

### videoBearDetector

- ヒグマ動画からヒグマの画像を抽出するプログラム

`python videoBearDetector/videoBearDetector.py -i <input_folder> -o <output_folder>`
example: `python videoBearDetector/videoBearDetector.py -i videoBearDetector/input_video -o videoBearDetector/output_video`

### trimBearImage
- ヒグマの画像から背景を除去し、ヒグマのみの画像を切り取るプログラム
`python trimBearImage/trimBearImage.py -i <input_folder>`
example: `python trimBearImage/trimBearImage.py -i trimBearImage/input_video`

## インストール
- 想定OS: Windows

1. pyenv をインストールする

- 参考: [pyenvのWindowsへのインストール](https://zenn.dev/lot36z/articles/1c734bde03677c)

2. pyenv で python3.10.11 をインストールする

```bash
pyenv install 3.10.11
```

3. venv で仮想環境を作成する

```bash
python -m venv .venv
```

4. 仮想環境を有効化する
- cmd.exeの場合
```bash
.venv\Scripts\activate.bat
```
- PowerShellの場合
```bash
.venv\Scripts\Activate.ps1
```
