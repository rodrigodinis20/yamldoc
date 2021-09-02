import re
import textwrap


class MetaEntry:
    """ 
    A container to hold a base level YAML entry plus any associated
    hierarchical keys and values. 
    """

    def __init__(self, name, meta):
        """ 
        Initialize the object.

        Arguments:
            name: Name of the value.
            meta: Comments derived from YAML file.
        """
        self.name = name
        self.meta = meta
        self.isBase = True
        self.entries = []
        self.has_schema = False

    def __repr__(self):
        """
        Returns a print representation.
        """
        if self.has_schema:
            return f'YAML Meta Object with {len(self.entries)} entries [{self.name}] and type information.'
        else:
            return f'YAML Meta Object with {len(self.entries)} entries [{self.name}]'

    def to_markdown(self, schema=False):
        """ 
        Prints the contents of the object in markdown.

        Argumenets:
            schema: Print with four columns instead of three.
        """
        if schema:

            if "%" in self.meta:
                self.meta = self.meta.replace(self.meta[self.meta.find("%"):].split()[0], "")
            if "$" in self.meta:
                self.meta = self.meta.replace(self.meta[self.meta.find("$"):].split()[0], "")
            if "@" in self.meta:
                self.meta = self.meta.replace(self.meta[self.meta.find("@"):].split()[0], "")
            output = f'## {self.name}\n\n{self.meta}\n\n'
            output += "### Member variables:\n\n"

            output += "| Parameter | Mandatory | Type | Default | Example | Information |\n"
            output += "| :-: | :-: | :-: | :-: | :-: | :-- |\n"

            entries = []

            for entry in self.entries:
                entries.append(entry.to_markdown(schema) + "\n")

            for entry in sorted(entries, key=lambda x: re.sub('[^A-Za-z]+', '', x).lower()):
                output += entry
            output += "\n\n"

            return output

        else:
            output = f'## `{self.name}`\n\n{self.meta}\n\n'
            output += "### Member variables:\n\n"

            output += "| Key | Value | Information |\n"
            output += "| :-: | :-: | :-- |\n"

            for entry in self.entries:
                output += entry.to_markdown()

            output += "\n\n"

            return output


class Entry:
    """
    Container for a single YAML key value pairing and associated metadata."""

    def __init__(self, key, value, meta, is_commented):
        """
        Initialize the object

        Arguments:
           key: Name of the value
           value: Given value.
           meta: Any associated comments or meta data.
        """
        self.key = key
        self.value = value
        self.meta = meta
        self.isBase = False
        self.type = None
        self.mandatory = None
        self.example = "Mandatory is not specified"
        self.is_commented = is_commented

    def __repr__(self):
        """
        Gives a print representation for the class.
        """
        if self.type is not None:
            return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}\n\t Type: {self.type}\n\t Mandatory: {self.mandatory}\n\t Example: {self.example}'
        else:
            return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}'

    def to_markdown(self, schema=False):
        """
        Prints the entry as markdown.

        Arguments:
            schema: Print with four columns instead of three.
        """
        if schema:
            m = self.meta
            example = self.example
            vartype = self.type
            mandatory = self.mandatory
            if "$" in m:
                accepted_types = ["byte", "boolean", "string", "integer", "long", "double", "char", "float", "short"]
                if m[m.find("$") + 1:].split()[0] in accepted_types:
                    vartype = m[m.find("$") + 1:].split()[0]
                    m = m.replace(m[m.find("$"):].split()[0], "")
                else:
                    vartype = "invalid variable type"
                    m = m.replace(m[m.find("$"):].split()[0], "")
            else:
                vartype = "Unknown"
            if "%" in m:
                accepted_types = ["yes", "no"]
                if m[m.find("%") + 1:].split()[0] in accepted_types:
                    mandatory = m[m.find("%") + 1:].split()[0]
                else:
                    mandatory = "invalid input"
                m = m.replace(m[m.find("%"):].split()[0], "")
            else:
                mandatory = ""

            if "@" in m:
                example = m.split("@", 1)[1]
                example = example.replace("@", "<br>")
                example = example.replace("<br>", "", 0)

                m = m.replace(m.split("@", 1)[1], "")
                m = m.replace("@", "")

            else:
                example = self.key + ": " + self.value

            if self.is_commented is True:
                default = ""
            elif self.is_commented is False:
                default = self.value

            return f'| {self.key} | {mandatory} | {vartype} | {default} | {example.replace(" ", "&nbsp;")} | {m.replace(" ", "&nbsp;")} |'
        else:
            m = '<br />'.join(textwrap.wrap(self.meta, width=50))
            return f'| `{self.key}` | `{self.value.replace(" ", "&nbsp;")}` | {m.replace(" ", "&nbsp;")} |'
