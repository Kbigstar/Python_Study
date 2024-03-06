import easyocr
import cv2
reader = easyocr.Reader(['en', 'ko'], gpu=False)
def draw_bbox(path, data):
    img = cv2.imread(path)
    for d in data:
        bbox = d['bbox']
        st_point = (int(bbox[0][0]), int(bbox[0][1])) # 왼쪽 상단 좌표 생성
        en_point = (int(bbox[2][0]), int(bbox[2][1])) # 오른쪽 하단 좌표 생성
        # 사각형 그리기
        color = (0, 255, 0)
        img = cv2.rectangle(img, st_point, en_point, color, 2)
    cv2.imwrite('output.jpg', img)
def fn_get_text(path):
    img = cv2.imread(path)
    result = reader.readtext(img)
    dataset = []
    for bbox, text, prob in result:
        if prob > 0.1:
            dataset.append({'text':text, 'bbox':bbox, 'prob':prob})
    draw_bbox(path, dataset)
if __name__ == '__main__':
    fn_get_text('./img/car2.jpg')
