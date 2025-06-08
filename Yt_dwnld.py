import yt_dlp


def download_youtube_video(video_url):
    """Downloads a YouTube video using yt-dlp."""

    ydl_opts = {
        "outtmpl": "%(title)s.%(ext)s",  # Output filename template
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(video_url, download=False)
        formats = info_dict.get("formats", [])

        if not formats:
            print("❌ No formats available for this video.")
            return

        # Print all the available formats
        print("\nAvailable formats:")
        for f in formats:
            format_note = f.get("format_note", "")
            height = f.get("height", "N/A")
            print(f"{f['format_id']}: {f['ext']} ({height}p) {format_note}")

        # Ask user if they want to choose format manually
        resolution_choice = input("\nDo you want to select format manually? (y/n): ")

        if resolution_choice.lower() == "y":
            format_id = input("Enter the format id of the video: ")
            ydl_opts["format"] = format_id
        else:
            # Filter formats with height not None
            valid_formats = [f for f in formats if f.get("height") is not None]
            if not valid_formats:
                print("❌ No downloadable formats with resolution found.")
                return
            highest_resolution = max(valid_formats, key=lambda x: x.get("height", 0))
            format_id = highest_resolution["format_id"]
            ydl_opts["format"] = format_id

        # Download the video using selected format
        print(f"\n⬇️ Downloading using format id: {format_id} ...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl_download:
            ydl_download.download([video_url])

        print("\n✅ Download complete!")


if __name__ == "__main__":
    video_url = input("🎥 Enter the YouTube video URL: ")
    download_youtube_video(video_url)
