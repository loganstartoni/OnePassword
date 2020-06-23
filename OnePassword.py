from json import loads
from json.decoder import JSONDecodeError
from subprocess import Popen, PIPE

# default values
debug = True


class OnePassword:
    _vault: str
    _op_session: str

    def __init__(self, subdomain: str, op_session: str, vault: str):
        """
        Init function that establishes the session and saves the _vault used for the project.

        :param op_session: A session that is 30 minutes to limit the exposure of the exposed Information
        :param vault: The _vault that contains the secrets. This allows for a limit on exposed information.
        """

        self._op_session = f'export OP_SESSION_{subdomain}="{op_session}"'
        if debug:
            print(self._op_session)
        self._vault = vault

    def get_all_items_in_vault(self) -> dict:
        """
        Return all values in the dict defined in this OnePassword Object

        :return: The dict for all the values in the object
        """
        return self._call_one_password_cli("list items")

    def get_item_by_name(self, pass_name: str) -> dict:
        """
        Gets an item by name from the vault.

        :param pass_name: the name of the one password object
        :return: The dict for the one pssword object
        """
        return self._call_one_password_cli(f'get item "{pass_name}"')

    def get_item_by_id(self, pass_id: str) -> dict:
        """
        Gets an item by uuid from the vault.

        :param pass_id: the uuid of the one password object
        :return: The dict for the one pssword object
        """
        return self._call_one_password_cli(f'get item "{pass_id}"')

    def _call_one_password_cli(self, input_command) -> dict:
        """
        Internal function to standardize the call of the one password program.

        In the event that tat you are calling for a single object this will throw an Error if the object is not present.
        You can catch that if your program can handle this being missing.
        
        :param input_command: Customization of the command.
        :return: The json object returned as a dictionary.
        """
        op_command = f'{self._op_session}; op {input_command} --vault "{self._vault}"'
        if debug:
            print(op_command)
        op_response = Popen(op_command, shell=True, stdout=PIPE).stdout.read()
        if debug:
            print(op_response)
        try:
            output = loads(op_response)
            return output
        except JSONDecodeError as exc:
            NotImplementedError("The object is not present in the dictionary.")

if __name__ == '__main__':
    in_subdomain = "startoni"
    in_session = "9bRYLZIessCh5PJNlI71sR0AnPNv8AgBNwXFmpbGWhM"
    in_vault = "Archive"

    op = OnePassword(in_subdomain, in_session, in_vault)
    op.get_all_items_in_vault()
    op.get_item_by_id("ipnpxfrsznczrdebfr2mnpovri")
    op.get_item_by_name("Blurb")