#!/usr/bin/env python3
"""
Docker Operations Helper Script

This script provides utilities for managing Docker operations in the MLOps project.
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Constants
DOCKER_REPO = os.environ.get("DOCKER_USERNAME", "iahmadraza7")
IMAGE_NAME = "mlops-app"
TAG = "latest"

def run_command(cmd, check=True):
    """Run a shell command and print output"""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, check=check, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result

def build_image(args):
    """Build Docker image"""
    cmd = ["docker", "build", "-t", f"{DOCKER_REPO}/{IMAGE_NAME}:{TAG}"]
    
    # Add build arguments if provided
    if args.build_args:
        for arg in args.build_args:
            cmd.extend(["--build-arg", arg])
    
    # Add dockerfile if specified
    if args.dockerfile:
        cmd.extend(["-f", args.dockerfile])
    
    # Add context
    cmd.append(".")
    
    run_command(cmd)
    print(f"✅ Image built: {DOCKER_REPO}/{IMAGE_NAME}:{TAG}")

def push_image(args):
    """Push Docker image to registry"""
    # Ensure user is logged in
    if not args.skip_login:
        print("Please login to Docker Hub:")
        run_command(["docker", "login"], check=False)
    
    # Push the image
    run_command(["docker", "push", f"{DOCKER_REPO}/{IMAGE_NAME}:{TAG}"])
    print(f"✅ Image pushed: {DOCKER_REPO}/{IMAGE_NAME}:{TAG}")

def run_container(args):
    """Run Docker container"""
    # Stop existing container if running
    run_command(["docker", "stop", IMAGE_NAME], check=False)
    run_command(["docker", "rm", IMAGE_NAME], check=False)
    
    # Run new container
    cmd = [
        "docker", "run",
        "--name", IMAGE_NAME,
        "-p", f"{args.port}:5000",
        "-d"  # Detached mode
    ]
    
    # Add environment variables
    if args.env:
        for env_var in args.env:
            cmd.extend(["-e", env_var])
    
    # Add volumes
    if args.volume:
        for volume in args.volume:
            cmd.extend(["-v", volume])
    
    # Add image name
    cmd.append(f"{DOCKER_REPO}/{IMAGE_NAME}:{TAG}")
    
    run_command(cmd)
    print(f"✅ Container running at http://localhost:{args.port}")

def compose_up(args):
    """Run docker-compose up"""
    cmd = ["docker-compose", "up"]
    
    if args.detach:
        cmd.append("-d")
    
    if args.build:
        cmd.append("--build")
    
    run_command(cmd)
    print("✅ Docker Compose services started")

def compose_down(args):
    """Run docker-compose down"""
    cmd = ["docker-compose", "down"]
    
    if args.volumes:
        cmd.append("-v")
    
    run_command(cmd)
    print("✅ Docker Compose services stopped")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Docker Operations Helper")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build Docker image")
    build_parser.add_argument("--build-args", "-b", nargs="+", help="Build arguments")
    build_parser.add_argument("--dockerfile", "-f", help="Path to Dockerfile")
    
    # Push command
    push_parser = subparsers.add_parser("push", help="Push Docker image")
    push_parser.add_argument("--skip-login", action="store_true", help="Skip Docker login")
    
    # Run command
    run_parser = subparsers.add_parser("run", help="Run Docker container")
    run_parser.add_argument("--port", "-p", default="5000", help="Port to expose")
    run_parser.add_argument("--env", "-e", nargs="+", help="Environment variables")
    run_parser.add_argument("--volume", "-v", nargs="+", help="Volumes to mount")
    
    # Compose up command
    compose_up_parser = subparsers.add_parser("compose-up", help="Run docker-compose up")
    compose_up_parser.add_argument("--detach", "-d", action="store_true", help="Run in detached mode")
    compose_up_parser.add_argument("--build", "-b", action="store_true", help="Build images before starting")
    
    # Compose down command
    compose_down_parser = subparsers.add_parser("compose-down", help="Run docker-compose down")
    compose_down_parser.add_argument("--volumes", "-v", action="store_true", help="Remove volumes")
    
    args = parser.parse_args()
    
    # Execute command
    if args.command == "build":
        build_image(args)
    elif args.command == "push":
        push_image(args)
    elif args.command == "run":
        run_container(args)
    elif args.command == "compose-up":
        compose_up(args)
    elif args.command == "compose-down":
        compose_down(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main() 