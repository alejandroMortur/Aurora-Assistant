import subprocess
import os
import threading
import psutil

def find_program(program_name):
    
    """
    Finds the executable path of a program by searching in the System32 directory.
    
    Args:
    - program_name (str): Name of the program to find.
    
    Returns:
    - list: List of found program paths.
    """
    
    # Get the path to the System32 directory
    system32_path = os.path.join(os.environ['SystemRoot'], 'System32')
    found_programs = []
    
    # Iterate through files in System32 directory
    for file_name in os.listdir(system32_path):
        # Check if the file name matches the program name with .exe extension
        if file_name.lower() == program_name.lower() + '.exe':
            found_programs.append(file_name)
            
    return found_programs

def open_program(program_name,queue):
    
    # Find the program paths
    program_paths = find_program(program_name)
    
    if program_paths:
        for program_path in program_paths:
            # Open each program in a separate thread
            print("---------------------------")
            print(f'{program_name} found. Opening...')
            queue.put("open program: "+program_name)
            print("---------------------------")
            thread = threading.Thread(target=subprocess.Popen, args=([os.path.join(os.environ['SystemRoot'], 'System32', program_path)],))
            thread.start()
            
    else:
        
        print("---------------------------")
        print(f'{program_name} not found.')
        queue.put(f'{program_name} not found.')
        print("---------------------------")
        

def close_program(program_name,queue):
    
    # Ensure program name has .exe extension
    program_name = program_name.lower() + '.exe'
    
    if is_program_running(program_name):
        
        # Close the program if it is running
        print("---------------------------")
        print(f'{program_name} found. Closing...')
        queue.put(f'{program_name} found. Closing...')
        print("---------------------------")
        
        subprocess.run(['taskkill', '/f', '/im', program_name])
        
    else:
        
        print("---------------------------")
        print(f'{program_name} not found or already closed.')
        queue.put(f'{program_name} not found or already closed.')
        print("---------------------------")
        

def is_program_running(program_name):
    
    # Convert program name to lowercase for case-insensitive comparison
    program_name = program_name.lower()
    
    for process in psutil.process_iter(['name']):
        # Check if any process matches the program name
        if process.info['name'].lower() == program_name:
            return True
        
    return False
