import sys
import os
import pkg_resources

def verify():
    print("🔍 Verifying AI Agent Onboarding Setup...")
    
    # 1. Check Python Version
    version = sys.version_info
    if version.major == 3 and version.minor >= 11:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python version: {version.major}.{version.minor} (Expected 3.11+)")

    # 2. Check Requirements
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            for req in requirements:
                # Handle cases like pkg==version
                name = req.split('==')[0].split('>=')[0]
                pkg_resources.require(name)
        print("✅ Dependencies: All installed")
    except Exception as e:
        print(f"❌ Dependencies: Missing or error - {e}")

    # 3. Check .env
    if os.path.exists('.env'):
        print("✅ .env file: Found")
    else:
        print("⚠️  .env file: Missing (Required for API keys)")

    # 4. Check Folders
    folders = ['src', 'tests', 'data', 'docs']
    missing = [f for f in folders if not os.path.exists(f)]
    if not missing:
        print("✅ Project structure: Valid")
    else:
        print(f"❌ Project structure: Missing {missing}")

    print("\n🎉 Setup check complete!")

if __name__ == "__main__":
    verify()
