# bear_module

Bear video extraction and background removal

## モジュールの説明

### videoBearDetector

- 動画が入ったフォルダからヒグマの動画を抽出するプログラム
- <output_folder>/bear と <output_folder>/not_bear にそれぞれヒグマの動画とヒグマでない動画が保存される

```bash
python videoBearDetector/videoBearDetector.py -i <input_folder> -o <output_folder>

# example
python videoBearDetector/videoBearDetector.py -i videoBearDetector/input_video -o videoBearDetector/output_video
```

### trimBearImage
- 動画が入ったフォルダから背景を除去したヒグマの画像を切り取るプログラム
- <output_folder>/<動画の名前> にヒグマの画像が保存される

```bash
python trimBearImage/trimBearImage.py -i <input_folder> -o <output_folder>

# example
python trimBearImage/trimBearImage.py -i trimBearImage/input_video -o trimBearImage/output_image

# example: fpsを指定する場合
python trimBearImage/trimBearImage.py -i trimBearImage/input_video -o trimBearImage/output_image -f 5

# exapmle: フォルダを作成しない場合
python trimBearImage/trimBearImage.py -i trimBearImage/input_video
```

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
