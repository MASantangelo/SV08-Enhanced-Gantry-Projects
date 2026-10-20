"""Step 5: the figures used in Mechanical Analysis.md, written to Renders/Analysis/."""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

WORK = os.environ["SV08_ANALYSIS_DIR"]
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(ROOT, "Renders", "Analysis")
os.makedirs(OUT, exist_ok=True)
SURF, INK, INK2, MUTED, GRID, BLUE, RED = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#2a78d6", "#e34948"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10, "axes.edgecolor": MUTED, "text.color": INK,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "svg.hashsalt": "sv08", "path.simplify": True})
SEQ = LinearSegmentedColormap.from_list("blue", ["#e8f0fb", "#9cc3ef", BLUE, "#123e73"])
idlers = json.load(open(os.path.join(WORK, "idlers.json")))
parts = json.load(open(os.path.join(WORK, "parts_Printed.json")))

# ---- plate displacement, front left top plate, all three versions ----
fig, axs = plt.subplots(1, 4, figsize=(17, 4.2))
bolts = [((p["bb"][0] + p["bb"][3]) / 2, (p["bb"][1] + p["bb"][4]) / 2) for p in parts
         if p["label"].startswith(("M4x10mm BHCS", "M4x45mm BHCS")) and any(s.startswith("Front Left Motor") for s in p["parents"])
         and p["bb"][5] > 49.5]
for ax, (key, name) in zip(axs, [("PrintedABS_FrontLeftTop", "Printed (ABS)"), ("CF0-90_FrontLeftTop", "Carbon fiber, weave 0/90"),
                                 ("CF45_FrontLeftTop", "Carbon fiber, weave at 45°"), ("Metal_FrontLeftTop", "6061 aluminium")]):
    d = np.load(os.path.join(WORK, key + "_res.npz"))
    xyz, U = d["xyz"], d["U"]
    top = xyz[:, 2] > xyz[:, 2].max() - 0.05
    mag = np.linalg.norm(U, axis=1)[top] * 1000
    sc = ax.scatter(xyz[top, 0], xyz[top, 1], c=mag, s=1.2, cmap=SEQ, vmin=0, vmax=mag.max(), linewidths=0, rasterized=True)
    for i in idlers:
        if i["asm"] == "Front L":
            f = np.array([i["fx"], i["fy"]]) / i["F"] * 9
            ax.annotate("", xy=(i["x"] + f[0], i["y"] + f[1]), xytext=(i["x"], i["y"]),
                        arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.2))
    for x, y in bolts:
        ax.plot(x, y, marker="x", color=RED, ms=6, mew=1.6)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.set_title(f"{name}\npeak {mag.max():.1f} µm", fontsize=11, color=INK)
    cb = fig.colorbar(sc, ax=ax, fraction=0.035, pad=0.02)
    cb.set_label("displacement (µm)", color=INK2); cb.outline.set_visible(False)
fig.suptitle("Front left top plate under 8 lb belt loads  (arrows: idler loads, red ×: bolts fixed)", fontsize=12, color=INK)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "Plate FEA - Front Left Top.png"), dpi=150, metadata={"Software": None})
plt.close(fig)

# ---- Y-axis thermal bow by version, at both chamber temperatures ----
fr = json.load(open(os.path.join(WORK, "frame_res.json")))
names = list(fr["cases"])
temps = sorted(fr["bow"], key=float)
x = np.arange(len(names)); w = 0.36
fig, ax = plt.subplots(figsize=(8.5, 4.0))
for k, (t, col) in enumerate(zip(temps, (BLUE, "#eb6834"))):
    vals = [fr["bow"][t]["cases"][n]["bow_um"] for n in names]
    bars = ax.bar(x + (k - 0.5) * w, vals, width=w, color=col, edgecolor=SURF, linewidth=2,
                  label=f"{t} °C chamber (free bow {fr['bow'][t]['free_y']:.0f} µm)")
    for bar, v in zip(bars, vals):
        ax.text(bar.get_x() + bar.get_width() / 2, v + 5, f"{v:.0f}", ha="center", color=INK, fontsize=9)
ax.set_xticks(x, names)
ax.set_ylabel("mid-span bow (µm)")
ax.set_title("Y-axis thermal bow, corners fully bonded (best case)", fontsize=11, color=INK, loc="left")
ax.legend(frameon=False, loc="upper right", fontsize=9)
ax.set_ylim(0, max(fr["bow"][t]["cases"][n]["bow_um"] for t in temps for n in names) * 1.35)
ax.grid(axis="y", color=GRID, lw=0.8); ax.set_axisbelow(True)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
fig.tight_layout()
fig.savefig(os.path.join(OUT, "Thermal Bow - Y Axis.png"), dpi=150, metadata={"Software": None})
plt.close(fig)
print("FIGURES written to Renders/Analysis")
