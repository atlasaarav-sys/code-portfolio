# Arduino-01 — Motion-Tracking Pan-Tilt Camera Rig

**Level:** Beginner-Intermediate
**Platform:** Arduino Uno R3 (ATmega328P) + PC-side Python/OpenCV
**Source:** rebuilt from `files.zip` (`motion_tracker.py` +
`pan_tilt_controller.ino`), provided as-is and documented here.

A webcam-driven pan-tilt camera rig: a PC runs OpenCV background
subtraction to find the largest moving blob in the frame, computes a
proportional pan/tilt correction, and streams `P<angle> T<angle>` commands
over serial to an Arduino Uno, which drives two hobby servos to keep the
camera pointed at the motion.

**Naming note:** the provided code tracks *motion* (via
`cv2.createBackgroundSubtractorMOG2` + largest-contour selection), not
specifically faces — there's no face detector in the pipeline. It'll track
a hand, a pet, or a moving chair just as readily as a face. If you want it
to track faces specifically rather than any motion, swap
`find_largest_motion_blob()` for a Haar cascade or DNN face detector
(`cv2.CascadeClassifier("haarcascade_frontalface_default.xml")` is the
one-line-swap option) — noted here rather than silently changed, since I
didn't want to alter the logic you actually sent.

## 1. Schematic — component & connection list

| Ref | Part | Value/Part # | Notes |
|---|---|---|---|
| U1 | Arduino Uno R3 | ATmega328P | Runs `pan_tilt_controller.ino`, connected to the PC via USB (also used for serial commands from `motion_tracker.py`) |
| M1 | Pan servo | SG90 (light rig) or MG996R (heavier camera/bracket) | Signal -> D9, per the `.ino`'s `PAN_PIN` |
| M2 | Tilt servo | SG90 or MG996R | Signal -> D10, per the `.ino`'s `TILT_PIN` |
| PS1 | External 5V supply | 5V, 2A+ (barrel jack or bench supply) | Powers M1/M2 directly — **not** the Arduino 5V pin, exactly as called out in the `.ino`'s header comment, to avoid brownouts resetting the Uno when both servos move at once |
| J1 | Barrel jack or screw terminal | 5.5x2.1mm or 2-pin terminal | External supply input, feeds M1/M2 VCC |
| C1 | Bulk capacitor | 470-1000uF, 16V electrolytic | Across the servo power rail (PS1 output), close to M1/M2, to absorb the current spikes when servos start moving — not in the original files, added here as standard practice for driving two servos from an external supply |
| — | Common ground | — | Arduino GND, servo GND (both M1 and M2), and PS1 GND all tied together — required for the PWM signal reference to be valid even though power is separate |
| CAM1 | USB webcam | Any UVC-compatible webcam | Connects directly to the PC via USB, **not** to the Arduino — `motion_tracker.py` opens it with `cv2.VideoCapture(args.camera)` |
| — | Pan-tilt bracket kit | Generic 2-servo pan-tilt bracket (SG90 or MG996R mount pattern to match M1/M2) | Mounts CAM1 on the tilt axis, tilt axis mounts on the pan axis |

### Signal path

```
PC (motion_tracker.py) --USB serial--> Arduino Uno (pan_tilt_controller.ino) --PWM--> M1 (pan), M2 (tilt)
CAM1 --USB--> PC directly (video never passes through the Arduino)
```

## 2. PCB layout plan — optional servo breakout shield

The base build is just an Uno + jumper wires to the servos and a barrel
jack, which is genuinely fine for a one-off build. If you want a cleaner,
repeatable version, here's a small Arduino Uno shield that breaks out the
two servo headers and the external power input properly:

- **Board size/shape:** Standard Arduino Uno shield form factor (68.6mm x
  53.3mm), 2-layer, with the usual Uno header footprint (two rows along
  the long edges + the ICSP block) so it plugs directly onto the Uno.
