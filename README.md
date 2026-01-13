# Project Gameface
Project Gameface helps gamers control their mouse cursor using head movement and facial gestures.

## Platforms
- Windows (see guide below)

## Windows guide
### Download
1. Download the program from the [Release section](https://github.com/Jefrry/project-gameface/releases).
2. Run `run_app.exe`.

### Python application
**Environment**
- Windows  
- Python 3.9

Install dependencies:
```
pip install -r requirements.txt
```

**Quick start**
1. Run the main application:
    ```
    python run_app.py
    ```

### Configs
#### Basic config
`configs/default/cursor.json`

|                        |                                                    |
|------------------------|----------------------------------------------------|
| camera_id              | Default camera index on your machine.             |
| tracking_vert_idxs     | Tracking points for controlling cursor ([see](assets/images/uv_unwrap_full.png)) |
| spd_up                 | Cursor speed in the upward direction.             |
| spd_down               | Cursor speed in downward direction.               |
| spd_left               | Cursor speed in left direction.                   |
| spd_right              | Cursor speed in right direction.                  |
| pointer_smooth         | Amount of cursor smoothness.                      |
| shape_smooth           | Reduces action flicker.                           |
| hold_trigger_ms        | Hold action trigger delay in milliseconds.        |
| auto_play              | Automatically begin playing on launch.            |
| mouse_acceleration     | Increase cursor speed when the head moves quickly.|
| use_transformation_matrix | Control cursor using head direction (ignores tracking_vert_idxs). |

#### Keybind configs
`configs/default/mouse_bindings.json`  
`configs/default/keyboard_bindings.json`

Keybinding entry structure:
```
gesture_name: [device_name, action_name, threshold, trigger_type]
```

|              |                                                                                           |
|--------------|-------------------------------------------------------------------------------------------|
| gesture_name | Face expression name (see `src/shape_list.py`).                                           |
| device_name  | "mouse" or "keyboard".                                                                    |
| action_name  | For mouse: "left", "right", "middle". For keyboard: key value (e.g., "w").                |
| threshold    | Trigger threshold from 0.0 to 1.0.                                                        |
| trigger_type | "single" for a single trigger, "hold" for ongoing action.                                 |

### Build
```
pyinstaller build.spec
```

## Model used
MediaPipe Face Landmark Detection API [Task Guide](https://developers.google.com/mediapipe/solutions/vision/face_landmarker)  
[MediaPipe BlazeFace Model Card](https://storage.googleapis.com/mediapipe-assets/MediaPipe%20BlazeFace%20Model%20Card%20(Short%20Range).pdf)  
[MediaPipe FaceMesh Model Card](https://storage.googleapis.com/mediapipe-assets/Model%20Card%20MediaPipe%20Face%20Mesh%20V2.pdf)  
[Mediapipe Blendshape V2 Model Card](https://storage.googleapis.com/mediapipe-assets/Model%20Card%20Blendshape%20V2.pdf)  

## Application
- Control mouse cursor in games.
- Intended users are people who choose to use face-control and head movement for gaming purposes.

## Out-of-scope applications
- Not intended for human life-critical decisions. 
- Predicted face landmarks do not provide facial recognition or identification and do not store any unique face representation.