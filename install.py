#!/usr/bin/env python3
"""
HrafnBot Installer
Installs HrafnBot CLI tool to a specified directory and adds it to PATH.
Supports both Windows and Linux.
"""
import os
import sys
import shutil
import argparse
import subprocess
import platform
from pathlib import Path

def is_windows():
    """Check if running on Windows"""
    return platform.system() == "Windows"

def get_script_directory():
    """Get the directory where this installer script is located"""
    return os.path.dirname(os.path.abspath(__file__))

def install_dependencies(install_dir):
    """Install Python dependencies"""
    requirements_file = os.path.join(install_dir, "hrafnbot", "requirements.txt")
    if os.path.exists(requirements_file):
        print("Installing Python dependencies...")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", "-r", requirements_file
            ])
            print("Dependencies installed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Warning: Failed to install dependencies: {e}")
            print("Please install dependencies manually with:")
            print(f"pip install -r {requirements_file}")
    else:
        print("Warning: requirements.txt not found. Dependencies may need to be installed manually.")

def copy_files(install_dir):
    """Copy HrafnBot files to the installation directory"""
    script_dir = get_script_directory()
    
    # Create installation directory
    os.makedirs(install_dir, exist_ok=True)
    
    # Files and directories to copy
    items_to_copy = [
        "hrafnbot/",
        "hrafnbot.py",
        "hrafnbot.bat"
    ]
    
    print(f"Copying HrafnBot files to {install_dir}...")
    
    for item in items_to_copy:
        src = os.path.join(script_dir, item)
        dst = os.path.join(install_dir, item)
        
        if os.path.exists(src):
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"Copied directory: {item}")
            else:
                shutil.copy2(src, dst)
                print(f"Copied file: {item}")
        else:
            print(f"Warning: {src} not found, skipping...")
    
    # Make hrafnbot.py executable on Unix-like systems
    if not is_windows():
        hrafnbot_script = os.path.join(install_dir, "hrafnbot.py")
        if os.path.exists(hrafnbot_script):
            os.chmod(hrafnbot_script, 0o755)
            print("Made hrafnbot.py executable")

def add_to_path_windows(install_dir):
    """Add installation directory to Windows PATH"""
    try:
        import winreg
        
        # Get current PATH from registry
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            current_path, _ = winreg.QueryValueEx(key, "PATH")
        except FileNotFoundError:
            current_path = ""
        
        # Check if already in PATH
        if install_dir.lower() in current_path.lower():
            print(f"Directory {install_dir} is already in PATH")
            winreg.CloseKey(key)
            return True
        
        # Add to PATH
        new_path = f"{current_path};{install_dir}" if current_path else install_dir
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        
        # Broadcast change to system
        import ctypes
        from ctypes import wintypes
        
        HWND_BROADCAST = 0xFFFF
        WM_SETTINGCHANGE = 0x001A
        SMTO_ABORTIFHUNG = 0x0002
        
        ctypes.windll.user32.SendMessageTimeoutW(
            HWND_BROADCAST, WM_SETTINGCHANGE, 0, "Environment", 
            SMTO_ABORTIFHUNG, 5000, ctypes.pointer(wintypes.DWORD())
        )
        
        print(f"Added {install_dir} to Windows PATH")
        print("You may need to restart your terminal or log out and back in for changes to take effect.")
        return True
        
    except ImportError:
        print("Warning: winreg module not available. Cannot modify Windows PATH automatically.")
        return False
    except Exception as e:
        print(f"Warning: Failed to add to Windows PATH: {e}")
        return False

