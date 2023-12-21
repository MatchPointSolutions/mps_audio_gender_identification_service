import gradio as gr
from pathlib import Path
from acoust_id import get_acoust_id_audio_details

def gradio_audio_file_analysis(input_file):
    try:
        temp_file_path = Path(input_file)
        result = get_acoust_id_audio_details(input_file)
        jsondata = {"filename": temp_file_path.name,
                    "result": result}
        title = jsondata["result"]["results"][0]["recordings"][2].get("title","")
        artist = jsondata["result"]["results"][0]["recordings"][2].get("artists","")
        filename  = temp_file_path.name
        body = f"""
            Thank you for using Matchpoint Audio Analyzer service. Our System has analyzed the audio file and Below are the analysis details.
                Human Voices:
                No. of Male voices :
                No. of femal Voices :
                Music Title : {title}
                Music Artist : {artist}
                Filename : {filename}
            Note: Matchpoint human Voice identification service works with 80% accuracy.
        """
        try:
            send_email(SUBJECT, body,str(receiver_email), SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD)
            print(f"Email Notification sent to {receiver_email}")
        except:
            print("Email Notification not sent")
        return body
    except Exception as error:
        print(f"Error: {error}")
        return "Unable to Process the audio file"

iface = gr.Interface(fn= audio_file_analysis, inputs = "file", outputs = "text")
iface.launch()
