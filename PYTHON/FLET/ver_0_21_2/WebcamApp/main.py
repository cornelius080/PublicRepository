import flet as ft
import cv2
import base64
import time
import threading
import os


class WebcamManager(ft.UserControl):
    def __init__(self, frameSize=(640,480)):        
        """
        Initializes the WebcamManager class with default or specified frame size.

        Parameters:
        frameSize (tuple): The desired frame size for the webcam capture, default is (640, 480).

        Attributes:
        isolated (bool): Flag indicating isolation state.
        frame (None or numpy.ndarray): Stores the current frame from the webcam.
        isRecording (bool): Flag indicating if the webcam is currently recording.
        webcam (cv2.VideoCapture or None): Video capture object for the webcam.
        video_writer (cv2.VideoWriter or None): Video writer object for saving video.
        frame_size (tuple): Stores the frame size for the webcam capture.
        output_path (str or None): Directory path where captured media is saved.

        Initializes the webcam with specified frame size using DirectShow API. If the webcam
        cannot be opened, the program will exit. Sets up the output directory for saving
        captured images and videos. If any exception occurs during initialization, 
        it prints the error message.
        """
        super().__init__()
        self.isolated = True
        self.frame = None
        self.isRecording = False
        self.webcam = None
        self.video_writer = None
        self.frame_size = frameSize
        self.output_path = None
        try:
            self.webcam = cv2.VideoCapture(index=0, apiPreference=cv2.CAP_DSHOW)
            if not self.webcam.isOpened():
                print("Cannot open camera")
                exit()
            else:    
                # Set new capture properties
                ret = self.webcam.set(cv2.CAP_PROP_FRAME_WIDTH, value=float(self.frame_size[0]))
                ret = self.webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, value=float(self.frame_size[1])) 

                print("webcam.isOpened(): ", self.webcam.isOpened())

                local_path = os.getcwd()
                self.output_path = local_path + "\\webcam_output\\"
                if not os.path.exists(self.output_path):
                    os.makedirs(self.output_path)

        except Exception as e:
            print(e)
        
    def capture_from_webcam(self):        
        """
        Captures frames from the webcam and updates the UI image.

        Uses the :py:class:`cv2.VideoCapture` object to read frames from the webcam.
        If the frame is read successfully, it checks if the recording is turned on.
        If it is, it writes the frame to the video writer object using
        :py:meth:`cv2.VideoWriter.write` method. Then, it encodes the frame to
        a PNG image and converts it to a base64 string. Finally, it updates
        the UI image by setting its :py:attr:`src_base64` attribute to the
        base64 string.

        :return: None
        """
        while self.webcam.isOpened():
            ret, self.frame = self.webcam.read()
            if ret:
                #self.frame = cv2.resize(self.frame,(854,480))
                if self.isRecording:
                    self.video_writer.write(self.frame)                    
                _, img_arr = cv2.imencode('.png', self.frame)
                img_b64 = base64.b64encode(img_arr)
                self.img.src_base64 = img_b64.decode("utf-8")
                self.update()

    def save_image(self):                
        """
        Saves the current frame as an image file in the PROJECT DIRECTORY.

        The filename of the saved image is the current date and time in the format
        "YYYY_MM_DD_HH_MM_SS_image.png".

        :return: A string message indicating the status of the saving operation.
        """
        msg = "Picture Not Saved !"
        filename = time.strftime("%Y_%m_%d___%H_%M_%S_", time.localtime()) + "image.png"
        
        ret = cv2.imwrite(self.output_path + filename, self.frame)
        if ret: 
            msg = filename + " saved in the PROJECT DIRECTORY"
        return msg
    
    def save_video(self, frame_per_sec:float = 20.0):        
        """
        Saves the current frame as a video file in the PROJECT DIRECTORY.

        The filename of the saved video is the current date and time in the format
        "YYYY_MM_DD_HH_MM_SS_video.mp4".

        Parameters
        ----------
        frame_per_sec : float, optional
            The frame rate of the saved video. Defaults to 20.0.

        Returns
        -------
        None
        """
        filename = time.strftime("%Y_%m_%d___%H_%M_%S_", time.localtime()) + "video.mp4"

        self.video_writer = cv2.VideoWriter(self.output_path + filename,
                                      fourcc=cv2.VideoWriter_fourcc(*'mp4v'), fps=frame_per_sec, 
                                      frameSize=self.frame_size)
        
        print("video_writer.isOpened(): ", self.video_writer.isOpened())
        
        
    def build(self):        
        """
        Builds the UI of this control by creating an ft.Image object with
        its border radius set to 20. The method is called when the control is being created and assigned its self.page.
        
        :return: The ft.Image object that represents the UI of this control.
        """
        self.img = ft.Image(
            border_radius=ft.border_radius.all(20)
        )
        return self.img
    
    def did_mount(self):        
        """
        Starts capturing frames from the webcam when the control is added to the page.
        
        This method is called after the control is added to the page and assigned transient uid.
        It starts the :py:meth:`capture_from_webcam` method which will capture frames from the
        webcam and update the UI image. This allows the user to see the camera feed in the UI.
        
        :return: None
        """
        self.capture_from_webcam()
    
    def will_unmount(self):        
        """
        Releases the video writer and webcam resources when the control is removed from the page.
        
        This method is called before the control is removed from the page and unassigned transient uid.
        It releases the video writer and webcam resources using the :py:meth:`cv2.VideoWriter.release` and
        :py:meth:`cv2.VideoCapture.release` methods, respectively. This is necessary to free up the
        resources and prevent memory leaks.
        
        :return: None
        """
        self.video_writer.release()
        self.webcam.release()
        

