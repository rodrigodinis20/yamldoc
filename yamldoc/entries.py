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
            output = f'## `{self.name}`\n\n{self.meta}\n\n'
            output += "### Member variables:\n\n"

            output += "| Parameter | Mandatory | Type | Example | Default | Information |\n"
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

    def __init__(self, key, value, meta):
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
        self.default = "Mandatory is not specified"

    def __repr__(self):
        """
        Gives a print representation for the class.
        """
        if self.type is not None:
            return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}\n\t Type: {self.type}\n\t Mandatory: {self.mandatory}\n\t Default: {self.default}'
        else:
            return f'YAML Entry [{self.key}: {self.value}]\n\t Meta: {self.meta}'

    def to_markdown(self, schema=False):
        """
        Prints the entry as markdown.

        Arguments:
            schema: Print with four columns instead of three.
        """
        if schema:
            # m = '<br />'.join(textwrap.wrap(self.meta, width=50))
            m = self.meta
            default = self.default
            if "$" in m:
                vartype = self.type
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
                mandatory = self.mandatory
                accepted_types = ["yes", "no"]
                if m[m.find("%") + 1:].split()[0] in accepted_types:
                    mandatory = m[m.find("%") + 1:].split()[0]
                    try:
                        if "@" in m:
                            default = m[m.find("@") + 1:].split()[0]
                            m = m.replace(m[m.find("@"):].split()[0], "")
                        elif mandatory == "yes":
                            default = ""
                        else:
                            default = "Default value is not specified"
                            # m = m.replace(m[m.find("@"):].split()[0], "")
                    except IndexError:
                        default = "Default value is not specified"
                        m = m.replace(m[m.find("@"):].split()[0], "")
                else:
                    mandatory = "invalid input"
                m = m.replace(m[m.find("%"):].split()[0], "")
            else:
                # raise Exception("Mandatory is not specified in " + self.key)
                mandatory = ""
            key = self.key
            if key.startswith("#"):
                key = key.replace("#", "", 1)

            return f'| {key} | {mandatory} | {vartype} | {self.value} | {default} | {m} |'
        else:
            m = '<br />'.join(textwrap.wrap(self.meta, width=50))
            return f'| `{self.key}` | `{self.value}` | {m} |'
