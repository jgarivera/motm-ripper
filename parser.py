import re
import frontmatter
import sys
import datetime


class Parser:
    def __init__(self, data, post):
        self.pattern = re.compile(
            r"\[(?:(?:([01]?\d|2[0-3]):)?([0-5]?\d):)?([0-5]?\d)\]"
        )
        self.data = data
        self.metadata = {}
        self.post = post
        self.output = data
        self.ftr = [3600, 60, 1]
        self.current_offset = 0

    def set_metadata(self, keys):
        for key in keys:
            self.metadata[key] = self.post[key]
        self.__set_offset_seconds()

    def __set_offset_seconds(self):
        offset_recording_time = self.metadata["offset-recording-time"]
        self.offset_seconds = self.__get_seconds(offset_recording_time)

    def get_hydrated(self):
        self.hydrate_metadata()
        self.hydrate_timestamps()
        return self.output

    def hydrate_metadata(self):
        hydrated_string = self.output

        for key, value in self.metadata.items():
            hydrated_string = hydrated_string.replace("{" + key + "}", value)

        self.output = hydrated_string

    def __get_matches(self):
        matches = []

        for match in self.pattern.finditer(self.output):
            matches.append({"index": match.start(), "string": match.group()})

        return matches

    def hydrate_timestamps(self):
        expanded_string = self.output + ""
        recording_link = self.metadata["recording-link"]
        matches = self.__get_matches()

        for match in matches:
            index, raw_time_string = match["index"], match["string"]

            raw_seconds = self.__get_seconds(raw_time_string[1:-1])
            adjusted_seconds = raw_seconds - self.offset_seconds
            adjusted_time = str(datetime.timedelta(seconds=adjusted_seconds))
            adjusted_time_string = f"[{adjusted_time}]"

            expanded_string = expanded_string.replace(
                raw_time_string, adjusted_time_string
            )

            time_string_length = len(adjusted_time_string)
            offset_length = len(raw_time_string) - time_string_length

            total_offset = index + time_string_length

            link = f"({recording_link}?st={adjusted_seconds})"

            expanded_string = (
                expanded_string[: index + time_string_length + self.current_offset]
                + link
                + expanded_string[total_offset + self.current_offset :]
            )
            self.current_offset += len(link)  - offset_length

        self.output = expanded_string

    def __get_seconds(self, time_string):
        ftr_length = len(self.ftr)
        splits = time_string.split(":")
        split_count = len(splits)

        if split_count > ftr_length:
            raise IndexError("Time is out of bounds")

        for i in range(0, ftr_length - split_count):
            splits.insert(0, "00")

        return sum([a * b for a, b in zip(self.ftr, map(int, splits))])


if __name__ == "__main__":
    scratchpad = sys.argv[1]

    with open(f"scratchpads/{scratchpad}") as f:
        data = f.read()
        post = frontmatter.loads(data)

    parser = Parser(data, post)
    parser.set_metadata(
        [
            "date",
            "venue",
            "offset-recording-time",
            "from-time",
            "to-time",
            "recording-link",
            "powerpoint-link",
        ]
    )

    hydrated = parser.get_hydrated()
    build_path = f"scratchpads/hydrated/{scratchpad}"

    with open(build_path, "w") as output:
        output.write(hydrated)