import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.path import Path
from matplotlib.lines import Line2D

# ====================================================================
# 1. DATA -- edit these to match any updated results
# ====================================================================

# The six trust dimensions (exogenous constructs), listed top -> bottom
TRUST = ["CT", "ET", "ST", "DT", "HBT", "IT"]

TRUST_LABELS = {
    "CT":  "Cognitive\nTrust",
    "ET":  "Emotional\nTrust",
    "ST":  "Situational\nTrust",
    "DT":  "Dispositional\nTrust",
    "HBT": "History-Based\nTrust",
    "IT":  "Institutional\nTrust",
}

# Direct path coefficients -- Table 4.9
# (hypothesis, from, to, std_estimate, p_value, supported?)
DIRECT_PATHS = [
    ("H1",  "CT",  "IU", 0.117, 0.026, True),
    ("H2",  "ET",  "IU", 0.220, 0.000, True),
    ("H3",  "ST",  "IU", 0.140, 0.012, True),
    ("H4",  "DT",  "IU", 0.197, 0.000, True),
    ("H5",  "HBT", "IU", 0.139, 0.008, True),
    ("H6",  "IT",  "IU", 0.140, 0.006, True),
    ("H7",  "CT",  "CE", 0.140, 0.193, False),
    ("H8",  "ET",  "CE", 0.140, 0.002, True),
    ("H9",  "ST",  "CE", 0.117, 0.638, False),
    ("H10", "DT",  "CE", 0.139, 0.000, True),
    ("H11", "HBT", "CE", 0.197, 0.000, True),
    ("H12", "IT",  "CE", 0.220, 0.033, True),
    ("H13", "IU",  "CE", 0.073, 0.024, True),
]

SUPPORTED_COLOR = "black"
NOT_SUPPORTED_COLOR = "#999999"


# ====================================================================
# 2. HELPER FUNCTIONS
# ====================================================================

def sig_stars(p):
    """APA-style significance stars for a p-value."""
    if p < 0.001:
        return "***"
    elif p < 0.01:
        return "**"
    elif p < 0.05:
        return "*"
    return "(ns)"


def quad_bezier_point(p0, p1, p2, t):
    """Point on a quadratic Bezier curve at parameter t in [0, 1]."""
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def draw_box(ax, cx, cy, w, h, text, facecolor, fontsize=9.8):
    """Draw a labeled rounded rectangle centered at (cx, cy)."""
    box = mpatches.FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle="round,pad=0.02,rounding_size=0.12",
        linewidth=1.6, edgecolor="black", facecolor=facecolor, zorder=3,
    )
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize,
            fontweight="bold", zorder=4)
    return {"cx": cx, "cy": cy, "w": w, "h": h}


def edge_point(box, side, offset=0.0):
    """Point on the left/right perimeter of a box, shifted vertically
    by `offset` (lets several lines land on distinct spots on a box)."""
    x = box["cx"] - box["w"] / 2 if side == "left" else box["cx"] + box["w"] / 2
    return (x, box["cy"] + offset)


