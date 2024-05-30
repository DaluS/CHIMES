import os
import cloudpickle
from .._config import config  # _SAVE_FOLDER


class saveM:
    def __init__(self) -> None:
        pass

    def save(self,
             name: str,
             description: str = '',
             relativeaddress=True,
             verb=False):
        """
        Save the current state of the hub as a .chm file for later use.

        This function serializes the hub object and saves it to a .chm file. The file can be loaded later using `chm.load(name)`.

        Parameters
        ----------
        name : str
            The name of the file to save. If a path is provided, the file will be saved at that location. 
            The .chm extension is added automatically if not provided.
        description : str, optional
            A description of the run. Default is an empty string.
        relativeaddress : bool, optional
            If True, the file will be saved in the CHIMES save folder. If False, the file will be saved at the location specified by `name`. 
            Default is True.
        verb : bool, optional
            If True, the save location and description will be printed. Default is False.

        Returns
        -------
        None

        Raises
        ------
        Exception
            If the file extension provided in `name` is not .chm or no extension is provided, an exception is raised with the message 
            "extension not understood :{extension}, expected .chm or nothing".

        Notes
        -----
        The function first checks the file extension and raises an exception if it's not .chm or no extension is provided. 
        It then determines the save location based on the value of `relativeaddress`. 
        It opens the file at the save location in write mode and dumps the hub object and description into the file using cloudpickle.

        Author
        ------
        Paul Valcke
        Original : Didier Vezinet

        Date
        ----
        OLD
        """

        # Absolute path management
        _SAVE_FOLDER = config.get_current('_SAVE_FOLDER')
        _PATH_HERE = os.path.abspath(os.path.dirname(__file__))
        _PATH_SAVE = os.path.join(os.path.dirname(os.path.dirname(_PATH_HERE)), _SAVE_FOLDER)

        # Extension management
        if (name[-4:] != '.chm' and '.' not in name):
            name = name + '.chm'
        if name[-4:] == '.chm':
            pass
        elif '.' in name:
            raise Exception(f"extension not understood :{name.split('.')[1]}, expected .chm or nothing")

        if relativeaddress:
            address = os.path.join(_PATH_SAVE, name)
        else:
            address = name
        # Saving
        with open(address, 'wb') as f:
            if verb:
                print('File will be saved as : ', address)
                print('Associated description: ', description)
            cloudpickle.dump({'hub': self,
                              'description': description},
                             f)