def main(page: ft.Page):   
    """
    The main function for this Flet application.

    This function contains all the UI elements and their respective event handlers.
    It also sets up the window's properties such as title, size, and prevent close.
    When the window is closed, it will open the bottom sheet to ask the user if they really want to close the app.
    If the user clicks "Yes", the window will be destroyed.
    If the user clicks "No", the bottom sheet will be closed and the window will stay open.

    Parameters
    ----------
    page : ft.Page
        The page object for this Flet application.

    Returns
    -------
    None
    """
    
    def close_bottom_sheet(e):        
        """
        Closes the bottom sheet when the user clicks on the "No" button.

        This function is called when the user clicks on the "No" button in the bottom sheet.
        It will close the bottom sheet and update the page.

        Parameters
        ----------
        e : Event
            The event object that is sent by Flet when the "No" button is clicked.

        Returns
        -------
        None
        """
        page.close_bottom_sheet()
        page.update()

    def on_window_closing(e):        
        """
        Handles the window closing event.

        This function is called when the window is closed or the user clicks on the close button.
        If the event data is "close", it will open the bottom sheet to ask the user if they really want to close the app.
        If the user clicks "Yes", the window will be destroyed.
        If the user clicks "No", the bottom sheet will be closed and the window will stay open.

        Parameters
        ----------
        e : Event
            The event object that is sent by Flet when the window is closed or the user clicks on the close button.

        Returns
        -------
        None
        """
        if e.data == "close":
            page.bottom_sheet.open = True
            page.update()

    def recording_blinking():        
        """
        This function blinks the text "REC" when the user is recording a video.

        The function will keep running in a separate thread and will stop when the user stops recording.

        The blinking is done by setting the "visible" property of the "recording_text" Text control to True and False every second.

        The function will wait for 1 second between each blink using the "wait" method of the "threading.Event" class.

        If the user stops recording, the "isRecording" variable will be set to False and the function will stop running.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        while True:
            recording_text.visible = not recording_text.visible 
            page.update() 
            threading.Event().wait(1) #blinking every 1 sec
            global isRecording
            if not isRecording:
                break
   
    def button_photo_clicked(e):        
        """
        This function is called when the user clicks on the "PHOTO" button.

        It takes a picture using the currently selected camera and saves it to the file system.

        It shows a SnackBar with a message indicating the status of the saving operation.

        Parameters
        ----------
        e : event object
            The event object that is sent by Flet when the user clicks on the button.

        Returns
        -------
        None
        """
        msg = camManager.save_image() 
        page.snack_bar = ft.SnackBar(ft.Text(msg))
        page.snack_bar.open = True
        page.update()

    def button_video_clicked(e):        
        """
        This function is called when the user clicks on the "VIDEO" button.

        If the user is currently recording a video, it will stop recording and save the video to the file system.
        If the user is not currently recording a video, it will start recording a video.

        It shows a SnackBar with a message indicating the status of the recording or saving operation.

        Parameters
        ----------
        e : event object
            The event object that is sent by Flet when the user clicks on the button.

        Returns
        -------
        None
        """

        global isRecording
        
        if isRecording: # recording -> not recording
            isRecording = False
            recording_text.value = ""
            page.snack_bar = ft.SnackBar(ft.Text("New video saved in the PROJECT DIRECTORY!"))
            page.snack_bar.open = True               
            button_photo.visible = True
        else: # not recording -> recording
            isRecording = True
            recording_text.value = "REC"
            button_photo.visible = False
            camManager.save_video()     
            #threading.Thread(target=recording_blinking()).start()       

        camManager.isRecording = isRecording
        page.update()
        

    global isRecording
    isRecording = False
    camManager = WebcamManager(frameSize=(1280,720))  

    webcamContainer = ft.Container(width=854, height=480, content = camManager, 
                                   padding=20, alignment=ft.alignment.center,
                                   #border=ft.border.all(1, ft.colors.RED), 
    )
    cardTop = ft.Card(content=webcamContainer, elevation=100)

    button_photo = ft.IconButton(icon=ft.icons.PHOTO_CAMERA, icon_size=46, 
                                on_click = button_photo_clicked, tooltip="Take a picture",
    )
    button_video = ft.IconButton(icon=ft.icons.VIDEO_CAMERA_FRONT, icon_size=46, 
                                on_click = button_video_clicked, tooltip="Record a video",
    )

    cardBottom = ft.Card(width=200, elevation=200, 
                         content=ft.Row([button_photo, button_video], alignment=ft.MainAxisAlignment.SPACE_AROUND),     
    )

    recording_text = ft.Text(theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM, color=ft.colors.RED)


    bs = ft.BottomSheet(
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text("Are you sure you want to close the app?"),
                    ft.Row(
                            controls=[
                                ft.ElevatedButton("No", on_click=close_bottom_sheet),
                                ft.ElevatedButton("Yes", on_click=lambda _: page.window_destroy()),
                            ], 
                            alignment = "center"
                    ),                   
                    
                ],
            ),
        ),
    )
    page.bottom_sheet = bs

    page.window_maximized = True
    page.scroll = ft.ScrollMode.AUTO
    page.window_prevent_close = True
    page.on_window_event = lambda e: on_window_closing(e)    
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.title = "Webcam Recorder"

    page.add(ft.Column(
        controls=[cardTop, cardBottom, recording_text], 
        horizontal_alignment = "center", 
        alignment = "center", )    
    )    

ft.app(target=main, assets_dir="assets")