def draw_curved_path(ax, start, ctrl, end, color, lw, linestyle, label,
                       label_t=0.5, zorder=2):
    """Draw a quadratic Bezier curve without arrowheads and place its label
    directly on the curve at parameter `label_t`."""
    path = Path([start, ctrl, end], [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    
    # EDITED: Changed arrowstyle to "-" to remove arrowheads completely
    line_path = mpatches.FancyArrowPatch(
        path=path, arrowstyle="-", mutation_scale=16,
        linewidth=lw, edgecolor=color, facecolor=color,
        linestyle=linestyle, zorder=zorder,
    )
    ax.add_patch(line_path)
    if label:
        lx, ly = quad_bezier_point(start, ctrl, end, label_t)
        ax.text(lx, ly, label, fontsize=8.2, ha="center", va="center",
                color=color, zorder=5, linespacing=1.3,
                bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                          edgecolor="none", alpha=0.88))


# ====================================================================
# 3. BUILD THE FIGURE
# ====================================================================

# EDITED: Simplified figure initialization to completely remove the table panel
fig, ax = plt.subplots(figsize=(15.5, 9.5))

ax.set_xlim(-0.5, 14.2)
ax.set_ylim(-2.3, 11.2)
ax.axis("off")
ax.set_title(
    "SEM Path Diagram\nTrust Dimensions \u2192 Intention to Use (IU) \u2192 Continued Engagement (CE) with LLMs",
    fontsize=14.5, fontweight="bold", pad=10,
)

# --- Boxes ----------------------------------------------------------
trust_x = 1.6
trust_w, trust_h = 2.3, 1.0
trust_y_positions = [9.5, 7.7, 5.9, 4.1, 2.3, 0.5]

boxes = {}
for name, y in zip(TRUST, trust_y_positions):
    boxes[name] = draw_box(ax, trust_x, y, trust_w, trust_h,
                            TRUST_LABELS[name], facecolor="#cfe2f3")

boxes["IU"] = draw_box(ax, 7.1, 5.0, 2.8, 1.5, "Intention\nto Use\n(IU)",
                        facecolor="#fce5cd")
boxes["CE"] = draw_box(ax, 12.6, 5.0, 2.8, 1.5, "Continued\nEngagement\n(CE)",
                        facecolor="#d9ead3")

# --- Edge attachment offsets (spreads multiple lines along an edge) -
iu_offsets = dict(zip(TRUST, [-0.44, -0.27, -0.09, 0.09, 0.27, 0.44]))
ce_slots = ["CT", "ET", "ST", "IU", "DT", "HBT", "IT"]
ce_offset_vals = [-0.50, -0.33, -0.16, 0.0, 0.16, 0.33, 0.50]
ce_offsets = dict(zip(ce_slots, ce_offset_vals))

# --- Draw the 13 direct paths (H1-H13) -------------------------------
for hyp, src, dst, coef, p, supported in DIRECT_PATHS:
    color = SUPPORTED_COLOR if supported else NOT_SUPPORTED_COLOR
    style = "solid" if supported else "dashed"
    lw = 1.0 + abs(coef) * 7.5
    label = "{0}: \u03b2={1:.3f} {2}".format(hyp, coef, sig_stars(p))

    if dst == "IU":
        start = edge_point(boxes[src], "right")
        end = edge_point(boxes["IU"], "left", iu_offsets[src])
        ctrl = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        draw_curved_path(ax, start, ctrl, end, color, lw, style, label, label_t=0.58)

    elif dst == "CE" and src != "IU":
        side_offset = 0.18 if boxes[src]["cy"] >= 5.0 else -0.18
        start = edge_point(boxes[src], "right", side_offset)
        end = edge_point(boxes["CE"], "left", ce_offsets[src])
        if boxes[src]["cy"] >= 5.0:
            ctrl = (boxes["IU"]["cx"], 10.6)
        else:
            ctrl = (boxes["IU"]["cx"], -2.1)
        draw_curved_path(ax, start, ctrl, end, color, lw, style, label, label_t=0.5)

    else:  # IU -> CE
        start = edge_point(boxes["IU"], "right")
        end = edge_point(boxes["CE"], "left", ce_offsets["IU"])
        ctrl = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
        draw_curved_path(ax, start, ctrl, end, color, 1.0 + abs(coef) * 7.5,
                           style, label, label_t=0.5)

# --- Legend -----------------------------------------------------------
legend_elements = [
    Line2D([0], [0], color="black", lw=2.4, label="Supported path (p < .05)"),
    Line2D([0], [0], color=NOT_SUPPORTED_COLOR, lw=1.6, linestyle="dashed",
           label="Not supported (p \u2265 .05)"),
]
ax.legend(handles=legend_elements, loc="upper left",
          bbox_to_anchor=(0.0, 0.04), fontsize=9.5, frameon=False)
ax.text(14.1, -2.15, "* p<.05   ** p<.01   *** p<.001   (ns) = not significant",
        fontsize=8.8, ha="right", style="italic", color="#444444")

fig.tight_layout()

# ====================================================================
# 4. SAVE + SHOW
# ====================================================================
plt.savefig("sem_path_diagram.png", dpi=300, bbox_inches="tight")
print("Diagram saved as 'sem_path_diagram.png' in the current working directory.")
plt.show()