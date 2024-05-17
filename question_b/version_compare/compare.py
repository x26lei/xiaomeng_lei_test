def compare_versions(version1, version2):
    """
    Compare two version strings.

    Args:
    version1 (str): The first version string (e.g., "1.2").
    version2 (str): The second version string (e.g., "1.1").

    Returns:
    int: -1 if version1 < version2, 0 if version1 == version2, 1 if version1 > version2.
    """
    # split the version strings into components
    v1_components = list(map(int, version1.split('.')))
    v2_components = list(map(int, version2.split('.')))
    
    # pad the shorter list with zeros (e.g., "1.2" -> "1.2.0" when compared to "1.2.1")
    max_length = max(len(v1_components), len(v2_components))
    v1_components.extend([0] * (max_length - len(v1_components)))
    v2_components.extend([0] * (max_length - len(v2_components)))
    
    # compare each component
    for v1, v2 in zip(v1_components, v2_components):
        if v1 < v2:
            return -1
        elif v1 > v2:
            return 1
        
    # all components are equal
    return 0
