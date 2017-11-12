import peewee as pw
import os as _os

db_path = _os.path.dirname(_os.path.abspath(__file__)) + "/PCS.db"
db = pw.SqliteDatabase(db_path)

def _check_level(level, name="level"):
    """
    Checks "level" is an integer between 1 and 4 inclusive,
    and raises a ValueError exception else.
    """
    if level not in range(1, 5):
        raise ValueError("The '{}' parameter must be between 1 and 5.".format(name))

class PCS(pw.Model):
    """A PCS, as stored in database.
    
    This object is a Peewee model, so you can use all the Peewee's
    methods on it, like `select()`, `where()`, etc.
    
    Attributes
    ----------
    code : str
        The code of the PCS. For example : "382b" (for level 4).
        Between one and four characters.
    description : str
        The INSEE description of the PCS, in french.
        For example : "Architectes salariés".
    level : int
        The classification level, between 1 and 4 inclusive.
    parent : ForeignKey to another PCS, or None.
        The parent PCS. For example, "382b" (level 4)
        has "38" (level 3) as parent. "3" (level 1) has no parent.
        The inverse relationship uses the attribute "children".
    """
    
    code = pw.CharField(index=True)
    description = pw.CharField()
    level = pw.IntegerField(index=True)
    parent = pw.ForeignKeyField("self", null=True, related_name="children")
    
    class Meta:
        database = db
    
    def INSEE_url(self):
        """Returns the URL of the PCS page on the INSEE website.
        
        Returns
        -------
        str
            The URL, beginning with "https://".
        """
        base_url = {
            1: "https://insee.fr/fr/metadonnees/pcs2003/categorieSocioprofessionnelleAgregee/{}",
            2: "https://insee.fr/fr/metadonnees/pcs2003/categorieSocioprofessionnelle/{}",
            3: "https://insee.fr/fr/metadonnees/pcs2003/categorieSocioprofessionnelleDetaillee/{}",
            4: "https://insee.fr/fr/metadonnees/pcs2003/professionRegroupee/{}",
        }.get(self.level)
        return base_url.format(self.code)
    
    def iter_children(self, max_level=4):
        """A recursive iterator on the PCS and its children.
        
        Parameters
        ----------
        max_level : int, optional
            The level at which to stop the iteration, included.
            Must be between 1 and 4 inclusive. 4 default.
        
        Yields
        ------
        PCS
            The next PCS.
        """
        _check_level(max_level, name="max_level")
        yield self
        if self.level in [4, max_level]:
            return
        for child in self.children:
            yield from child.iter_children(max_level=max_level)
    
    def all_parents(self, include_self=True):
        """Returns recursively all the parents of the PCS.
        
        Parameters
        ----------
        include_self : bool, optional
            Defines whether the PCS must add itself at the beginning
            of the list.
        
        Returns
        -------
        list[PCS]
            The list of all the parents of the PCS,
            from the highest level to the lowest.
            Example:
            [
                <PCS '382b' (level 4)>, <PCS '38' (level 3)>,
                <PCS '36' (level 2)>, <PCS '3' (level 1)>
            ]
        """
        parents = []
        if include_self:
            parents.append(self)
        p = self
        while p.parent:
            p = p.parent
            parents.append(p)
        return parents
    
    def __repr__(self):
        return self.__str__()
    
    def __str__(self):
        return "<PCS '{}' (level {})>".format(self.code, self.level)

def get_all_PCS_of_level(level):
    """Gets all the PCS of a given level.
    
    It's just an "alias" for "PCS.select().where(PCS.level==level)".
    
    Parameters
    ----------
    level : int
        The desired level.
    
    Returns
    -------
    peewee.SelectQuery
        The PCS of the desired level, ready for filtering with peewee.
        Convertible into a list or a tuple.
    
    Raises
    ------
    ValueError
        If "level" is not between 1 and 4 inclusive.
    """
    _check_level(level)
    return PCS.select().where(PCS.level==level)

def get_PCS(level, code):
    """Gets a PCS from its level and its code.
    
    Parameters
    ----------
    level : int
        The level of classification.
    code : str
        The code of the PCS (for example: "382b").
    
    Returns
    -------
    PCS : The requested PCS.
    
    Raises
    ------
    ValueError
        If "level" is not between 1 and 4 inclusive.
        If not PCS was found for the given level and code.
    """
    _check_level(level)
    try:
        return PCS.get(PCS.level==level, PCS.code==code)
    except PCS.DoesNotExist:
        raise ValueError(
            "No PCS was found with code '{code}' at level '{level}'.".format(
                code=code, level=level
            )
        )

db.connect()
