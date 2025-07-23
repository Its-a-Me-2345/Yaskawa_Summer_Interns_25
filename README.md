# Yaskawa_Summer_Interns_25

## 🤖 Chobo — NLP-to-Robotics Command Translation

**Chobo** is a prototype system developed during my internship at **Yaskawa India Private Limited** (Robotics Division), aimed at bridging the gap between human language and robotic execution. The project focuses on converting natural language commands into low-level robot instructions using Yaskawa’s proprietary Python libraries.

### 🧠 Objective

To enable industrial robots to understand and perform actions based on high-level natural language prompts.

### 🔍 How It Works

1. **User Input**: A natural language instruction is given (e.g., *“Move up by 20”*)
2. **Parsing & Interpretation**: The instruction is parsed using NLP techniques.
3. **Command Generation**: The parsed result is translated into coordinate-based robot instructions.
4. **Execution**: Instructions are executed using Yaskawa’s Python interface (on a physical robot).

### 🚀 Features

- Natural language command parsing
- Mapping linguistic intent to robotic operations
- Generation of robot movement code based on 3D coordinate frames

### 🛠️ Tech Stack

- **Python**
- **HuggingFace Transformers**
- **PyTorch**