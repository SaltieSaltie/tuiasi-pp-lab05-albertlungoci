"""
Worker proces pentru conversia text → HTML.

Primește text dintr-o coadă de intrare, îl convertește
și trimite rezultatul în coada de ieșire.
"""

import multiprocessing
from lab05.converter import TextToHtmlConverter


class ConverterWorker(multiprocessing.Process):
    """Proces worker care realizează conversia în fundal."""

    def __init__(
        self,
        input_queue: multiprocessing.Queue,
        output_queue: multiprocessing.Queue,
    ) -> None:
        """Inițializează workerul cu cozile de comunicare.

        Args:
            input_queue: Coada din care se citește textul de convertit.
            output_queue: Coada în care se scrie rezultatul HTML.
        """
        super().__init__()
        # TODO: Salvează referințele la cozi
        raise NotImplementedError("De implementat")

    # TODO: Implementează metoda run
    def run(self) -> None:
        """Bucla principală a workerului.

        Citește mesaje din input_queue, le convertește și
        trimite rezultatul în output_queue.
        Workerul se oprește când primește None ca mesaj.
        """
        raise NotImplementedError("De implementat")
