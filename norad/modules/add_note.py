#!/usr/bin/env python

class AddNote:

    def __init__(self, factory):
        self.config = factory.get_config()

    def get_command(self):
        return "add_note"

    def get_description(self):
        return '''add_note: Adds a note to the NORA storage.
The body of the request should contain a properly formatted note.

Example:
        
Title: Some note
Category: AI
[... Any MIME data valid...]

Contents of the note, e.t.c.
'''

    def is_valid_request(self, request):
        return True 

    def process_request(self, request):
        return ""
