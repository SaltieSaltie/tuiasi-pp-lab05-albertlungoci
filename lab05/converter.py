"""
Convertor text → HTML.

Prima linie din text devine titlu <h1>.
Blocurile separate de linii goale devin paragrafe <p>.
"""


class TextToHtmlConverter:
    """Convertește text simplu în HTML structurat."""

    # TODO: Implementează metoda convert
    def convert(self, text: str) -> str:
        """Convertește textul în HTML.

        Prima linie devine <h1>, blocurile separate de linie goală
        devin paragrafe <p>.

        Args:
            text: Textul de convertit.

        Returns:
            String HTML valid.
        """
        raise NotImplementedError("De implementat")
