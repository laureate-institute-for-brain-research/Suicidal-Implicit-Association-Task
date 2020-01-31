README for the Physiological Baseline task (flower slide show)

*****************************************************************SUMMARY**************************************************************************

This task presents a slideshow of different flowers. Each flower is displayed for 3s. Baseline physiological measures are collected while the subject views the slideshow.

*****************************************************************TRIAL STRUCTURE******************************************************************

      [         instructions         ] ->
      ^                              ^
INSTRUCT_ONSET                   TASK_ONSET

      3s
[image onset] ->
^
IMAGE_ONSET

*****************************************************************INPUT DETAILS********************************************************************

EACH LINE CODES: one trial
COLUMN 1: not used
COLUMN 2: image to show
COLUMN 3: duration of image display (always 3s here)
COLUMN 4: not used
TRIAL ORDER IS: fixed

*****************************************************************OUTPUT DETAILS*******************************************************************

INSTRUCT_ONSET (1)
response_time: not used
response: not used
result: not used

TASK_ONSET (2)
response_time: time between INSTRUCT_ONSET and TASK_ONSET
response: not used
result: not used

IMAGE_ONSET (3)
response time: not used
response: not used
result: the image shown



