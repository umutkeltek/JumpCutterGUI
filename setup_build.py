"""
Setup script for building JumpCutter Pro standalone executable.
"""

import subprocess
import sys
import os
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            return True
        except subprocess.CalledProcessError:
            print("Failed to install PyInstaller.")
            return False

def build_executable():
    """Build standalone executable."""
    script_dir = Path(__file__).parent
    
    # Build enhanced GUI
    enhanced_script = script_dir / "jump_cutter_gui_enhanced.py"
    if enhanced_script.exists():
        print("Building JumpCutter Pro Enhanced...")
        
        cmd = [
            'pyinstaller',
            '--onefile',
            '--windowed',
            '--name', 'JumpCutterPro',
            '--icon', str(script_dir / 'icon.ico') if (script_dir / 'icon.ico').exists() else None,
            '--add-data', f"{script_dir / 'presets.py'};.",
            '--add-data', f"{script_dir / 'utils.py'};.",
            str(enhanced_script)
        ]
        
        # Remove None values
        cmd = [arg for arg in cmd if arg is not None]
        
        try:
            subprocess.run(cmd, check=True)
            print("Build completed successfully!")
            print(f"Executable location: {script_dir / 'dist' / 'JumpCutterPro.exe'}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Build failed: {e}")
            return False
    else:
        print("Enhanced GUI script not found!")
        return False

def clean_build():
    """Clean build artifacts."""
    script_dir = Path(__file__).parent
    
    # Remove build directories
    for dir_name in ['build', '__pycache__']:
        dir_path = script_dir / dir_name
        if dir_path.exists():
            import shutil
            shutil.rmtree(dir_path)
            print(f"Cleaned {dir_name} directory")
    
    # Remove spec file
    spec_file = script_dir / "JumpCutterPro.spec"
    if spec_file.exists():
        spec_file.unlink()
        print("Cleaned spec file")

def main():
    """Main setup function."""
    print("JumpCutter Pro Build Setup")
    print("=" * 30)
    
    import argparse
    parser = argparse.ArgumentParser(description="Build JumpCutter Pro executable")
    parser.add_argument('--clean', action='store_true', help='Clean build artifacts')
    parser.add_argument('--build', action='store_true', help='Build executable')
    
    args = parser.parse_args()
    
    if args.clean:
        clean_build()
        return
    
    if args.build or not any(vars(args).values()):
        # Install PyInstaller
        if not install_pyinstaller():
            return
        
        # Build executable
        if build_executable():
            print("\n✅ Build completed successfully!")
            print("You can find the executable in the 'dist' folder.")
        else:
            print("\n❌ Build failed!")

if __name__ == "__main__":
    main()