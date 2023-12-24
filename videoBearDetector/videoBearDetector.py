import argparse
from ultralytics import YOLO

from pathlib import Path
import cv2


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--model",
        default="yolov8x-seg",
        type=str,
        help="This is segmentation model name. ex: yolov8x-seg",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="videoBearDetector/input_video",
        type=str,
        help="This is input video folder.",
    )

    return parser.parse_args()


def main():
    args = get_args()

    # Load a model
    model = YOLO(args.model)
    input_folder = Path(args.input)
    print(f"input folder name: {input_folder}")

    # 拡張子の指定
    movie_extensions = [".mp4", ".MP4", ".mov", ".MOV"]

    # 出力フォルダの作成
    output_bear_folder = Path("videoBearDetector/output_video/bear")
    output_bear_folder.mkdir(parents=True, exist_ok=True)
    output_no_bear_folder = Path("videoBearDetector/output_video/no_bear")
    output_no_bear_folder.mkdir(parents=True, exist_ok=True)

    for file_name in input_folder.glob("*"):
        # 拡張子が動画の場合
        if file_name.suffix in movie_extensions:
            print(f"file name: {file_name}")
            cap = cv2.VideoCapture(str(file_name))
            movie_fps = cap.get(cv2.CAP_PROP_FPS)
            extract_frame = movie_fps  # 1fps = 5フレームに1回抽出
            frame_idx = 0
            bear_detected = False
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if int(frame_idx % extract_frame) == 0:
                    results = model.predict(frame)  # 21 = bear
                    for r in results:
                        # print(r.boxes.cls.tolist())
                        if 21 in r.boxes.cls.tolist():
                            bear_detected = True
                if bear_detected:
                    print(f"bear detected in {file_name}")
                    cap.release()

                    # クマの動画を移動
                    file_name.rename(output_bear_folder / file_name.name)
                    break
                frame_idx += 1

            cap.release()
            # クマが検出されなかった場合
            if not bear_detected:
                file_name.rename(output_no_bear_folder / file_name.name)
        else:
            print(f"{file_name} is not movie file.")
            continue


if __name__ == "__main__":
    main()
