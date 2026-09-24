"""Score each album photo, so the gallery can lead with the good ones.

Run: python3 tools/score-photos.py

How it works:
- YuNet finds faces, SFace turns each one into a 128-d embedding
- a reference profile is built from the solo portraits already on the site
- the profile is then expanded once with the album's own strongest matches, so
  it covers the angles and lighting the portraits don't
- a photo is kept if any face in it is close enough to the profile

Per photo it records:
  me          how closely the best face matches Aashna (0-1, >=0.363 means it is her)
  prominence  how much of the frame the largest face fills -- close-ups over crowd shots
  sharpness   variance of the Laplacian, a standard blur measure
  faces       how many people are in it

Nothing is deleted or filtered here. build-gallery.py reads the scores and uses
them to decide what leads the gallery.

Writes: tools/photo-scores.json
"""
import json
import pathlib
import sys

import cv2
import numpy as np

ROOT = pathlib.Path(__file__).resolve().parent.parent
MODELS = ROOT / "tools/models"
ALBUM = ROOT / "assets/img/gallery/album"
SCORES = ROOT / "tools/photo-scores.json"

# Solo photos, so every face found in them is hers.
REFERENCES = [
    ROOT / "assets/img/aashna-p-shah-harvard-portrait.jpg",
    ROOT / "assets/img/aashna-p-shah-harvard.jpg",
]

MATCH = 0.363                  # OpenCV's recommended cosine threshold for SFace
BOOTSTRAP = 0.50               # only very confident matches join the profile

detector = cv2.FaceDetectorYN.create(str(MODELS / "face_detection_yunet_2023mar.onnx"), "", (320, 320),
                                     score_threshold=0.75)
recognizer = cv2.FaceRecognizerSF.create(str(MODELS / "face_recognition_sface_2021dec.onnx"), "")


def embeddings(path):
    img = cv2.imread(str(path))
    if img is None:
        return []
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    _, faces = detector.detect(img)
    if faces is None:
        return []
    out = []
    for face in faces:
        try:
            out.append(recognizer.feature(recognizer.alignCrop(img, face)).flatten())
        except cv2.error:
            pass
    return out


def best_face(vecs, profile):
    """The face here that looks most like the profile, and how much: (score, vector)."""
    if not vecs or not profile:
        return 0.0, None
    best = (0.0, None)
    for v in vecs:
        score = max(float(np.dot(v, p) / (np.linalg.norm(v) * np.linalg.norm(p))) for p in profile)
        if score > best[0]:
            best = (score, v)
    return best


def best_match(vecs, profile):
    return best_face(vecs, profile)[0]


profile = []
for ref in REFERENCES:
    found = embeddings(ref)
    if not found:
        print(f"  warning: no face found in reference {ref.name}")
    profile.extend(found)
if not profile:
    sys.exit("no reference faces found -- cannot identify anyone")
print(f"profile seeded with {len(profile)} reference face(s)")

photos = sorted(ALBUM.glob("*.jpg"))
faces = {p: embeddings(p) for p in photos}
print(f"scanned {len(photos)} photos")

# Expand the profile with the album's own most confident matches, so it covers
# angles and lighting the two portraits don't. Only the face that actually
# matched joins the profile -- adding any other face from a group photo would
# teach the profile to recognise someone else as her.
seed = list(profile)
for p, vecs in faces.items():
    score, vec = best_face(vecs, seed)
    if score >= BOOTSTRAP and vec is not None:
        profile.append(vec)
print(f"profile expanded to {len(profile)} faces")

scores = {}
for p in photos:
    vecs = faces[p]
    score, _ = best_face(vecs, profile)
    img = cv2.imread(str(p))
    h, w = img.shape[:2]
    detector.setInputSize((w, h))
    _, boxes = detector.detect(img)
    prominence = 0.0
    if boxes is not None and len(boxes):
        prominence = max(float(b[2] * b[3]) for b in boxes) / (w * h)
    sharpness = float(cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), cv2.CV_64F).var())
    scores[p.name] = {
        "me": round(score, 4),
        "is_me": score >= MATCH,
        "faces": 0 if boxes is None else len(boxes),
        "prominence": round(prominence, 5),
        "sharpness": round(sharpness, 1),
    }

SCORES.write_text(json.dumps(scores, indent=1, sort_keys=True))
mine = sum(1 for v in scores.values() if v["is_me"])
print(f"scored {len(scores)} photos; {mine} look like they have you in them")
print(f"wrote {SCORES.relative_to(ROOT)}")
