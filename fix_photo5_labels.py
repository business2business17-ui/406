#!/usr/bin/env python3
"""Swap the swapped 'front'/'back' captions on Photo 5 of the Pro series (406516...).
In the source images the view with the print is captioned 'back' and the view with the pairing
button is captioned 'front'. Correct captions: print view = 'front', button view = 'back'.
Usage: python3 fix_photo5_labels.py SRC_DIR OUT_DIR   (files named <SKU>_5.jpg, 2000x2000)
Only the two captions change. Every other pixel is untouched."""
import sys, glob, os
import numpy as np
import cv2

# search windows (x0, x1, y0, y1) measured on the source images
WIN = {"print_view": (1300, 1560, 1115, 1200),   # caption under the view with the print
       "button_view": (500, 720, 1885, 1960)}    # caption under the view with the button
TH = 150     # caption pixels are dark gray on a light background
PAD = 10


def bbox(gray, win):
    x0, x1, y0, y1 = win
    ys, xs = np.where(gray[y0:y1, x0:x1] < TH)
    if len(xs) < 300:
        raise ValueError("caption not found")
    return xs.min() + x0, ys.min() + y0, xs.max() + x0 + 1, ys.max() + y0 + 1


def fix(src, dst):
    img = cv2.imread(src)
    if img is None or img.shape[:2] != (2000, 2000):
        raise ValueError("unexpected image")
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY).astype(np.int32)
    boxes = {k: bbox(gray, w) for k, w in WIN.items()}
    # width sanity: 'back' (print view) ~110 px, 'front' (button view) ~120 px
    wp = boxes["print_view"][2] - boxes["print_view"][0]
    wb = boxes["button_view"][2] - boxes["button_view"][0]
    if not (95 <= wp <= 130 and 105 <= wb <= 140):
        raise ValueError(f"caption widths unexpected: {wp}, {wb}")
    # patches with alpha taken from the original captions
    patches = {}
    for k, (x0, y0, x1, y1) in boxes.items():
        crop = img[y0:y1, x0:x1].astype(np.float32)
        g = gray[y0:y1, x0:x1].astype(np.float32)
        bg = np.percentile(g, 95)
        fg = np.percentile(g, 2)
        alpha = np.clip((bg - g) / max(bg - fg, 1), 0, 1)
        alpha = np.clip((alpha - 0.08) / 0.92, 0, 1)   # drop background noise, keep letter edges
        color = crop[alpha > 0.9].mean(axis=0) if (alpha > 0.9).any() else np.array([100, 100, 100], np.float32)
        patches[k] = (alpha, color)
    # erase both captions: mask only the letter pixels (anti-aliased edges included), never the padding
    mask = np.zeros(gray.shape, np.uint8)
    for (x0, y0, x1, y1) in boxes.values():
        bg = np.median(gray[y0 - PAD:y1 + PAD, x0 - PAD:x1 + PAD])
        sub = gray[y0 - 3:y1 + 3, x0 - 3:x1 + 3]
        mask[y0 - 3:y1 + 3, x0 - 3:x1 + 3] = (sub < bg - 4).astype(np.uint8) * 255
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8))
    out = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA).astype(np.float32)
    # paste swapped: the caption of the other view, centered on this view's caption, same baseline
    for target, source in (("print_view", "button_view"), ("button_view", "print_view")):
        tx0, ty0, tx1, ty1 = boxes[target]
        alpha, color = patches[source]
        h, w = alpha.shape
        cx = (tx0 + tx1) // 2
        x0 = cx - w // 2
        y0 = ty1 - h            # align baselines (no descenders in either word)
        region = out[y0:y0 + h, x0:x0 + w]
        a = alpha[..., None]
        out[y0:y0 + h, x0:x0 + w] = region * (1 - a) + color * a
    cv2.imwrite(dst, np.clip(out, 0, 255).astype(np.uint8), [cv2.IMWRITE_JPEG_QUALITY, 95])


if __name__ == "__main__":
    src_dir, out_dir = sys.argv[1], sys.argv[2]
    os.makedirs(out_dir, exist_ok=True)
    bad = 0
    for f in sorted(glob.glob(os.path.join(src_dir, "*_5.jpg"))):
        try:
            fix(f, os.path.join(out_dir, os.path.basename(f)))
        except Exception as e:
            bad += 1
            print("FAILED", os.path.basename(f), e)
    print("done, failures:", bad)
