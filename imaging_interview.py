import cv2
import imutils
import os
import glob


def draw_color_mask(img, borders, color=(0, 0, 0)):
    h = img.shape[0]
    w = img.shape[1]

    x_min = int(borders[0] * w / 100)
    x_max = w - int(borders[2] * w / 100)
    y_min = int(borders[1] * h / 100)
    y_max = h - int(borders[3] * h / 100)

    img = cv2.rectangle(img, (0, 0), (x_min, h), color, -1)
    img = cv2.rectangle(img, (0, 0), (w, y_min), color, -1)
    img = cv2.rectangle(img, (x_max, 0), (w, h), color, -1)
    img = cv2.rectangle(img, (0, y_max), (w, h), color, -1)

    return img


def preprocess_image_change_detection(img, gaussian_blur_radius_list=None, black_mask=(5, 10, 5, 0)):
    gray = img.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    if gaussian_blur_radius_list is not None:
        for radius in gaussian_blur_radius_list:
            gray = cv2.GaussianBlur(gray, (radius, radius), 0)

    gray = draw_color_mask(gray, black_mask)


    return gray


def compare_frames_change_detection(prev_frame, next_frame, min_contour_area):
    frame_delta = cv2.absdiff(prev_frame, next_frame)
    thresh = cv2.threshold(frame_delta, 45, 255, cv2.THRESH_BINARY)[1]

    thresh = cv2.dilate(thresh, None, iterations=2)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    score = 0
    res_cnts = []
    for c in cnts:
        if cv2.contourArea(c) < min_contour_area:
            continue

        res_cnts.append(c)
        score += cv2.contourArea(c)

    return score, res_cnts, thresh


def search_img(directory):    # function to search for all images
    # to search for all files with .png extension
    search_pattern = os.path.join(directory, '*.png')

    # to get all image files
    img_files = glob.glob(search_pattern)

    return img_files

def main():
    path = input(r'Enter path to images folder: ')

    os.chdir(path)

    images = search_img(path)

    rem = 0
    del_img = []
    for i, img1 in enumerate(images):
        print(i)
        if 'c10' in img1:
            black_mask = [5,20,5,0]
        elif 'c20' in img1:
            black_mask = [5, 30, 5, 0]
        elif 'c21' in img1:
            black_mask = [0, 30, 0, 0]
        elif 'c23' in img1:
            black_mask = [0, 40, 0, 0]

        if img1 in del_img:
            continue

        try:
            prev_img = cv2.imread(img1)
            height1, width1, channels1 = prev_img.shape                                             # to remove images with very low resolution
            if height1 < 30 or width1 < 30:
                if img1 not in del_img:
                    rem += 1
                    del_img.append(img1)
                    continue
            prev_img = cv2.resize(prev_img, (480,480))
            prev_img = preprocess_image_change_detection(prev_img, [9, 11, 15, 17], black_mask)
        except:                                                                                     # if image is invalid, then remove
            if img1 not in del_img:
                del_img.append(img1)
                continue

        try:
            for img2 in images[i:]:
                if img2 not in del_img and img1 != img2:
                    if img1.split('\\')[-1][0:3] == img2.split('\\')[-1][0:3]:
                        next_img = cv2.imread(img2)
                        next_img = cv2.resize(next_img, (480,480))
                        next_img = preprocess_image_change_detection(next_img,[9,11,15,17],black_mask)
                        score, res_cnts, thresh = compare_frames_change_detection(prev_img, next_img, 100)
                        if score <= 3000:                                                           # remove images if score <= 3000
                            rem+=1
                            if img2 not in del_img:
                                del_img.append(img2)
                    else:
                        break
        except:
            if img2 not in del_img:
                rem += 1
                del_img.append(img2)

    for im in del_img:
        os.remove(im)


    print('removed - ',rem)

if __name__ == "__main__":
    main()

