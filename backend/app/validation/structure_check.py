import os


REQUIRED_INDICATORS = ["README", "requirements.txt", "package.json", "composer.json", "pubspec.yaml"]


def check_structure(local_path: str) -> dict:
    found_files = os.listdir(local_path)
    has_readme = any(f.lower().startswith("readme") for f in found_files)
    has_dependency_file = any(
        f in found_files for f in ["requirements.txt", "package.json", "composer.json", "pubspec.yaml"]
    )
    has_src_folder = any(
        os.path.isdir(os.path.join(local_path, f)) for f in found_files
    )

    return {
        "has_readme": has_readme,
        "has_dependency_file": has_dependency_file,
        "has_folders": has_src_folder,
        "passed": has_dependency_file and has_src_folder,
    }
