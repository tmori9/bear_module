from ultralytics import YOLO
import numpy as np
import argparse
from torchvision.transforms import ToPILImage
from itertools import chain

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
        "-f",
        "--fps",
        default=2,
        type=int,
        help="This is fps of output video.",
    )
    parser.add_argument(
        "-i",
        "--input",
        default="trimBearImage/input_video",
        type=str,
        help="This is input video folder.",
    )

    return parser.parse_args()


def find_bbox(mask):
    """
    Finds the bounding box coordinates from a 2D mask.

    Parameters:
    - mask: 2D numpy array with True/False values.

    Returns:
    - tuple of (ymin, xmin, ymax, xmax)
    """
    # Trueのインデックスを取得
    rows, cols = np.where(mask)

    # bboxの座標を取得
    ymin, ymax = np.min(rows), np.max(rows)
    xmin, xmax = np.min(cols), np.max(cols)

    return (ymin, xmin, ymax, xmax)


def save_no_bg_image(file_name: str, path_num: int, results):
    """
    maskを用いて背景を除去した画像を保存する

    Parameters:
    - file_name: 入力する動画の名前 (拡張子なし)
    - path_num: 保存する画像の番号
    - results: YOLOの出力
    """
    save_path = Path(f"trimBearImage/output_image/{file_name}")
    save_path.mkdir(parents=True, exist_ok=True)
    for result in results:
        if result.masks:
            masks = result.masks.data.cpu()
            ori_img = result.orig_img[:, :, [2, 1, 0]]
            for j, mask in enumerate(masks):
                mask = mask.numpy()
                mask_resize = cv2.resize(mask, (ori_img.shape[1], ori_img.shape[0]))
                mask_bool = np.array(mask_resize, dtype=bool)

                # maskのbboxを取得
                y_min, x_min, y_max, x_max = find_bbox(mask_bool)

                new = np.zeros_like(ori_img, dtype=np.uint8)
                new[mask_bool] = ori_img[mask_bool]
                new = new[y_min : y_max + 1, x_min : x_max + 1]
                image = ToPILImage()(new)
                image.save(save_path / f"{path_num:04}_{j}.png")


def main():
    args = get_args()

    # Load a model
    model = YOLO(args.model)
    input_folder = Path(args.input)

    # 拡張子の指定
    movie_extensions = [".mp4", ".MP4", ".mov", ".MOV"]

    for file_name in input_folder.glob("*"):
        # 拡張子が動画の場合
        if file_name.suffix in movie_extensions:
            print(f"file name: {file_name}")
            cap = cv2.VideoCapture(str(file_name))
            movie_fps = cap.get(cv2.CAP_PROP_FPS)
            extract_frame = movie_fps // args.fps  # 何フレームに1回抽出するか
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if int(frame_idx % extract_frame) == 0:
                    path_num = int(frame_idx // movie_fps)

                    # class 21 = bear
                    results = model.predict(
                        frame,
                        save_crop=False,
                        classes=21,
                    )
                    save_no_bg_image(file_name.stem, path_num, results)
                frame_idx += 1


if __name__ == "__main__":
    main()
