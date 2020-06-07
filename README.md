[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![HitCount](http://hits.dwyl.io/nulLeeKH/archery-recorder.svg)](http://hits.dwyl.io/nulLeeKH/archery-recorder)
![GitHub last commit](https://img.shields.io/github/last-commit/nulLeeKH/archery-recorder.svg)

# archery-recorder
The video monitoring and recording program for archer

## How to Use
- space | R
    - Start/Stop recording
- ESC | E
    - End program
- up | U
    - Increase monitoring delay time
- down | D
    - Decrease monitoring delay time
- left | L
    - Decrease recording resolution
- right | H
    - Increase recording resolution
- 0~9
    - Change camera device

## Other Tools
Check other tools in [robin-hood-project](https://github.com/nulLeeKH/robin-hood-project)!

## Patch Note

### v1.0.0-alpha
- Initial release

### v1.0.1-alpha
- Add exception handler while threading.

### v1.0.2-alpha
- Add delay adjust feature.
- Add rotate code as comment for device.
- Add resolution adjust code as comment and set default as SD.

### v1.0.3-alpha
- Change video file naming convention.
- Remove pointless threading for performance.
- Fix exception printing feature.

### v1.0.4-alpha
- Apply mirror mode while monitoring.
- Modify information monitoring texts.

### v1.0.5-alpha
- Add resolution and camera adjust feature.
- Modify texts in screen.