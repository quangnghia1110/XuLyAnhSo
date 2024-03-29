import cv2
import time
import os
import utility.B10_RecognitionFinger.hand as htm
import streamlit as st

st.sidebar.markdown("Nhận Dạng Tay")

def get_fvalue(val):
    feature_dict = {"No": 1, "Yes": 2}
    for key, value in feature_dict.items():
        if val == key:
            return value

def get_value(val, my_dict):
    for key, value in my_dict.items():
        if val == key:
            return value

app_mode = st.sidebar.selectbox('Select Page', ['Finger Recognition'])
if app_mode == 'Finger Recognition':
    st.title("Finger Recognition")

    start_btn = st.button('START')
    if start_btn:
        cap = cv2.VideoCapture(0)

        FRAME_WINDOW = st.image([])

        FolderPath = "utility/B10_RecognitionFinger/Fingers"
        lst = os.listdir(FolderPath)

        lst_2 = []  # khai báo list chứa các mảng giá trị của các hình ảnh/
        for i in lst:
            image = cv2.imread(f"{FolderPath}/{i}")  # Fingers/1.jpg , Fingers/2.jpg ...
            lst_2.append(image)

        pTime = 0
        detector = htm.handDetector(detectionCon=1)
        # 0.75 độ chính xác 75%

        exit_btn = st.button('EXIT')
        fingerid = [4, 8, 12, 16, 20]
        while True:
            ret, frame = cap.read()
            frame = detector.findHands(frame)
            lmList = detector.findPosition(frame, draw=False)  # phát hiện vị trí

            if len(lmList) != 0:
                fingers = []

                # Thumb
                if lmList[fingerid[0]][1] < lmList[fingerid[0] - 1][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

                # Four fingers
                for id in range(1, 5):
                    if lmList[fingerid[id]][2] < lmList[fingerid[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                print(fingers)
                songontay = fingers.count(1)
                print(songontay)

                # chú ý mỗi bức ảnh sẽ đẩy về giá trị của 1 mảng có chiều rông, cao khác nhau
                # ví dụ ảnh 0.png : print(lst_2[0].shape) kết quả (126, 110, 3)
                # frame[0:126,0:110] = lst_2[0]
                # do các bức ảnh 0-5.png khác nhau các giá trị wisth, height nên phải get theo shape
                h, w, c = lst_2[songontay - 1].shape
                frame[0:h, 0:w] = lst_2[songontay - 1]  # nếu số ngón tay =0 thì lst_2[-1] đẩy về phần tử cuối cùng của list là ảnh 6

                # vẽ thêm hình chữ nhật hiện số ngón tay
                cv2.rectangle(frame, (0, 200), (150, 400), (0, 255, 0), -1)
                cv2.putText(frame, str(songontay), (30, 390), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 5)

            cTime = time.time()  # trả về số giây, tính từ 0:0:00 ngày 1/1/1970 theo giờ utc , gọi là(thời điểm bắt đầu thời gian)
            fps = 1 / (cTime - pTime)  # tính fps Frames per second - đây là chỉ số khung hình trên mỗi giây
            pTime = cTime
            # show fps lên màn hình, fps hiện đang là kiểu float , ktra print(type(fps))

            cv2.putText(frame, f"FPS: {int(fps)}", (150, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

            print(frame)
            FRAME_WINDOW.image(frame)
            if exit_btn:
                break
