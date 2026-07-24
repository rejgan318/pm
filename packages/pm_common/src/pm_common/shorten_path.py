from pathlib import Path


def shorten_path(path: str | Path, max_len: int = 60, placeholder: str = "...") -> str:
    """
    Сокращает строку до указанной длины, добавляя в середину ... или placeholder
    Используется, например, для отображения длинных путей в логах.
    """
    path_str = str(path)

    if len(path_str) <= max_len:
        return path_str
    if max_len <= len(placeholder):
        return placeholder[:max_len]

    keep = max_len - len(placeholder)
    left = max(1, keep // 4)
    right = keep - left

    return f"{path_str[:left]}{placeholder}{path_str[-right:]}"


if __name__ == '__main__':
    long_path = "/home/user/very/long/path/to/file.txt"
    print(shorten_path(long_path))
    print(shorten_path(Path(long_path), max_len=25))