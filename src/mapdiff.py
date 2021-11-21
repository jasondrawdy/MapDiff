# -*- coding: utf-8 -*-
# ########################################################################
# Program: MapDiff
# Author: "Jason Drawdy (Buddha)"
# Version: "1.0.0"
# Date: 11/7/21 @ 1:58 AM
# #########################################################################
# mapdiff.py - System comparison tool used in conjuction with Pathwalk.
#
# Description:
# A compact module which can be utilized to compare a hash map including
# system files, directories, and all of their relevant information.
# #########################################################################
import os
import sys
import asyncio
import platform
import datetime
from logger import Logger
from sentinel import Sentinel
#from utils import TextUtils

_version = "1.0.0"
_version_name = "Flamberge"
_sentinel = Sentinel(verbose=False)
_logger = Logger(__name__, write_output=False)
_default_results_file = f"./mapdiff-results-{datetime.datetime.now().strftime('%Y-%m-%d')}.txt"

# def _print_progress_bar(current_index: int, max_index:int, progress_bar_message: str):
#     size = 25 # The amount of the desired char that should be displayed, i.e, '=' or '-'.
#     percent = current_index/max_index
#     sys.stdout.write('\r')
#     sys.stdout.write(f"[{'=' * int(size * percent):{size}s}] {int(100 * percent)}%  {progress_bar_message}")
#     sys.stdout.flush()
    
def _check_results_log():
    """Determines if a scan result file already exists and asks the user what they would like to do if it does."""
    valid_responses = ["y", "yes", "ok", "sure", "of course", "ofcourse", "duh", "okay", "yep", "yeah", "ye", "alright", "please", "bien", "si"]
    if os.path.exists(_default_results_file): 
        if input(f"The file '{_default_results_file}' already exists. Would you like to overwrite it?: ").lower() in valid_responses:
            os.remove(_default_results_file)
            _logger.note(f"The file '{_default_results_file}' will now be overwritten.")
        else: _logger.note(f"The file '{_default_results_file}' will not be deleted and will only be appended to.")

