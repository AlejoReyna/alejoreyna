# Terminal profile README setup

## 1. Add your data

Edit `profile.json`. Replace `YOUR_GITHUB_USERNAME` and every example value. Use a valid IANA timezone such as `America/Monterrey`, `Europe/London`, or `Asia/Kolkata`.

The supported item colors are `value`, `accent`, `warning`, and `muted`. Keep the right-hand text compact; long values wrap automatically.

## 2. Create your portrait

Use a well-lit, front-facing photo with your head and upper torso visible. A plain background helps, but the converter removes the background automatically.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-portrait.txt
python photo_to_ascii.py /absolute/path/to/photo.jpg
```

If the result needs tuning:

```bash
python photo_to_ascii.py /absolute/path/to/photo.jpg --columns 92 --bust .68 --detail 2.5 --shape .42 --trim-x .1
```

- Increase `--detail` when dark clothing looks flat.
- Decrease `--shape` when shadows dominate the portrait.
- Adjust `--bust` between `.55` and `.8` to change the crop.
- Increase `--trim-x` to zoom toward the face when wide shoulders make it look too small.
- Try a photo with clearer, softer lighting before pushing the settings too far.
- The default `u2net_human_seg` model is optimized for portraits. Try `--model u2net` for non-human subjects.

The portrait dependencies are only used on your computer. The daily GitHub workflow needs no Python packages.

## 3. Preview locally

```bash
python generate_profile.py
```

Open `profile-dark.svg` and `profile-light.svg` in a browser. If the right column reaches the footer, shorten some text or remove an item.

## 4. Publish on your GitHub profile

1. Create a **public** repository whose name exactly matches your GitHub username.
2. Copy every file and the `.github` folder from this kit into that repository.
3. Run `python generate_profile.py` once and commit both generated SVG files.
4. Push to the repository's default branch.
5. Open the Actions tab and run **Update terminal profile** once to confirm write access.

GitHub displays `README.md` from a public repository named exactly like your username on your profile. The workflow refreshes the stats and timestamp daily.

## Privacy note

Everything in `profile.json` becomes public. Do not include a private email address, exact home address, phone number, secrets, or private project/client names.
