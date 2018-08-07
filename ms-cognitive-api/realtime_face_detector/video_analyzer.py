from __future__ import print_function
import cv2
import time
import os
import _thread
import util
import cognitive_face as CF


class WebCamAnalyzer:

    def __init__(self):
        self.started = False
        self.temp_file_name = r'temp_'
        self.temp_file_ext = r'.jpg'
        self.enable_face_id = ''
        self.cap = ''
        self.webcam_frame = "Original View"
        self.analyze_frame = "Analyze View"
        self.person_group_id = 'latrobe_cdac_team'

    def start_capture(self, frame_rate, emotion_api_key, enable_face_id):
        self.enable_face_id = enable_face_id
        CF.Key.set(emotion_api_key)

        # Base URL for calling the Cognitive Face API.
        BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'
        CF.BaseUrl.set(BASE_URL)

        self.cap = cv2.VideoCapture(0)

        cv2.namedWindow(self.webcam_frame, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.webcam_frame, 800, 800)
        cv2.namedWindow(self.analyze_frame, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.analyze_frame, 800, 800)
        # cv2.resizeWindow(self.analyze_frame, 1960, 1200)

        iteration = 1
        while True:
            ret, frame = self.cap.read()
            cv2.imshow(self.webcam_frame, frame)

            if iteration % frame_rate == 0:
                self._process_frame(frame, cv2, iteration)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            iteration += 1

        self.cap.release()
        cv2.destroyAllWindows()

    def _render_result_on_image(self, result, img):

        def get_emotion_as_text(emotion_dict):
            result = ''
            for emo_name, emo_score in emotion_dict.items():
                if emo_score > 0.1:
                    result += emo_name + ':' + str(round(emo_score, 1)) + ' '
            return result

        fontScale = 0.5
        fontThickness = 2
        font_colour = (255, 153, 0)  # (0, 255, 0)

        for _, person in result.items():

            desc = person['personName'] + ", " + person['faceAttributes']['gender'] + ", " + str(person['faceAttributes']['age'])
            left = person['faceRectangle']['left']
            top = person['faceRectangle']['top']
            height = person['faceRectangle']['height']
            width = person['faceRectangle']['width']

            cv2.rectangle(img, (left, top), (left + width, top + height), (255, 0, 0), 1)
            cv2.putText(img, desc, (left, top), cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour,
                        fontThickness)
            cv2.putText(img, get_emotion_as_text(person['faceAttributes']['emotion']), (left, top + height),
                        cv2.FONT_HERSHEY_SIMPLEX, fontScale, font_colour, fontThickness)

        return img

    def _connect_ms_face_api_async(self, filename_temp, is_detect):

        def send_request(filename_temp, is_detect):

            res = CF.face.detect(filename_temp, attributes='age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories')

            face_dict = {}
            for idx, face_detail in enumerate(res):
                face_dict[face_detail['faceId']] = {
                    'faceAttributes': face_detail['faceAttributes'],
                    'faceId': face_detail['faceId'],
                    'faceRectangle': face_detail['faceRectangle'],
                    'personId': 0,
                    'personName': 'Unknown',
                    'confidence': 1.0,
                }

            if is_detect:

                for key, face in face_dict.items():

                    # For each face identify the person candidates
                    identified_persons = CF.face.identify([face['faceId']], self.person_group_id)
                    if len(identified_persons) > 0:
                        candidate_person_id = identified_persons[0]['candidates'][0]['personId']
                        candidate_person_confidence = round(identified_persons[0]['candidates'][0]['confidence'], 2)

                        person_name = CF.person.get(self.person_group_id, candidate_person_id)
                        face_dict[key]['personId'] = candidate_person_id
                        face_dict[key]['confidence'] = candidate_person_confidence
                        face_dict[key]['personName'] = person_name['name']

            img = cv2.imread(filename_temp)

            img = self._render_result_on_image(face_dict, img)
            cv2.imshow(self.analyze_frame, img)

            if os.path.exists(filename_temp):
                os.remove(filename_temp)

        # send_request(filename_temp, is_emotion)
        _thread.start_new_thread(send_request, (filename_temp, is_detect))

    def _process_frame(self, frame, cv2, iteration):

        filename_temp = self.temp_file_name + str(iteration) + self.temp_file_ext
        cv2.imwrite(filename_temp, frame)

        self._connect_ms_face_api_async(filename_temp, True)


def getAnalyzer():
    return WebCamAnalyzer()