import os
from spleeter.separator import Separator
from config import OUTPUT_DIR

def audio_seperator(input_audio_path, output_dir = OUTPUT_DIR):
    file_list = list()
    try:
        separator = Separator('splits:stems')
        separator.separate_to_file(input_audio_path, output_dir)
        print(f"Separation complete. Check the output files in {output_dir}")
        files = os.listdir(output_dir)
        for file in files:
            file_list.append(file)
        print(f"files : {file_list}")
        return f"files : {file_list}"
    except Exception as error:
        print(f"Error : {error}")
        return f"Error : {error}"

