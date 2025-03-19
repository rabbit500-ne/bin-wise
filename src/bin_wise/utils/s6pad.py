from PIL import Image
import os

def split_image_with_overlap(image_path, output_dir, overlap_ratio=0.1):
    """ 画像を6つの正方形に分割して保存する

    Returns:
    --------
    sub_images : list
        6つの正方形画像
    """

    img = Image.open(image_path)
    width, height = img.size

    # 正方形の一辺の長さ（元画像の1/3を基本）
    square_size = height // 3
    
    # オーバーラップするピクセル数
    overlap = int(square_size * overlap_ratio)

    overlap_square_size = square_size + overlap

    # 各正方形の開始位置
    positions = [
        (0, 0),  # 1
        (width - overlap_square_size, 0),  # 2
        # 真ん中の正方形:
        (0, int(height / 2 - overlap_square_size / 2)),  # 3
        (width - overlap_square_size, int(height / 2 - overlap_square_size / 2)),  # 4
        (0, height - overlap_square_size),  # 5
        (width - overlap_square_size, height - overlap_square_size)  # 6
    ]

    # 子画像の作成
    sub_image_paths = []
    for i, (x, y) in enumerate(positions):
        cropped = img.crop((x, y, x + overlap_square_size, y + overlap_square_size))
        path = os.path.join(output_dir, f"sub_image_{i+1}.png")
        cropped.save(path)
        sub_image_paths.append(path)

    return sub_image_paths

if __name__ == "__main__":
    # 画像パスを指定して実行
    split_image_with_overlap("/home/rag451/BinWise/data/picture/wakekata-dashikata_1_1.png")