#!/usr/bin/env python3
"""
JumpCutter Pro Launcher

This script launches the best available version of JumpCutter GUI.
"""

import sys
import subprocess
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = {
        'PyQt6': 'PyQt6',
        'moviepy': 'moviepy',
        'numpy': 'numpy',
        'tqdm': 'tqdm'
    }
    
    missing_packages = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(pip_name)
    
    return missing_packages

def install_requirements(packages):
    """Install missing packages."""
    print(f"Installing missing packages: {', '.join(packages)}")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        return True
    except subprocess.CalledProcessError:
        return False

def launch_gui():
    """Launch the appropriate GUI version."""
    script_dir = Path(__file__).parent
    
    # Try enhanced version first
    enhanced_gui = script_dir / "jump_cutter_gui_enhanced.py"
    if enhanced_gui.exists():
        try:
            subprocess.run([sys.executable, str(enhanced_gui)])
            return
        except Exception as e:
            print(f"Failed to launch enhanced GUI: {e}")
    
    # Fall back to Qt version
    qt_gui = script_dir / "jump_cutter_gui_qt.py"
    if qt_gui.exists():
        try:
            subprocess.run([sys.executable, str(qt_gui)])
            return
        except Exception as e:
            print(f"Failed to launch Qt GUI: {e}")
    
    # Fall back to Tkinter version
    tk_gui = script_dir / "jump_cutter_gui.py"
    if tk_gui.exists():
        try:
            subprocess.run([sys.executable, str(tk_gui)])
            return
        except Exception as e:
            print(f"Failed to launch Tkinter GUI: {e}")
    
    print("No GUI version could be launched!")

def main():
    """Main launcher function."""
    print("JumpCutter Pro Launcher")
    print("=" * 30)
    
    # Check requirements
    missing = check_requirements()
    
    if missing:
        print(f"Missing required packages: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ")
        
        if response.lower() in ['y', 'yes']:
            if install_requirements(missing):
                print("Packages installed successfully!")
            else:
                print("Failed to install packages. Please install manually:")
                print(f"pip install {' '.join(missing)}")
                return
        else:
            print("Cannot proceed without required packages.")
            return
    
    # Launch GUI
    print("Launching JumpCutter Pro...")
    launch_gui()

if __name__ == "__main__":
    main()