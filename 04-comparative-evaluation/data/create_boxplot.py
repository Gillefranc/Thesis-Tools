import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 12,
    "axes.labelsize": 11,
    "axes.titlesize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "figure.dpi": 400,
})

OUTPUT_PATH = "Images/boxplot.png"

def create_boxplot(stats_dict):
    labels = list(stats_dict.keys())
    box_data = []
    y_values = set()

    for label in labels:
        s = stats_dict[label]
        box_data.append({
            'label': label,
            'whislo': s['min'],
            'q1': s['q1'],
            'med': s['q2'],
            'q3': s['q3'],
            'whishi': s['max'],
            'fliers': []
        })
        y_values.update([s['min'], s['q1'], s['q2'], s['q3'], s['max'], s['avg']])
    y_values.add(60)

    yticks = sorted(y_values)

    fig, ax = plt.subplots(figsize=(5, 5))  # Compact but square

    # Adjust boxprops to widen the boxes
    ax.bxp(
        box_data,
        showfliers=False,
        widths=0.5  # Widen box
    )

    # Draw average lines
    for i, label in enumerate(labels):
        avg = stats_dict[label]['avg']
        ax.hlines(avg, i + 1 - 0.25, i + 1 + 0.25, colors='black', linewidth=2)

    ax.set_ylabel("Recovery Time (s)")
    ax.set_title("Recovery Time of Node")
    ax.set_yticks(yticks)
    ax.set_yticklabels([str(y) for y in yticks])

    # Reference line and properly placed label inside plot
    # ax.axhline(y=60, color='red', linestyle='--', linewidth=1)
    # ax.text(
    #     x=0.5,
    #     y=61.5,
    #     s="Network Recovered",
    #     color='red',
    #     fontsize=10,
    #     ha='left'
    # )

    plt.grid(True, axis='y')
    # plt.tight_layout()
    plt.savefig(OUTPUT_PATH)

data = {
    "KubeEdge": {"min": 40, "q1": 64, "q2": 93, "q3": 117, "max": 132, "avg": 93},
    "Feather": {"min": 15, "q1": 30, "q2": 41, "q3": 53, "max": 67, "avg": 41}
}

create_boxplot(data)
