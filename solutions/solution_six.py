from solution import Solution


class SolutionSix(Solution):

    def get_signal(self) -> str:
        return self.readlines()[0].strip()

    # Returns True if a string contains any duplicate characters
    def _contains_duplicates(self, string: str) -> bool:
        # Keep track of the counts of all chars
        present_chars = set()

        # Loop through all the chars in the string
        for char in string:
            # If the char is already present, we found the duplicate
            if char in present_chars:
                return True

            # Mark this char as seen
            present_chars.add(char)

        # No dupes detected
        return False

    def find_marker(self, packet_length: int):
        last_processed_index = 0

        # Start looping through every character in the signal
        for char_index in range(0, len(self.get_signal()) - packet_length - 1):
            last_processed_index = char_index
            # Check if there are no duplicates within this packet_length char substring
            if not self._contains_duplicates(self.get_signal()[char_index:char_index + packet_length]):
                break

        return last_processed_index + packet_length

    def solve_p1(self):
        return self.find_marker(4)

    def solve_p2(self):
        return self.find_marker(14)
