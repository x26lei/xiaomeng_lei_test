def do_lines_overlap(line1, line2):
    """
    Determine if two lines on the x-axis overlap.

    Args:
    line1 (tuple): A tuple containing the start and end points (x1, x2) of the first line.
    line2 (tuple): A tuple containing the start and end points (x3, x4) of the second line.

    Returns:
    bool: True if the lines overlap, False otherwise.
    """
    x1, x2 = sorted(line1)  # ensure line1 is ordered correctly
    x3, x4 = sorted(line2)  # ensure line2 is ordered correctly

    # check for overlap
    return max(x1, x3) <= min(x2, x4)

if __name__ == "__main__":
    line1 = (1, 5)
    line2 = (2, 6)
    print(do_lines_overlap(line1, line2))  # Output: True

    line3 = (1, 5)
    line4 = (6, 8)
    print(do_lines_overlap(line3, line4))  # Output: False