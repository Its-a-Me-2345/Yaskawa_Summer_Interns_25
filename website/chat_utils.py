import pandas as pd
import subprocess

def append_chat_to_file(user_input, output, path="chat_output.txt"):
    with open(path, "a") as f:
        f.write(f"User: {user_input}\n")
        f.write(f"Output: {output}\n\n")

def extract_increments(path="chat_output.txt"):
    increments = []
    with open(path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("Output:"):
                output_line = line.replace("Output:", "").strip().replace("End Task", "")
                parts = output_line.split(",")

                x, y, z = 0, 0, 0
                for part in parts:
                    part = part.strip()
                    if part.startswith("X +="):
                        x += int(part.split("+=")[1].strip())
                    elif part.startswith("X -="):
                        x -= int(part.split("-=")[1].strip())
                    elif part.startswith("Y +="):
                        y += int(part.split("+=")[1].strip())
                    elif part.startswith("Y -="):
                        y -= int(part.split("-=")[1].strip())
                    elif part.startswith("Z +="):
                        z += int(part.split("+=")[1].strip())
                    elif part.startswith("Z -="):
                        z -= int(part.split("-=")[1].strip())
                increments.append((x, y, z))
    return increments

def write_csv(increments, csv_path="movement_increments.csv"):
    import pandas as pd
    df = pd.DataFrame(increments, columns=["X", "Y", "Z"])
    df.to_csv(csv_path, index=False)  # this overwrites the file

def git_push(file_name):
    subprocess.run(["git", "add", file_name], check=True)
    subprocess.run(["git", "commit", "-m", "Auto update after chat"], check=True)
    subprocess.run(["git", "push"], check=True)

