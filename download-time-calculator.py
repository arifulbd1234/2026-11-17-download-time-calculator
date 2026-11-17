# Day 42: Download Time Calculator - 2026-11-17
# What it does: Works out how long a file will take to download at your
# internet speed, converts between file sizes (MB, GB), and tells you what
# speed you need to finish a download in a given time.
# Useful for: Anyone downloading movies, games or big files who wants to know
# whether to start now or wait, and which internet speed is worth paying for.

def convert_size(amount, from_unit, to_unit):
    """Convert a file size between B, KB, MB, GB and TB.

    Example: convert_size(2, "GB", "MB") -> 2048.0
    """
    units = {"B": 0, "KB": 1, "MB": 2, "GB": 3, "TB": 4}
    from_unit = from_unit.upper()
    to_unit = to_unit.upper()
    if from_unit not in units or to_unit not in units:
        raise ValueError("Unit must be one of B, KB, MB, GB, TB.")
    if amount < 0:
        raise ValueError("Amount cannot be negative.")
    bytes_amount = amount * (1024 ** units[from_unit])
    return round(bytes_amount / (1024 ** units[to_unit]), 2)


def download_time_seconds(file_mb, speed_mbps):
    """How many seconds a download takes.

    file_mb is the file size in megabytes, speed_mbps is the internet
    speed in megabits per second (note: 8 megabits = 1 megabyte).
    Example: download_time_seconds(100, 10) -> 80.0 seconds.
    """
    if file_mb < 0 or speed_mbps <= 0:
        raise ValueError("File size cannot be negative and speed must be positive.")
    file_megabits = file_mb * 8
    return round(file_megabits / speed_mbps, 1)


def format_time(seconds):
    """Turn a number of seconds into a friendly '2h 15m 30s' string.

    Example: format_time(8130) -> "2h 15m 30s".
    """
    if seconds < 0:
        raise ValueError("Seconds cannot be negative.")
    seconds = int(round(seconds))
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    parts.append(f"{secs}s")
    return " ".join(parts)


def speed_needed(file_mb, minutes):
    """What internet speed (in Mbps) you need to finish a download
    within a given number of minutes.

    Example: speed_needed(2000, 30) -> about 8.89 Mbps for a 2 GB file in 30 min.
    """
    if file_mb < 0 or minutes <= 0:
        raise ValueError("File size cannot be negative and minutes must be positive.")
    return round((file_mb * 8) / (minutes * 60), 2)


def download_summary(file_mb, speed_mbps):
    """A quick summary: download time in seconds and as a friendly string,
    plus how many files this size you could download in one hour.

    Returns a dict with seconds, a readable time, and files per hour.
    """
    if file_mb <= 0 or speed_mbps <= 0:
        raise ValueError("File size and speed must both be positive.")
    seconds = download_time_seconds(file_mb, speed_mbps)
    files_per_hour = round(3600 / seconds, 1) if seconds > 0 else 0
    return {
        "seconds": seconds,
        "time": format_time(seconds),
        "files_per_hour": files_per_hour,
    }


if __name__ == "__main__":
    # Example 1: A 2 GB movie on a 10 Mbps connection - how long?
    movie = download_summary(2048, 10)
    print("2 GB movie at 10 Mbps takes:", movie["time"],
          f"({movie['seconds']} seconds)")

    # Example 2: A 500 MB app update on a 25 Mbps connection.
    update = download_summary(500, 25)
    print("500 MB update at 25 Mbps takes:", update["time"])

    # Example 3: You want a 5 GB game downloaded in 20 minutes -
    # what speed do you need?
    print("Speed needed for a 5 GB game in 20 minutes:",
          speed_needed(5120, 20), "Mbps")

    # Bonus: unit conversion - 1.5 GB in MB.
    print("1.5 GB =", convert_size(1.5, "GB", "MB"), "MB")
