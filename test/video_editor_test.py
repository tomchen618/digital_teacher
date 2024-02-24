from lecture.common.video_editor import VideoEditor


def run_video_editor_test():
    video_editor = VideoEditor(lecture_id="id_test", lecture_name="The Call of the Wild author Jack London",
                               file_path="pdf_testing.mp4",
                               explanations=[], voice_file="liuin-8.mp4",
                               lecture_output="liuin-out-8.mp4")
    video_editor.merge_videos(output_path="")
