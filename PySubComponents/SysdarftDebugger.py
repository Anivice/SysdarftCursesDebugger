import requests


class TargetUnreachable(Exception):
    def __init__(self, message="Cannot reach remote target"):
        self.message = message
        super().__init__(self.message)


class BackendAPIIncorrectResponse(Exception):
    def __init__(self, message="Remote backend responded with incorrect API format"):
        self.message = message
        super().__init__(self.message)


class SysDbg:
    def __init__(self, target):
        self.target = target

    def req_api_ver(self):
        response = requests.get(self.target + "/IsAPIAvailable")
        if response.status_code != 200:
            raise TargetUnreachable("Target " + self.target + " is unreachable")

        json_parsed_response = response.json()

        if not "Version" in json_parsed_response:
            raise BackendAPIIncorrectResponse(self.target + " provides an incorrect API")

        return json_parsed_response["Version"]

    # def req_continue(self):

