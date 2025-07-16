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

                for part in parts:
                    part = part.strip()
                    if part.startswith("X +="):
                        val = int(part.split("+=")[1].strip())
                        increments.append((val, 0, 0))
                    elif part.startswith("X -="):
                        val = int(part.split("-=")[1].strip())
                        increments.append((-val, 0, 0))
                    elif part.startswith("Y +="):
                        val = int(part.split("+=")[1].strip())
                        increments.append((0, val, 0))
                    elif part.startswith("Y -="):
                        val = int(part.split("-=")[1].strip())
                        increments.append((0, -val, 0))
                    elif part.startswith("Z +="):
                        val = int(part.split("+=")[1].strip())
                        increments.append((0, 0, val))
                    elif part.startswith("Z -="):
                        val = int(part.split("-=")[1].strip())
                        increments.append((0, 0, -val))
    return increments

def write_csv(increments, csv_path="movement_increments.csv"):
    import pandas as pd
    df = pd.DataFrame(increments, columns=["X", "Y", "Z"])
    df.to_csv(csv_path, index=False)  # this overwrites the file

def git_push(csv_file="movement_increments.csv"):
    subprocess.run(["git", "add", csv_file], check=True)
    subprocess.run(["git", "commit", "-m", "Auto update after chat"], check=True)
    subprocess.run(["git", "push"], check=True)
