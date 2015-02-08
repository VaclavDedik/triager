import os
import re
import logging
import json

from classifier.document import Document
from classifier.parsers import DocumentParser


class MRSParser(DocumentParser):
    """Parses MRS data stored in a folder as html files into list of documents.
    Title of the document is parsed from the header of the file, content is
    parsed from *Problem Description* section. Label is parsed from the first
    *Action-By* field which represents the assignee. If Action-By field
    contains *Unassigned*, the label is replaced by ``None`` object in the
    ``Document`` object.
    """

    def __init__(self, folder, project_match=".*"):
        self.folder = folder
        self.project_match = project_match

    def parse(self):
        """Parses data from given folder into list of documents.

        :returns: List of Document objects
        """

        files = os.listdir(self.folder)
        documents = []

        for f in files:
            if f not in ['.DS_Store']:  # excluded files
                full_f = os.path.join(self.folder, f)
                ticket_info = self._parse_file(full_f)
                if ticket_info and re.match(
                        self.project_match, ticket_info[3]):
                    if ticket_info[2] == "Unassigned":
                        ticket_info[2] = None
                    document = Document(
                        ticket_info[0], ticket_info[1], ticket_info[2])
                    documents.append(document)

        return documents

    def _parse_file(self, fname):
        with open(fname) as f:
            content = f.readlines()
            content = [line.rstrip() for line in content]

        ticket_info = [None, "", None, ""]
        ticket_id = os.path.basename(fname).replace(".html", "")
        description_stage = 0
        is_bug = False
        for line in content:
            if not line.startswith("|"):
                continue

            # get summary
            summary_match = re.match("^\| " + ticket_id + " : (.*)\|$", line)
            if summary_match and not ticket_info[0]:
                ticket_info[0] = summary_match.group(1).strip()

            # get project
            project_match = re.match("^\| Found In:   ([\w]+)", line)
            if project_match and not ticket_info[3]:
                ticket_info[3] = project_match.group(1).strip()

            # test if is bug
            if not is_bug and re.match("\| Created:", line) \
                    and re.match(".*\| Class: ER\|.*", line):
                is_bug = True

            # get assignee (only from the first APS line)
            assignee_match = re.match("\| Action-By:  ([\w,']+)", line)
            if assignee_match and not ticket_info[2]:
                ticket_info[2] = assignee_match.group(1).strip()

            # get description
            description_match = re.match(
                "\| MR: " + ticket_id + "  Problem Description", line)
            if description_match:
                description_stage = 1
                continue
            if description_stage == 1:
                if line.startswith("|*** "):
                    description_stage = 2
            elif description_stage == 2:
                if line.startswith("|*** ") or line.startswith("|---"):
                    description_stage = 3
                    break
                ticket_info[1] += line.replace("|", "").strip() + "\n"

        if not is_bug:
            return None

        if not ticket_info[0]:
            logging.warn("Could not parse summary from ticket %s.", ticket_id)
        if not ticket_info[1]:
            logging.warn(
                "Could not parse description from ticket %s", ticket_id)
        else:
            ticket_info[1] = ticket_info[1].strip()
        if not ticket_info[2]:
            logging.warn("Could not parse assignee from ticket %s", ticket_id)

        return ticket_info


class BugzillaParser(DocumentParser):
    """Parser for bugzilla bugs, e.g. Mozilla, Red Hat etc."""

    BUGS_FILE = "bugs"
    COMMENTS_FILE = "latest_comments"

    def __init__(self, folder):
        """Specify folder that contains two files, 'bugs' and 'latest_comments.
        """

        self.folder = folder

    def parse(self):
        bugsfn = os.path.join(self.folder, self.BUGS_FILE)
        commentsfn = os.path.join(self.folder, self.COMMENTS_FILE)

        with open(bugsfn, "r") as bugsf:
            bugs_raw = bugsf.read()
        with open(commentsfn, "r") as commentsf:
            comments_raw = commentsf.read()

        bugs = json.loads(bugs_raw)["bugs"]
        comments = json.loads(comments_raw)

        documents = []
        for bug in bugs:
            title = bug["summary"]
            description = comments[str(bug["id"])]["comments"]["text"]
            label = bug["assigned_to"]
            document = Document(title, description, label)
            documents.append(document)

        return documents
