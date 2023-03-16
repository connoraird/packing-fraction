import matplotlib.pyplot as plt

def plot_coordinates(width, height, radius, coordinates):
    longest = width if width > height else width 
    point_ration = radius / longest

    fig, ax = plt.subplots(figsize=(10*width/longest, 10*height/longest))

    # Plot the data
    ax.scatter(
        coordinates["x"], 
        coordinates["y"],
        c=coordinates["rank"],
        s=point_ration * 10000 * radius
    )
    ax.set_xlim([0,width])
    ax.set_ylim([0,height])

    # Customise the plot
    ax.set(
        title="Circle coordinates",
        xlabel="x",
        ylabel="y"
    )

    fig.savefig("coordinates.png")

def plot_samples_vs_PF(samples_vs_PF_DF):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(samples_vs_PF_DF["Number of Samples"], samples_vs_PF_DF["Packing Fraction"])

    fig.savefig("PF_vs_samples.png")

def plot(width, height, radius, samples_vs_PF_DF, coordinates_DF):
    plot_coordinates(width, height, radius, coordinates_DF)
    plot_samples_vs_PF(samples_vs_PF_DF)


