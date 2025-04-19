class Formats:
    def __init__(self):
        self.supported_formats = ['odt', 'pdf', 'docx']

    def is_supported(self, report_type):
        return report_type in self.supported_formats
