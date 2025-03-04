from pathlib import Path

def main():
    input_file_path = Path(__file__).parent.parent / "requirements.txt"
    input_file_handle = open(file=input_file_path,mode="r")
    text_lines = input_file_handle.readlines()
    
    output_file_path = Path(__file__).parent.parent / "requirements-explained.txt"
    output_file_handle = open(output_file_path,mode="a")
    
    
    for index, line in enumerate(text_lines):
        package_name = line.split("==")[0] # ['asyncio','3.4.2']
        version_number = line.split("==")[1]
        # 1.    asyncio 
        #       3.4.2
        output_multiline = "%s .\t%s\n\t%s" % (index+1, package_name, version_number)
        print(output_multiline)
        output_file_handle.write(output_multiline)
        
    output_file_handle.close()
    input_file_handle.close()


if __name__ == "__main__":
    main()