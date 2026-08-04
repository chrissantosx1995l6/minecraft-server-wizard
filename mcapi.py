from pathlib import Path
import httpx

# Mojang version manifest url
MANIFEST_URL = "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json"
PAPER_API = "https://api.papermc.io/v2/projects/paper"

def get_vanilla_download_url(version: str) -> str:
    r = httpx.get(MANIFEST_URL)
    r.raise_for_status()
    data = r.json()

    version_entry = next((v for v in data["versions"] if v["id"] == version), None)
    if not version_entry:
        raise ValueError(f"Minecraft version {version} not found in Mojang manifest")

    meta_url = version_entry["url"]
    meta_r = httpx.get(meta_url)
    meta_r.raise_for_status()
    meta_data = meta_r.json()

    server_download = meta_data.get("downloads", {}).get("server")
    if not server_download:
        raise ValueError(f"No server download available for version {version}")

    return server_download["url"]

def get_paper_download_url(version: str) -> str:
    # gets the url for the latest stable build of paper for a given mc version
    builds_url = f"{PAPER_API}/versions/{version}/builds"
    r = httpx.get(builds_url)
    if r.status_code == 404:
        raise ValueError(f"Paper version {version} not found or unsupported")
    r.raise_for_status()
    
    data = r.json()
    # Filter builds to find actual releases, ignoring pre-releases where possible
    builds = [b for b in data.get("builds", []) if b.get("channel") == "default"]
    if not builds:
        builds = data.get("builds", [])
        
    if not builds:
        raise ValueError(f"No builds found for Paper version {version}")
        
    latest_build = builds[-1]
    build_number = latest_build["build"]
    
    downloads = latest_build.get("downloads", {})
    application_download = downloads.get("application")
    if not application_download:
        raise ValueError(f"No application jar found for build {build_number}")
        
    filename = application_download["name"]
    return f"{PAPER_API}/versions/{version}/builds/{build_number}/downloads/{filename}"

def download_jar(url: str, destPath: Path):
    with httpx.stream("GET", url, follow_redirects=True) as response:
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        downloaded = 0
        with open(destPath, "wb") as f:
            for chunk in response.iter_bytes(chunk_size=16384): # larger chunk size works better on faster connections
                f.write(chunk)
                downloaded += len(chunk)
                if total > 0:
                    percent = int(downloaded * 100 / total)
                    # print(f"dbg: {downloaded}/{total}")
                    print(f"Downloading: {percent}%\r", end="", flush=True)
        print()