- **Placement:** J1 (external power barrel jack/terminal) placed at a
  board edge for easy cable access. C1 (bulk cap) placed immediately next
  to J1's output, before the trace fans out to the two servo headers.
  Two 3-pin servo headers (signal/V+/GND, standard 0.1" pitch) placed near
  the edge closest to where the pan-tilt bracket sits relative to the Uno
  in the final assembly, silkscreened "PAN (D9)" and "TILT (D10)".
- **Routing notes:**
  - Servo power (from J1, through C1) routed as a wide trace (>=40mil) or
    small copper pour, since MG996R-class servos can draw >1A stall
    current per channel — this is the one part of an "Arduino shield" that
    actually needs power-trace sizing.
  - Servo GND tied to Arduino GND (through the shield's GND pin) at a
    single point, not looped, to avoid ground loops between the logic
    and power domains.
  - Signal traces (D9/D10 passthrough to the servo headers) are low
    current — standard 12-15mil is fine.
  - Keep the servo power plane physically separated from the Uno's own
    5V pin — the shield should only ever pass D9/D10 (signal) and GND
    through to the Uno, never route J1's 5V onto the Uno's 5V pin.
- **Layer stackup:** 2-layer, 1.6mm FR4, standard 1oz copper.

## 3. Bill of materials

| Qty | Ref | Part | Footprint | Example distributor P/N |
|---|---|---|---|---|
| 1 | U1 | Arduino Uno R3 | — | Digi-Key 1050-1024-ND |
| 2 | M1,M2 | SG90 micro servo (or MG996R for a heavier camera) | — | Digi-Key/Adafruit/SparkFun generic hobby servo |
| 1 | — | 2-axis pan-tilt bracket kit (servo mount pattern matching M1/M2) | — | Generic "pan tilt camera platform" kit (Amazon/AliExpress/SparkFun) |
| 1 | CAM1 | USB webcam (UVC-compatible) | — | Any UVC webcam |
| 1 | PS1 | 5V 2A+ wall adapter or bench supply | 5.5x2.1mm barrel | Digi-Key T1042-P5P-ND (adapter) |
| 1 | J1 | Barrel jack or 2-pin screw terminal | THT | Digi-Key CP-102A-ND (barrel jack) |
| 1 | C1 | 470-1000uF 16V electrolytic capacitor | THT radial | Digi-Key P5150-ND |
| — | — | Jumper wires / 3-pin servo extension leads | — | Generic |
| 1 (optional) | — | Servo breakout shield PCB (see Section 2) | Uno shield form factor | Custom fab (JLCPCB/PCBWay) |

## Code

- [code/motion_tracker.py](code/motion_tracker.py) — PC-side OpenCV motion
  detection + proportional pan/tilt controller, sends `P<pan> T<tilt>\n`
  over serial
- [code/pan_tilt_controller.ino](code/pan_tilt_controller.ino) — Arduino
  sketch: parses `P<pan> T<tilt>` serial commands, drives the two servos
  via the `Servo` library, echoes `OK P<pan> T<tilt>` back for
  logging/confirmation
- [code/requirements.txt](code/requirements.txt) — `opencv-python`,
  `pyserial`

### How to run

```bash
# 1. Flash pan_tilt_controller.ino onto the Arduino Uno via the Arduino IDE

# 2. On the PC:
pip install -r code/requirements.txt
python code/motion_tracker.py --port COM5       # Windows
python code/motion_tracker.py --port /dev/ttyACM0  # Linux/Mac
```

Press `q` in the preview window to quit. If the rig tracks backwards
(moves away from the subject instead of toward it), flip the sign on
`pan_angle -= error_x * args.gain` in `motion_tracker.py` — the comment in
the code already flags this as orientation-dependent on your specific
servo/bracket mounting.

## Notes

`pan_tilt_controller.ino` compiles clean against an Arduino Uno (5,894
bytes flash / 18%, 260 bytes RAM / 12%) — I actually built it with
`arduino-cli` rather than just eyeballing the code. The Python side isn't
run end-to-end here, though (no webcam/Arduino attached, and
`opencv-python`/`pyserial` aren't installed) — the Python and `.ino`
files are exactly what was provided, reviewed but not modified; the
capacitor (C1) and the shield PCB in Section 2 are additions on top of the
original two files, called out explicitly above rather than folded in
silently.