class Analyzer:
    def __init__(self: "Analyzer", original_map_file: str, current_map_file: str) -> None:
        """Constructs a new analyzer object with the provided system map files and attempts to reconstruct them into internal hash maps.
        
        Parameters
        ----------
        :param original_map_file: The original system map file path containing a valid MapDiff data schema.
        :type original_map_file: str\n
        :param current_map_file: The current system map file path containing a valid MapDiff data schema.
        :type current_map_file: str
        """
        if not os.path.exists(original_map_file):
            _logger.error("Please provide the original hash map to compare against the current one.")
            sys.exit(2)
        if not os.path.exists(current_map_file):
            _logger.error("Please provide the current hash map to compare against the original one.")
            sys.exit(2)
        self.original_map = self._build_map(original_map_file)
        self.current_map = self._build_map(current_map_file)
        self.found_data = None
        _logger.note("System maps have been reconstructed!")

    def _build_map(self: "Analyzer", filename: str) -> None:
        """Creates a dictionary containing valid MapDiff data from the specified file.
        
        Parameters
        ----------
        :param filename: A hash map file path containing a valid MapDiff data schema.
        :type filename: str\n
        """
        _logger.info(f"Building system map for: '{filename}'")
        try:
            with open(filename, 'r') as stream:
                hash_map = dict()
                for line in stream:
                    current_file_data = line.split('>')[-1].split("|")
                    current_file_name = f"{current_file_data[0].strip()}|"
                    hash_map[current_file_name] = '|'.join(current_file_data).strip().replace(current_file_name, "")
            return hash_map
        except Exception as error: _logger.error(str(error))

    # def _find(self: "Analyzer", filename: str, substring: str) -> bool:
    #     """Sequentially locates a character or entire string within a larger body of text using the provided document file."""
    #     with open(filename, 'r') as stream:
    #         for line in stream:
    #             if substring in line:
    #                 self.found_data = line
    #                 return True
    #     return False

    def compare(self: "Analyzer", original_map_file: str, current_map_file: str, print_to_console: bool = False) -> dict:
        """Checks for data changes between two system map files created using the Pathwalk program written by `Jason Drawdy (Buddha)`.
        
        Parameters
        ----------
        :param original_map_file: The original system map file path containing a valid MapDiff data schema.
        :type original_map_file: str\n
        :param current_map_file: The current system map file path containing a valid MapDiff data schema.
        :type current_map_file: str\n
        :param print_to_console: A flag determining whether or not to print verbose work to the terminal.
        :type print_to_console: object, optional

        Returns
        ----------
        :rtype: dict
        :return: A dictionary populated with files and their corresponding data based on changes in the provided map files.
        """
        _logger.info("Comparing both system map files...")
        result_set = dict()
        original_set = set(self.original_map.items())
        current_set = set(self.current_map.items())
        set_difference = original_set ^ current_set
        for entry_tuple in set_difference:
            if not entry_tuple[0] in result_set:
                result_set[entry_tuple[0]] = entry_tuple[1]
        return result_set
        #! The above code is the best.

        # count = 0
        # logger.note(f"Starting comparison between: '{original_map_file}' and '{current_map_file}'.")
        # for filename in self.current_map:
            # count += 1
            # print(f"{get_timestamp()} | INFO | {__name__} > {count}. Evaluating '{filename}'")
            # if filename in self.original_map:
                # if self.current_map[filename] != self.original_map[filename]:
                    # logger.warning(f"{get_timestamp()} - Change detected in '{filename}'!\n\n")
                    # abc = input("Found!")
        #! Above code is better.

        # with open(current_map_file, 'r') as stream:
        #     line_count = 0
        #     for line in stream:
        #         line_count += 1
        #         if print_to_console: print(f"{line_count}. {line}")
        #         current_file_data = line.split('>')[-1].split("|")
        #         current_file_name = f"{current_file_data[0].strip()}|"
        #         current_file_checksum = current_file_data[-1].split(" ")[-1].strip().replace("\n", "")
        #         if current_file_name in self.map:
        #             if current_file_checksum != self.map[current_file_name]:
        #                 logger.warning(f"{get_timestamp()} - Change detected in '{current_file_data[0].strip()}'!\n\n")
        #                 abc = input("Found!")
        #! Above code is good.

                # if self._find(original_map_file, f"{current_file_data[0].strip()}|"): 
                #     original_file_data = self.found_data.split('>')[-1].split("|")
                #     original_checksum = (original_file_data[-1].split(" ")[-1].strip().replace("\n", ""))
                #     current_checksum = (current_file_data[-1].split(" ")[-1].strip().replace("\n", ""))
                #     if current_checksum != original_checksum:
                #         logger.warning(f"{get_timestamp()} - Change detected in '{current_file_data[0].strip()}'!\n\n")
                #         abc = input("Found!")
                #         #* Log the modified file into a file.
                #! The above is slow...

