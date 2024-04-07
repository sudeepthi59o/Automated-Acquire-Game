import sys
import json
import os

parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_directory)


from JSONOutput import JSONOutput

def process_json(input_data):
    js=JSONOutput()
    return js.runGame(input_data)

def run_test(input_file_name, output_file_name,N):
    try:
        with open(input_file_name, 'r') as input_file:
            input_json = json.load(input_file)
    except FileNotFoundError:
        print(f"Error: File not found - {input_file_name}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file - {input_file_name}")
        sys.exit(1)
    
    try:
        with open(output_file_name, 'r') as output_file:
            expected_output_json = json.load(output_file)
    except FileNotFoundError:
        print(f"Error: File not found - {output_file_name}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file - {output_file_name}")
        sys.exit(1)

    output_json = process_json(input_json)
    #print(output_json)
    try:
        output_str = json.dumps(output_json)
    except Exception as e:
        output_json= "Error, caught an exception"
        output_str = "Error, caught an exception"

    #print(output_json)
    #print("*===============*")
    print("------------------------------------------------")
    if output_json == expected_output_json:
        print(f"For the files in{i}.json and out{i}.json:" )
        print("Test passed!")
    else:
        print(f"For the files in{i}.json and out{i}.json" )
        print("Test failed!")
        print("Actual Output:")
        print(json.dumps(output_str))
        print("Expected Output:")
        print(json.dumps(expected_output_json))
    print("=======================TEST END=========================>")

if __name__ == "__main__":
   
    if len(sys.argv) != 1:
        print("Invalid number of command line arguments")
        sys.exit(1)

    directory_path = os.path.dirname(os.path.abspath(__file__))+'/player-tests'

    for i in range(len(os.listdir(directory_path))//2):
        input_file = f"in{i}.json"
        output_file = f"out{i}.json"
        
        input_file_name = os.path.join(directory_path, input_file)
        output_file_name = os.path.join(directory_path, output_file)
        
        run_test(input_file_name, output_file_name,i)