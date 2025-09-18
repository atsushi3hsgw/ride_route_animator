# Ride Route Animator

Generate high-resolution animated videos from cycling FIT files, including route maps, elevation profiles, and dynamic ride statistics.  
This tool is designed for customization, extensibility, and beautiful visual storytelling.

## Features

- Parses FIT files and extracts GPS, elevation, speed, heart rate, and cadence  
- Renders route map with background tiles (OpenStreetMap, CartoDB, etc.)  
- Displays elevation profile and dynamic overlay statistics  
- Supports background image, video title, and flexible frame range/step  
- Outputs MP4 or WebM video using FFmpeg

## Sample Animation
<img src="images/sample_ride.gif" width="600">

## Requirements

### Python packages

Install required packages using pip:

    pip install fitparse matplotlib geopandas contextily pyproj shapely scipy pillow

Note: You may need additional system packages for `geopandas` and `pyproj` (e.g., `gdal`, `fiona`, `libspatialindex`).

### FFmpeg

FFmpeg is required to encode video output.

- macOS: `brew install ffmpeg`  
- Ubuntu/Debian: `sudo apt install ffmpeg`  
- Windows: [Download from ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH

## Usage

    python ride_route_animator.py -i activity.fit -o ride.mp4

### Options

| Option                     | Description |
|----------------------------|-------------|
| `-i`, `--input`            | Input FIT file (default: input.fit) |
| `-o`, `--output`           | Output video file (MP4 or WebM, default: output.mp4) |
| `--dpi`                    | Output resolution (default: 100) |
| `--zoom`                   | Tile zoom level (default: 13) |
| `--fps`                    | Frames per second (default: 10) |
| `--tile`                   | Tile provider (e.g. `OpenStreetMap.Mapnik`) |
| `--tilelist`               | List available tile providers and exit |
| `--title`                  | Title to embed in the video |
| `--no-elevation-smoothing`| Disable elevation smoothing |
| `--overlay-style`          | Position of overlay text (`top-left`, `top-right`, `bottom-left`, `bottom-right`) |
| `--start-frame`            | Start frame index (default: 0) |
| `--end-frame`              | End frame index (default: 0 = full length) |
| `--step-frame`             | Frame step interval (default: 10) |

### Example

    python ride_route_animator.py \
      -i activity.fit \
      -o ride.mp4 \
      --title "Morning Ride in Kanagawa" \
      --tile CartoDB.DarkMatter \
      --bg background.png \
      --start-frame 100 \
      --end-frame 800 \
      --step-frame 5 \
      --overlay-style bottom-right

## Notes

- Some tile providers may require authentication or block external access (e.g. Strava)  
- WebM output using VP9 codec may be slower than MP4 (h264)  
- Background image is applied to the entire figure, not just the map  
- Frame range and step allow partial or accelerated animations

## License

MIT License (or specify your preferred license)

## Author

Created by atsushi hasegawa  
Feel free to fork, extend, or contribute!