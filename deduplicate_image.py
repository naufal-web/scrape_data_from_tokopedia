from os.path import join
from os import listdir
from os import getcwd
import cv2


def get_histogram_image_data(image):
    image_data = cv2.imread(image)
    try:
        histo_image_data = cv2.calcHist([image_data], [0, 1, 2], None, [256, 256, 256],
                                        [0, 256, 0, 256, 0, 256])
        histo_image_data[255, 255, 255] = 0
        cv2.normalize(histo_image_data, histo_image_data, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX)
        return histo_image_data
    except cv2.error:
        return None


def get_similarity_score(histo_images):
    image1, image2 = histo_images
    try:
        return cv2.compareHist(image1, image2, cv2.HISTCMP_CORREL)
    except cv2.error:
        return 0.0


def deduplicate_images_from_directory(images_dir="images"):
    images = [join(getcwd(), images_dir, image) for image in listdir(join(getcwd(), images_dir))]

    images_set = set()

    for i in range(len(images)):
        for j in range(1, len(images)):
            for k in range(2, len(images) + 1):
                if len(images[i:j:k]) == 2:
                    image_path_1, image_path_2 = images[i:j:k]
                    histogram_images = get_histogram_image_data(image_path_1), get_histogram_image_data(image_path_2)
                    score = get_similarity_score(histogram_images)
                    if score == 1.0:
                        images_set.add(image_path_1)

    return images_set


# print(len(deduplicate_images_from_directory()))
