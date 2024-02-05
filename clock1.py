import cv2
import numpy as np
from datetime import datetime

# 画像の読み込み
image = cv2.imread('時計4.JPG')

# グレースケール変換
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#白黒2値化
ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY)

# 画像のぼかし処理（ノイズ低減）
blurred = cv2.GaussianBlur(thresh, (5, 5), 0)

# エッジ検出
edges = cv2.Canny(blurred, 50, 150)

# 輪郭検出
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 面積の大きい順にソート
contours = sorted(contours, key=cv2.contourArea, reverse=True)


# アナログ時計の針を取得
clock_hand_contour = None
for contour in contours:
    epsilon = 0.02 * cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, epsilon, True)

    if len(approx) == 5:
        clock_hand_contour = approx
        break
    
# アナログ時計の針の角度を計算
if clock_hand_contour is not None:
    rect = cv2.minAreaRect(clock_hand_contour)
    angle = rect[2]
    if angle < -45:
        angle = 90 + angle

    # アナログ時計の針の角度から概算時間を計算
    hour = int((angle + 90) % 360 / 30)
    minute = int((angle + 90) % 360 % 30 / 0.5) 

    # 現在の時間帯を表示
    current_time = datetime.now()
    current_time = current_time.replace(hour=hour, minute=minute, second=0, microsecond=0)
    print('現在の時間帯:', current_time.strftime('%H:%M'))

else:
    print('検出できませんでした。')
    

# 結果の表示
cv2.imshow('Analog Clock Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()