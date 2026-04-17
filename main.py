import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from attacker.attacker import run_attacker

if __name__ == "__main__":
    run_attacker()