class Program:
    def __init__(self: "Program") -> None:
        self.verbose = False
        self.original_map = None
        self.current_map = None
        self.file_mode = 'a'

    def _print_greeting(self: "Program") -> None:
        """Displays a welcome message for the user upon initialization of the script without parameters or during usage."""
        greeting = ("======================================\n" +
                    "✨       Welcome to: MapDiff!       ✨\n" +
                    "======================================\n")
        info = [
            f'⇢ Version\t| MapDiff (v{_version})[{_version_name}]',
            f'⇢ Author\t| Jason Drawdy (Buddha)',
            f'⇢ Platform\t| Python (v{platform.python_version()})',
            f'⇢ Spawned\t| {datetime.datetime.now()}',
        ]
        line_bar = ""
        line_bar_length = 0
        for bar in info:
            if len(bar) > line_bar_length:
                line_bar_length = len(bar)
        while len(line_bar) != line_bar_length+10:
            line_bar += "-"
        print('\n'+ f"{greeting}")
        print(f"{line_bar}")
        for entry in info:
            print(f"{entry}")
        print(f"{line_bar}")

    def _print_usage(self: "Program") -> None:
        """Displays detailed documentation for the user upon request or misuse of the script."""
        usage = [
            "\n===========================================",
            f"Usage: {os.path.basename(__file__)}: [options] <parameters>",
            "===========================================",
            "-h or --help..............| Displays the current help documentation for the program.",
            "-v or --verbose...........| Displays all of the work currently being performed by the script.\n\n"
            "===========================================",
            f"Examples: ",
            "===========================================",
            f"Start a comparison........| {os.path.basename(__file__)} original_hash_map current_hash_map",
            f"Compare with verbose......| {os.path.basename(__file__)} -v file1 file2",
            f"Show help documentation...| {os.path.basename(__file__)} -h",
            f"\nFor more information please visit: https://github.com/jasondrawdy\n"
        ]
        self._print_greeting()
        for line in usage: print(line)

    def _scan(self: "Program"):
        """Begins comparing the differences between two provided system map files generated by the Pathwalk program written by `Jason Drawdy (Buddha)`."""
        output_message = f"OUTPUT GENERATED BY: MapDiff v({_version})[{_version_name}] on {datetime.datetime.now().strftime('%Y-%m-%d @ %H:%M:%S')}\n"
        _logger.success("MapDiff has been successfully intialized!")
        _check_results_log()
        try:
            total_count, difference_count = 0, 0
            analyzer = Analyzer(self.original_map, self.current_map)
            difference_map = analyzer.compare(self.original_map, self.current_map, print_to_console=self.verbose) # Params retained for learning from older compare algorithms.
            if len(difference_map) > 0:
                change_detected_message = f"Changes were detected in the system maps!\n\nPlease check '{_default_results_file}' for more details.\n"
                with open(_default_results_file, self.file_mode) as stream:
                    for filename in difference_map:
                        try:
                            total_count += 1
                            filename_parts = str(filename).split(" ")
                            original_data = [f"\t{item}" for item in analyzer.original_map[filename].split('|')]
                            current_data = [f"\t{item}" for item in analyzer.current_map[filename].split('|')]
                            original_checksum = str(original_data[-1].split(' ')[-1].strip())
                            current_checksum = str(current_data[-1].split(' ')[-1].strip())
                            if current_checksum != original_checksum:
                                merged_original = '\n'.join(original_data)
                                merged_current = '\n'.join(current_data)
                                seperator = ''.join(["=" for count in range(0, 100)])
                                seperator2 = ''.join(["-" for count in range(0, 100)])
                                data = f"{seperator}\n[{filename_parts[0][:-1].upper()}]: {filename_parts[-1][:-1]}\n{seperator}\n[ORIGINAL DATA]: \n{merged_original}\n{seperator2}\n[CURRENT DATA]: \n{merged_current}\n\n\n\n"
                                stream.write(data)
                                difference_count += 1
                                if self.verbose: print(data)
                        except KeyError: pass # The original map didn't have the file. #* Do something with the newly found files...
                        #_print_progress_bar(total_count, len(difference_map), f"") #? The progress bar makes the algorithm very slow.
                    difference_message = f"There is a file change difference of {difference_count} between the system maps originally located at '{self.original_map}' and '{self.current_map}'.\n"
                    stream.write(output_message)
                    stream.write(difference_message)
                    stream.close()
                    if self.verbose:
                        print(output_message.replace('\n', ''))
                        print(difference_message)
                    _logger.warning(change_detected_message)
            else: _logger.success("No changes were found among the map files. 😃")
            _logger.success("Comparison finished!")
        except Exception as error: _logger.error(str(error))

    def main(self: "Program"):
        """Main initialization point for the application which checks for options, arguments, and parameters."""
        asyncio.run(asyncio.sleep(.5)) # Give the sentinel time to clean up.
        error = False
        try: 
            if "-v" in sys.argv or "--verbose" in sys.argv:
                sys.argv.remove("-v") if "-v" in sys.argv else sys.argv.remove("--verbose")
                self.verbose = True
            if "-h" in sys.argv or "--help" in sys.argv: #? If the help flag is detected anywhere just display it instead of doing anything else.
                sys.argv.remove("-h") if "-h" in sys.argv else sys.argv.remove("--help")
                error = True
                self._print_usage()
                sys.exit(2)
        except Exception as error:
            self._print_usage()
            _logger.error(f"{str(error).capitalize()}\n")
            sys.exit(2)
        if not error: #? Run all of the appropriate functions provided the proper options were given.
            if len(sys.argv) > 0:
                if len(sys.argv) > 3:
                    self._print_usage()
                else:
                    try:
                        self.original_map = sys.argv[1]
                        self.current_map = sys.argv[2]
                        self._print_greeting()
                        self._scan()
                    except: self._print_usage()
            else: self._print_usage()
        else: sys.exit(2)

if __name__ == "__main__":
    _sentinel.authorized = True
    _sentinel.start_resolver()
    program = Program()
    program.main()