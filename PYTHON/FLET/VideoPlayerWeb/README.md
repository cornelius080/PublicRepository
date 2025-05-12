# A Web-Video Player Flet app

A simple web-video player developed with Flet. The app allows to add one or more web URL corresponding to web video (such as Youtube videos) and, optionally, to assign a name to them. Once the playlist is completed, a video player is shown and the videos are shown according to some basic settings.

![Screenshot of the app](assets\App_Screenshot.png)

## Add new video

In the top-right part of the UI, user can add a new video to the playlist by clicking on the "Plus" icon button. Once the button is pressed a new window dialog is opened. In this window, user can specify the web video url and, optionally, its video name in order to add this new item to the playlist. After a new video is added, it can be also selected for playlist playing or deleted / discarded.

## Video selection

In the top-right part of the UI, user can select all video previously added by clicking on the "Select All" button. If at least one video has been selected, the button "PLAY SELECTED VIDEO" gives access to the video player.

## Player

Section in which the video is played. Video player is based on [Flet Video control](https://flet.dev/docs/controls/video/). With the following version of the Flet framework (flet==0.21.2, flet-core==0.21.2, flet-runtime==0.21.2), some properties and events of the [Flet Video control](https://flet.dev/docs/controls/video/) appear unavailable: **title**, **on_completed()** and **on_track_changed()**.
With the lack of this properties and methods, the visualization of the current video title or URL has not be implemented neither inside the _video player container_ nor outside in other controls such as _TextFields_.

## Settings

Basic settings are adopted by default: high video filter quality and video aspect ratio of 16/9.

##### To run the app:

```
flet run [app_directory]
flet run --web [app_directory]
```