import subprocess

def generate_booklet():
    try:
        # Run the generate_content.py script
        subprocess.run(["python3", "generate_content.py"], check=True)
        
        # Convert the generated markdown file to PDF using Pandoc
        subprocess.run(["pandoc", "Booklet/CODING_BOOKLET.md", "-o", "Booklet/CODING_BOOKLET.pdf", "--pdf-engine=xelatex"], check=True)
        
        print("Booklet generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while generating the booklet: {e}")

if __name__ == "__main__":
    generate_booklet()
