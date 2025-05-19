import os
import pandas as pd
import matplotlib.pyplot as plt

BASE_DIR = "./"
OUTPUT_DIR = "Images"
FRAMEWORKS = ["Feather"]
EXPERIMENT = "04_disconnect"
METRICS = ["cpu.csv", "memory.csv"]
TIME_LIMIT = 360 # seconds

ACTIONS = [
    # (31, "Network Disconnected", "dotted"),
    # (72, "KubeEdge Node NotReady", "solid"),
    # (85, "Feather Node NotReady", "dashed"),
    # (211, "Network Reconnected", "dotted"),
    # (260, "Feather Node Ready", "dashed"),
    # (338, "KubeEdge Node Ready", "solid"),
]

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


def load_data(frameworks, experiment, metric):
    data = {}
    for framework in frameworks:
        file_path = os.path.join(BASE_DIR, framework, experiment, metric)
        df = pd.read_csv(file_path)
        data[framework] = df
    print(data)
    return data


def plot_metric(data, metric_name, output_path, time_limit, actions):
    fig, ax = plt.subplots(figsize=(6, 4))

    line_styles = ['solid', 'dashed', 'dotted', 'dashdot']
    style_cycle = iter(line_styles)

    all_values = []
    for label, df in data.items():
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['time_sec'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.total_seconds()
        df = df[df['time_sec'] <= time_limit]

        all_values.extend(df.iloc[:, 1].tolist())

        linestyle = next(style_cycle, 'solid')
        ax.plot(df['time_sec'], df.iloc[:, 1], label=label, markersize='1', linestyle=linestyle, linewidth=1.5,
                color='black',)

    bottom = min(all_values) * 0.9
    top = max(all_values) * 1.1
    ax.set_ylim(bottom=bottom, top=top)

    for i, (action_time, description, linestyle) in enumerate(actions):
        side = 'right'
        ax.axvline(x=action_time, color="black", linestyle=linestyle, linewidth=0.8)
        ax.text(action_time, 7, description, rotation=90,
                verticalalignment='top', horizontalalignment=side, fontsize=8, color='grey')

    ax.set_xlabel("Time (s)")
    unit = "(MB)" if "memory" in metric_name else "(%)" if "cpu" in metric_name else "()"
    ax.set_ylabel(f"{metric_name.capitalize()} {unit}")
    ax.set_title(f"{metric_name.capitalize()} Usage")
    ax.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7)
    ax.minorticks_on()
    ax.grid(True, which='minor', linestyle=':', linewidth=0.3, alpha=0.5)
    ax.legend()
    plt.tight_layout()

    plt.savefig(output_path)
    plt.close()
    print(f"Saved: {output_path}")


# Main execution
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

for metric in METRICS:
    for number in range(2, 6):
        metric_name = metric.split('.')[0]
        data = load_data(FRAMEWORKS, f"{EXPERIMENT}/{number}", metric)
        # Output folder
        os.makedirs(f"{OUTPUT_DIR}/{number}", exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, f"{number}/{metric_name}_comparison.png")
        plot_metric(data, metric_name, output_path, TIME_LIMIT, ACTIONS)