def add_to_path_unix(install_dir):
    """Add installation directory to Unix PATH by modifying shell configuration"""
    shell = os.environ.get('SHELL', '/bin/bash')
    
    # Determine which shell config file to modify
    if 'zsh' in shell:
        config_files = ['.zshrc']
    elif 'fish' in shell:
        config_files = ['.config/fish/config.fish']
    else:
        config_files = ['.bashrc', '.bash_profile']
    
    home_dir = os.path.expanduser("~")
    modified = False
    
    for config_file in config_files:
        config_path = os.path.join(home_dir, config_file)
        
        # For fish shell, create directory if needed
        if config_file.startswith('.config'):
            os.makedirs(os.path.dirname(config_path), exist_ok=True)
        
        # Read existing config
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                content = f.read()
        else:
            content = ""
        
        # Check if already added
        path_line = f'export PATH="{install_dir}:$PATH"'
        if 'fish' in shell:
            path_line = f'set -gx PATH "{install_dir}" $PATH'
        
        if install_dir in content:
            print(f"Directory {install_dir} already appears to be in {config_file}")
            continue
        
        # Add PATH export
        with open(config_path, 'a') as f:
            f.write(f"\n# Added by HrafnBot installer\n{path_line}\n")
        
        print(f"Added {install_dir} to PATH in {config_path}")
        modified = True
        break
    
    if modified:
        print("Please restart your terminal or run 'source ~/.bashrc' (or equivalent) for changes to take effect.")
    else:
        print("Could not automatically modify PATH. Please add the following to your shell configuration:")
        print(f'export PATH="{install_dir}:$PATH"')
    
    return modified

def add_to_path(install_dir):
    """Add installation directory to PATH (cross-platform)"""
    if is_windows():
        return add_to_path_windows(install_dir)
    else:
        return add_to_path_unix(install_dir)

def create_symlink_unix(install_dir):
    """Create a symlink to make hrafnbot command available on Unix systems"""
    # Try to create symlink in /usr/local/bin if accessible
    local_bin = "/usr/local/bin"
    hrafnbot_script = os.path.join(install_dir, "hrafnbot.py")
    
    if os.path.isdir(local_bin) and os.access(local_bin, os.W_OK):
        symlink_path = os.path.join(local_bin, "hrafnbot")
        try:
            if os.path.exists(symlink_path):
                os.remove(symlink_path)
            os.symlink(hrafnbot_script, symlink_path)
            print(f"Created symlink: {symlink_path} -> {hrafnbot_script}")
            return True
        except OSError as e:
            print(f"Could not create symlink in {local_bin}: {e}")
    
    return False

def verify_installation(install_dir):
    """Verify that the installation was successful"""
    hrafnbot_script = os.path.join(install_dir, "hrafnbot.py")
    hrafnbot_package = os.path.join(install_dir, "hrafnbot", "__init__.py")
    
    if not os.path.exists(hrafnbot_script):
        print("Error: hrafnbot.py not found in installation directory")
        return False
    
    if not os.path.exists(hrafnbot_package):
        print("Error: hrafnbot package not found in installation directory")
        return False
    
    print("Installation verification successful!")
    return True

def main():
    parser = argparse.ArgumentParser(
        description="Install HrafnBot CLI tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python install.py /opt/hrafnbot          # Linux/Mac
  python install.py C:\\Tools\\HrafnBot     # Windows
        """
    )
    parser.add_argument(
        "install_directory", 
        help="Directory where HrafnBot should be installed"
    )
    parser.add_argument(
        "--no-path", 
        action="store_true", 
        help="Don't automatically add to PATH"
    )
    parser.add_argument(
        "--no-deps", 
        action="store_true", 
        help="Don't install Python dependencies"
    )
    
    args = parser.parse_args()
    
    # Convert to absolute path
    install_dir = os.path.abspath(args.install_directory)
    
    print(f"Installing HrafnBot to: {install_dir}")
    print(f"Platform: {platform.system()}")
    print()
    
    try:
        # Copy files
        copy_files(install_dir)
        
        # Install dependencies
        if not args.no_deps:
            install_dependencies(install_dir)
        
        # Add to PATH
        if not args.no_path:
            path_added = add_to_path(install_dir)
            
            # On Unix, also try to create symlink
            if not is_windows() and not path_added:
                create_symlink_unix(install_dir)
        
        # Verify installation
        if verify_installation(install_dir):
            print()
            print("🎉 HrafnBot installation completed successfully!")
            print()
            print("Usage:")
            if is_windows():
                print("  hrafnbot <input_file.csv>")
                print("  or")
                print(f"  python \"{os.path.join(install_dir, 'hrafnbot.py')}\" <input_file.csv>")
            else:
                print("  hrafnbot <input_file.csv>")
                print("  or")
                print(f"  {os.path.join(install_dir, 'hrafnbot.py')} <input_file.csv>")
            print()
            print("For help:")
            print("  hrafnbot --help")
        else:
            print("❌ Installation verification failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Installation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()